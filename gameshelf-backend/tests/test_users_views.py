from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import Profile, UserToken

User = get_user_model()


@pytest.mark.django_db
def test_profile_me(client_admin):
    response = client_admin.get('/api/users/me/')

    assert response.status_code == 200
    assert response.data['user']['username'] == client_admin.user.username


@pytest.mark.django_db
def test_profile_me_unauthorized(client):
    response = client.get('/api/users/me/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_profile_detail(client):
    user = User.objects.create_user(username='test', password='pass')
    profile = Profile.objects.create(user=user)

    response = client.get(f'/api/users/{profile.pk}/')

    assert response.status_code == 200
    assert response.data['id'] == profile.pk


@pytest.mark.django_db
def test_profile_detail_not_found(client):
    response = client.get('/api/users/999999/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_profile_edit_forbidden(client):
    user1 = User.objects.create_user(username='u1', password='pass')
    user2 = User.objects.create_user(username='u2', password='pass')

    profile = Profile.objects.create(user=user1)

    client.force_authenticate(user=user2)

    response = client.patch(f'/api/users/{profile.pk}/', {'bio': 'hack'}, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_profile_edit_success(client_admin):
    profile = client_admin.user.profile

    response = client_admin.patch(f'/api/users/{profile.pk}/', {'bio': 'new bio'}, format='json')

    profile.refresh_from_db()

    assert response.status_code == 200
    assert profile.bio == 'new bio'


@pytest.mark.django_db
def test_profile_edit_username_taken(client_admin):
    user2 = User.objects.create_user(username='existing', password='pass')
    Profile.objects.create(user=user2)

    profile = client_admin.user.profile

    response = client_admin.patch(
        f'/api/users/{profile.pk}/', {'username': 'existing'}, format='json'
    )

    assert response.status_code == 400
    assert 'taken' in response.data['error']


@pytest.mark.django_db
def test_search_profiles(client):
    user = User.objects.create_user(username='johnsmith', password='pass')
    Profile.objects.create(user=user)

    response = client.get('/api/users/search/?q=john')

    assert response.status_code == 200


@pytest.mark.django_db
def test_search_profiles_missing_q(client):
    response = client.get('/api/users/search/')

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_success(client):
    payload = {'username': 'newuser', 'password': 'pass123', 'email': 'new@test.com'}

    response = client.post('/api/auth/register/', payload, format='json')

    assert response.status_code == 201
    assert 'token' in response.data


@pytest.mark.django_db
def test_register_duplicate_username(client):
    User.objects.create_user(username='taken', password='pass')

    payload = {'username': 'taken', 'password': 'pass', 'email': 'x@test.com'}

    response = client.post('/api/auth/register/', payload, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_success_username(client):
    User.objects.create_user(username='john', password='pass123')

    payload = {'login': 'john', 'password': 'pass123'}

    response = client.post('/api/auth/login/', payload, format='json')

    assert response.status_code == 201
    assert 'token' in response.data


@pytest.mark.django_db
def test_login_success_email(client):
    User.objects.create_user(username='john', email='john@test.com', password='pass123')

    payload = {'login': 'john@test.com', 'password': 'pass123'}

    response = client.post('/api/auth/login/', payload, format='json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_login_invalid(client):
    payload = {'login': 'nope', 'password': 'wrong'}

    response = client.post('/api/auth/login/', payload, format='json')

    assert response.status_code == 401


# def test_change_password(client_admin):
#     user = client_admin.user
#     user.set_password('password123')
#     user.save()

#     client_admin.force_authenticate(user=user)

#     payload = {
#         'old_password': 'password123',
#         'new_password': 'newpass123',
#     }

#     response = client_admin.post(
#         '/api/auth/change-password/',
#         payload,
#         format='json',
#     )

#     assert response.status_code == 200


@pytest.mark.django_db
def test_change_password_wrong_old(client_admin):
    payload = {'old_password': 'wrong', 'new_password': 'newpass123'}

    response = client_admin.post('/api/auth/change-password/', payload, format='json')

    assert response.status_code == 400


# @pytest.mark.django_db
# def test_deactivate_account(client_admin):
#     response = client_admin.delete('/api/auth/deactivate/')

#     assert response.status_code == 200


@pytest.mark.django_db
@patch('users.views.deliver_verification_email.delay')
def test_send_verification_email(mock_task, client_admin):
    response = client_admin.post('/api/auth/verify-email/')

    assert response.status_code == 200
    mock_task.assert_called_once()


# @pytest.mark.django_db
# def test_verify_email_success(client_admin):
#     token = UserToken.objects.create(
#         user=client_admin.user,
#         type=UserToken.TokenType.VERIFY_EMAIL,
#         expires_at=timezone.now() + timezone.timedelta(hours=1),
#     )

#     response = client_admin.get(f'/api/auth/verify-email/{token.token}/')

#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_verify_email_invalid(client):
#     response = client.get('/api/auth/verify-email/00000000-0000-0000-0000-000000000000/')

#     assert response.status_code == 400


@pytest.mark.django_db
@patch('users.views.deliver_password_reset_email.delay')
def test_password_reset_email(mock_task, client):
    user = User.objects.create_user(username='u', email='u@test.com', password='pass')

    response = client.post('/api/auth/password-reset/', {'email': 'u@test.com'}, format='json')

    assert response.status_code == 200
    mock_task.assert_called_once()


@pytest.mark.django_db
@patch('users.views.deliver_password_reset_email.delay')
def test_password_reset_email_not_exist(mock_task, client):
    response = client.post('/api/auth/password-reset/', {'email': 'no@test.com'}, format='json')

    assert response.status_code == 200
    mock_task.assert_not_called()
