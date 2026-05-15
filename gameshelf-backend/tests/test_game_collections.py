import pytest
from django.db import IntegrityError
from django.utils import timezone

from game_collections.models import CollectionItem
from tests.factories.game_collections import (
    CollectionFactory,
    CollectionItemFactory,
    UserFactory,
    WishlistFactory,
    WishListItemFactory,
)

from tests.factories.classifications import PlatformFactory

from tests.factories.games import GameFactory


@pytest.mark.django_db
def test_collection_creation():
    collection = CollectionFactory()

    assert collection.pk is not None
    assert collection.user is not None
    assert collection.name


@pytest.mark.django_db
def test_collection_str_and_fields():
    collection = CollectionFactory(name='My Games')

    assert 'My Games' in collection.name
    assert collection.user is not None


@pytest.mark.django_db
def test_collection_unique_name_case_insensitive():
    user = UserFactory()

    CollectionFactory(user=user, name='Favorites')

    with pytest.raises(IntegrityError):
        CollectionFactory(user=user, name='favorites')


@pytest.mark.django_db
def test_collection_item_creation():
    item = CollectionItemFactory()

    assert item.pk is not None
    assert item.collection is not None
    assert item.game is not None
    assert item.platform is not None


@pytest.mark.django_db
def test_collection_item_unique_constraint():
    collection = CollectionFactory()
    game = GameFactory()
    platform = PlatformFactory()

    CollectionItemFactory(
        collection=collection,
        game=game,
        platform=platform,
        type='D'
    )

    with pytest.raises(IntegrityError):
        CollectionItemFactory(
            collection=collection,
            game=game,
            platform=platform,
            type='D'
        )


@pytest.mark.django_db
def test_collection_item_different_types_allowed():
    collection = CollectionFactory()
    game = GameFactory()

    CollectionItemFactory(collection=collection, game=game, type='D')
    CollectionItemFactory(collection=collection, game=game, type='P')

    assert CollectionItem.objects.count() == 2


@pytest.mark.django_db
def test_wishlist_creation():
    wishlist = WishlistFactory()

    assert wishlist.pk is not None
    assert wishlist.user is not None


@pytest.mark.django_db
def test_wishlist_one_to_one():
    user = UserFactory()

    WishlistFactory(user=user)

    with pytest.raises(IntegrityError):
        WishlistFactory(user=user)


@pytest.mark.django_db
def test_wishlist_item_creation():
    item = WishListItemFactory()

    assert item.pk is not None
    assert item.wishlist is not None


@pytest.mark.django_db
def test_wishlist_item_priority_range():
    item = WishListItemFactory(priority=5)

    assert 1 <= item.priority <= 10


@pytest.mark.django_db
def test_wishlist_item_unique_constraint():
    wishlist = WishlistFactory()
    game = GameFactory()
    platform = PlatformFactory()

    WishListItemFactory(
        wishlist=wishlist,
        game=game,
        platform=platform,
        type='D'
    )

    with pytest.raises(IntegrityError):
        WishListItemFactory(
            wishlist=wishlist,
            game=game,
            platform=platform,
            type='D'
        )

@pytest.mark.django_db
def test_wishlist_item_null_game_allowed():
    item = WishListItemFactory(game=None)

    assert item.game is None


@pytest.mark.django_db
def test_soft_delete_does_not_block_creation():
    user = UserFactory()

    c1 = CollectionFactory(user=user, name='Games')
    c1.deleted_at = timezone.now()
    c1.save()

    c2 = CollectionFactory(user=user, name='Games')

    assert c2.pk is not None
