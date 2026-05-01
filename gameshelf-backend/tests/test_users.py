import pytest
from django.db import IntegrityError
from django.utils import timezone

from users.models import Profile, UserToken
from tests.factories.users import (
    UserFactory,
    ProfileFactory,
    AdminProfileFactory,
    UserTokenFactory,
    ExpiredUserTokenFactory,
)

@pytest.mark.django_db
def test_profile_creation():
    profile = ProfileFactory()

    assert profile.pk is not None
    assert profile.user is not None
    assert profile.color_bg.startswith("#")
    
@pytest.mark.django_db
def test_profile_one_to_one_constraint():
    user = UserFactory()

    ProfileFactory(user=user)

    with pytest.raises(IntegrityError):
        ProfileFactory(user=user)
        
@pytest.mark.django_db
def test_profile_default_role():
    profile = ProfileFactory()

    assert profile.role == Profile.Role.USER
    
@pytest.mark.django_db
def test_admin_profile_role():
    profile = AdminProfileFactory()

    assert profile.role == Profile.Role.ADMIN
    assert profile.verified is True
    
@pytest.mark.django_db
def test_profile_verified_flag():
    profile = ProfileFactory(verified=True)

    assert profile.verified is True
    
@pytest.mark.django_db
def test_user_token_creation():
    token = UserTokenFactory()

    assert token.pk is not None
    assert token.token is not None
    assert token.user is not None
    
@pytest.mark.django_db
def test_user_token_uuid_unique():
    t1 = UserTokenFactory()
    t2 = UserTokenFactory()

    assert t1.token != t2.token
    
@pytest.mark.django_db
def test_user_token_default_type():
    token = UserTokenFactory()

    assert token.type == UserToken.TokenType.VERIFY_EMAIL
    
@pytest.mark.django_db
def test_user_token_is_valid_true():
    token = UserTokenFactory()

    assert token.is_valid() is True
    
@pytest.mark.django_db
def test_user_token_is_valid_false():
    token = ExpiredUserTokenFactory()

    assert token.is_valid() is False
    
@pytest.mark.django_db
def test_user_token_expiry_boundary():
    token = UserTokenFactory()

    token.expires_at = timezone.now() - timezone.timedelta(seconds=1)
    token.save()

    assert token.is_valid() is False
    
@pytest.mark.django_db
def test_user_can_have_multiple_tokens():
    user = UserFactory()

    UserTokenFactory(user=user)
    UserTokenFactory(user=user)

    assert UserToken.objects.filter(user=user).count() == 2
    
@pytest.mark.django_db
def test_user_deletion_cascades_tokens():
    user = UserFactory()

    token = UserTokenFactory(user=user)

    user.delete()

    assert UserToken.objects.filter(id=token.id).count() == 0