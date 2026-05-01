import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from classifications.models import Developer, Edition, Genre, Platform, Publisher, Region
from tests.factories.classifications import (
    DeveloperFactory,
    EditionFactory,
    GenreFactory,
    PlatformFactory,
    PublisherFactory,
    RegionFactory,
)
from users.models import Profile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


# =========================
# FIXTURE ADMIN
# =========================

@pytest.fixture
def client_admin(db):
    user = User.objects.create_user(username='admin', password='pass')
    Profile.objects.create(user=user, role=Profile.Role.ADMIN)

    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client

@pytest.fixture
def client():
    return APIClient()

# =========================
# PLATFORM
# =========================


@pytest.mark.django_db
def test_platform_list(client):
    PlatformFactory.create_batch(3)

    response = client.get('/api/platforms/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_platform_detail(client):
    platform = PlatformFactory()

    response = client.get(f'/api/platforms/{platform.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_platform_update(client_admin):
    platform = PlatformFactory()

    response = client_admin.put(
        f'/api/platforms/{platform.pk}/',
        data={'name': 'Updated Platform'},
        content_type='application/json',
    )

    assert response.status_code == 200
    platform.refresh_from_db()
    assert platform.name == 'Updated Platform'


@pytest.mark.django_db
def test_platform_delete(client_admin):
    platform = PlatformFactory()

    response = client_admin.delete(f'/api/platforms/{platform.pk}/')

    assert response.status_code in (200, 204)
    assert not Platform.objects.filter(pk=platform.pk).exists()


# =========================
# GENRE
# =========================


@pytest.mark.django_db
def test_genre_list(client):
    GenreFactory.create_batch(3)

    response = client.get('/api/genres/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_genre_detail(client):
    genre = GenreFactory()

    response = client.get(f'/api/genres/{genre.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_genre_update(client_admin):
    genre = GenreFactory()

    response = client_admin.put(
        f'/api/genres/{genre.pk}/',
        data={'name': 'New Genre'},
        content_type='application/json',
    )

    assert response.status_code == 200
    genre.refresh_from_db()
    assert genre.name == 'New Genre'


@pytest.mark.django_db
def test_genre_delete(client_admin):
    genre = GenreFactory()

    response = client_admin.delete(f'/api/genres/{genre.pk}/')

    assert response.status_code in (200, 204)
    assert not Genre.objects.filter(pk=genre.pk).exists()


# =========================
# DEVELOPER
# =========================


@pytest.mark.django_db
def test_developer_list(client):
    DeveloperFactory.create_batch(3)

    response = client.get('/api/developers/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_developer_detail(client):
    dev = DeveloperFactory()

    response = client.get(f'/api/developers/{dev.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_developer_update(client_admin):
    dev = DeveloperFactory()

    response = client_admin.put(
        f'/api/developers/{dev.pk}/',
        data={'name': 'New Dev'},
        content_type='application/json',
    )

    assert response.status_code == 200
    dev.refresh_from_db()
    assert dev.name == 'New Dev'


@pytest.mark.django_db
def test_developer_delete(client_admin):
    dev = DeveloperFactory()

    response = client_admin.delete(f'/api/developers/{dev.pk}/')

    assert response.status_code in (200, 204)
    assert not Developer.objects.filter(pk=dev.pk).exists()


# =========================
# PUBLISHER
# =========================


@pytest.mark.django_db
def test_publisher_list(client):
    PublisherFactory.create_batch(3)

    response = client.get('/api/publishers/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_publisher_detail(client):
    pub = PublisherFactory()

    response = client.get(f'/api/publishers/{pub.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_publisher_update(client_admin):
    pub = PublisherFactory()

    response = client_admin.put(
        f'/api/publishers/{pub.pk}/',
        data={'name': 'New Publisher'},
        content_type='application/json',
    )

    assert response.status_code == 200
    pub.refresh_from_db()
    assert pub.name == 'New Publisher'


@pytest.mark.django_db
def test_publisher_delete(client_admin):
    pub = PublisherFactory()

    response = client_admin.delete(f'/api/publishers/{pub.pk}/')

    assert response.status_code in (200, 204)
    assert not Publisher.objects.filter(pk=pub.pk).exists()


# =========================
# EDITION
# =========================


@pytest.mark.django_db
def test_edition_list(client):
    EditionFactory.create_batch(3)

    response = client.get('/api/editions/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_edition_create(client_admin):
    response = client_admin.post(
        '/api/editions/',
        data={'name': 'Special Edition', 'description': 'Test desc'},
        content_type='application/json',
    )

    assert response.status_code in (200, 201)
    assert Edition.objects.filter(name='Special Edition').exists()


@pytest.mark.django_db
def test_edition_update(client_admin):
    edition = EditionFactory()

    response = client_admin.put(
        f'/api/editions/{edition.pk}/',
        data={'name': 'Updated', 'description': 'Updated desc'},
        content_type='application/json',
    )

    assert response.status_code == 200
    edition.refresh_from_db()
    assert edition.name == 'Updated'


@pytest.mark.django_db
def test_edition_delete(client_admin):
    edition = EditionFactory()

    response = client_admin.delete(f'/api/editions/{edition.pk}/')

    assert response.status_code in (200, 204)
    assert not Edition.objects.filter(pk=edition.pk).exists()


# =========================
# REGION
# =========================


@pytest.mark.django_db
def test_region_list(client):
    RegionFactory.create_batch(3)

    response = client.get('/api/regions/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_region_detail(client):
    region = RegionFactory()

    response = client.get(f'/api/regions/{region.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_region_update(client_admin):
    region = RegionFactory()

    response = client_admin.put(
        f'/api/regions/{region.pk}/',
        data={'name': 'Europe', 'acronym': 'EU'},
        content_type='application/json',
    )

    assert response.status_code == 200
    region.refresh_from_db()
    assert region.name == 'Europe'
    assert region.acronym == 'EU'


@pytest.mark.django_db
def test_region_delete(client_admin):
    region = RegionFactory()

    response = client_admin.delete(f'/api/regions/{region.pk}/')

    assert response.status_code in (200, 204)
    assert not Region.objects.filter(pk=region.pk).exists()
