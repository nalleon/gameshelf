import pytest

from classifications.models import Platform
from game_collections.models import Wishlist
from tests.factories.game_collections import (
    CollectionFactory,
    CollectionItemFactory,
    UserFactory,
    WishListItemFactory,
)
from tests.factories.games import GameFactory

# -------------------------
# COLLECTION TESTS
# -------------------------


@pytest.mark.django_db
def test_collection_list_public(client):
    CollectionFactory(is_private=False)
    CollectionFactory(is_private=True)

    response = client.get('/api/collections/')

    assert response.status_code == 200
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_collection_list_authenticated(client_admin):
    CollectionFactory(is_private=True, user=client_admin.user)
    CollectionFactory(is_private=False)

    response = client_admin.get('/api/collections/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_collection(client_admin):
    payload = {
        'name': 'My Collection',
        'is_private': False,
    }

    response = client_admin.post('/api/collections/', payload, format='json')

    assert response.status_code == 201
    assert response.data['name'] == 'My Collection'


# -------------------------
# COLLECTION ITEMS
# -------------------------


@pytest.mark.django_db
def test_get_collection_item(client_admin):
    collection = CollectionFactory(user=client_admin.user)
    item = CollectionItemFactory(collection=collection)

    response = client_admin.get(f'/api/collections/{collection.pk}/items/{item.pk}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_collection_item(client_admin):
    collection = CollectionFactory(user=client_admin.user)
    game = GameFactory()
    platform = Platform.objects.first() or Platform.objects.create(name='PC')

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'type': 'P',
        'is_private': True
    }

    response = client_admin.post(
        f'/api/collections/{collection.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_add_collection_item_forbidden(client):
    user = UserFactory()
    collection = CollectionFactory(user=user)
    game = GameFactory()
    platform = Platform.objects.first() or Platform.objects.create(name='PC')

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'is_private': False,
        'type': 'P',
    }

    response = client.post(
        f'/api/collections/{collection.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 401
    
@pytest.mark.django_db
def test_add_collection_item_forbidden_other_user():
    owner = UserFactory()

    other_user = UserFactory()

    collection = CollectionFactory(user=owner)
    game = GameFactory()
    platform = Platform.objects.first() or Platform.objects.create(name='PC')

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'is_private': False,
        'type': 'P',
    }

    from rest_framework.test import APIClient

    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.post(
        f'/api/collections/{collection.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_collection_item(client_admin):
    collection = CollectionFactory(user=client_admin.user)
    item = CollectionItemFactory(collection=collection)

    response = client_admin.delete(f'/api/collections/{collection.pk}/items/{item.pk}/')

    assert response.status_code == 204


@pytest.mark.django_db
def test_edit_collection_item(client_admin):
    collection = CollectionFactory(user=client_admin.user)
    item = CollectionItemFactory(collection=collection)

    platform = Platform.objects.first() or Platform.objects.create(name="PC")

    payload = {
        'is_private': True,
        'type': 'P',
        'platform_id': platform.pk,
    }

    response = client_admin.patch(
        f'/api/collections/{collection.pk}/items/{item.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 200


# -------------------------
# WISHLIST TESTS
# -------------------------


@pytest.mark.django_db
def test_get_own_wishlist(client_admin):
    wishlist = getattr(client_admin.user, 'wishlist', None)
    if not wishlist:
        wishlist = Wishlist.objects.create(user=client_admin.user)

    response = client_admin.get('/api/wishlist/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_wishlist_detail(client_admin):
    wishlist = getattr(client_admin.user, 'wishlist', None)
    if not wishlist:
        wishlist = Wishlist.objects.create(user=client_admin.user)

    response = client_admin.get(f'/api/wishlist/{wishlist.pk}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_wishlist_item(client_admin):
    wishlist = getattr(client_admin.user, 'wishlist', None)
    if not wishlist:
        wishlist = Wishlist.objects.create(user=client_admin.user)

    game = GameFactory()
    platform = Platform.objects.first() or Platform.objects.create(name='PC')

    payload = {
        'game_id': game.pk,
        'platform_id': platform.pk,
        'priority': 1,
        'annotation': 'test',
        'type': 'P',
        'is_private': True
    }

    response = client_admin.post(
        f'/api/wishlist/{wishlist.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_delete_wishlist_item(client_admin):
    wishlist = getattr(client_admin.user, 'wishlist', None)
    if not wishlist:
        wishlist = Wishlist.objects.create(user=client_admin.user)

    item = WishListItemFactory(wishlist=wishlist)

    response = client_admin.delete(f'/api/wishlist/items/{item.pk}/')

    assert response.status_code == 204


@pytest.mark.django_db
def test_edit_wishlist_item(client_admin):
    wishlist = getattr(client_admin.user, 'wishlist', None)
    if not wishlist:
        wishlist = Wishlist.objects.create(user=client_admin.user)

    item = WishListItemFactory(wishlist=wishlist)
    platform = Platform.objects.first() or Platform.objects.create(name='PC')

    payload = {
        'priority': 2,
        'annotation': 'updated',
        'is_private': False,
        'type': 'P',
        'platform_id': platform.pk,

    }

    response = client_admin.patch(
        f'/api/wishlist/items/{item.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 200
