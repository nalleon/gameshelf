import pytest
from rest_framework.test import APIClient

from classifications.models import Platform
from tests.factories.games import GameFactory
from tests.factories.libraries import (
    LibraryFactory,
    LibraryItemFactory,
    UserFactory,
)

@pytest.mark.django_db
def test_get_own_library(client_admin):
    LibraryFactory(user=client_admin.user)

    response = client_admin.get('/api/library/')

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_own_library_unauthorized(client):
    response = client.get('/api/library/')

    assert response.status_code == 401
    
@pytest.mark.django_db
def test_edit_own_library(client_admin):
    LibraryFactory(user=client_admin.user, is_private=False)

    payload = {
        'is_private': True
    }

    response = client_admin.patch('/api/library/', payload, format='json')

    assert response.status_code == 200
    assert response.data['is_private'] is True
    
@pytest.mark.django_db
def test_edit_own_library_unauthorized(client):
    payload = {'is_private': True}

    response = client.patch('/api/library/', payload, format='json')

    assert response.status_code == 401
    
@pytest.mark.django_db
def test_add_library_item(client_admin):
    library = LibraryFactory(user=client_admin.user)
    game = GameFactory()
    platform = game.platforms.first() or Platform.objects.create(name='PC')
    game.platforms.add(platform)

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'status': 'P',
        'is_private': False,
    }

    response = client_admin.post('/api/library/', payload, format='json')

    assert response.status_code == 201
    
@pytest.mark.django_db
def test_add_library_item_invalid_platform(client_admin):
    LibraryFactory(user=client_admin.user)
    game = GameFactory()
    platform = Platform.objects.create(name='PC')  # no añadido al juego

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'status': 'P',
        'is_private': False,
    }

    response = client_admin.post('/api/library/', payload, format='json')

    assert response.status_code == 400
    
@pytest.mark.django_db
def test_add_library_item_duplicate(client_admin):
    library = LibraryFactory(user=client_admin.user)
    game = GameFactory()
    platform = Platform.objects.create(name='PC')
    game.platforms.add(platform)

    LibraryItemFactory(library=library, game=game, platform=platform)

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'status': 'P',
        'is_private': False,
    }

    response = client_admin.post('/api/library/', payload, format='json')

    assert response.status_code == 400
    
@pytest.mark.django_db
def test_get_library_item_owner(client_admin):
    item = LibraryItemFactory(library__user=client_admin.user)

    response = client_admin.get(f'/api/library/{item.pk}/')

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_library_item_private_forbidden():
    owner = UserFactory()
    other = UserFactory()

    item = LibraryItemFactory(library__user=owner, is_private=True)

    client = APIClient()
    client.force_authenticate(user=other)

    response = client.get(f'/api/library/{item.pk}/')

    assert response.status_code == 403
    
@pytest.mark.django_db
def test_get_library_item_public_other_user():
    owner = UserFactory()
    other = UserFactory()

    item = LibraryItemFactory(library__user=owner, is_private=False)

    client = APIClient()
    client.force_authenticate(user=other)

    response = client.get(f'/api/library/{item.pk}/')

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_edit_library_item(client_admin):
    item = LibraryItemFactory(library__user=client_admin.user)
    platform = item.platform

    payload = {
        'platform_id': platform.pk,
        'status': 'CMP',
        'hours_played': 10,
        'is_private': True,
    }

    response = client_admin.patch(
        f'/api/library/{item.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_edit_library_item_forbidden():
    owner = UserFactory()
    other = UserFactory()

    item = LibraryItemFactory(library__user=owner)

    client = APIClient()
    client.force_authenticate(user=other)

    payload = {
        'platform_id': item.platform.pk,
    }

    response = client.patch(
        f'/api/library/{item.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 403
    
@pytest.mark.django_db
def test_delete_library_item(client_admin):
    item = LibraryItemFactory(library__user=client_admin.user)

    response = client_admin.delete(f'/api/library/{item.pk}/')

    assert response.status_code == 204
    
@pytest.mark.django_db
def test_delete_library_item_forbidden():
    owner = UserFactory()
    other = UserFactory()

    item = LibraryItemFactory(library__user=owner)

    client = APIClient()
    client.force_authenticate(user=other)

    response = client.delete(f'/api/library/{item.pk}/')

    assert response.status_code == 403
    
@pytest.mark.django_db
def test_get_user_library_public(client):
    user = UserFactory()
    LibraryFactory(user=user, is_private=False)

    response = client.get(f'/api/library/users/{user.pk}/')

    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_user_library_private_forbidden(client):
    user = UserFactory()
    LibraryFactory(user=user, is_private=True)

    response = client.get(f'/api/library/users/{user.pk}/')

    assert response.status_code == 404
    
@pytest.mark.django_db
def test_get_user_library_owner(client_admin):
    LibraryFactory(user=client_admin.user, is_private=True)

    response = client_admin.get(f'/api/library/users/{client_admin.user.pk}/')

    assert response.status_code == 200