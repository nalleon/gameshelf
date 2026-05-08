import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Profile

User = get_user_model()


@pytest.fixture
def client_admin(db):
    user = User.objects.create_user(username='admin', password='pass')
    Profile.objects.create(user=user, role=Profile.Role.ADMIN)

    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.user = user
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def client():
    return APIClient()

