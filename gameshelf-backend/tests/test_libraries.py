import pytest
from django.db import IntegrityError
from django.utils import timezone

from libraries.models import LibraryItem
from tests.factories.classifications import PlatformFactory
from tests.factories.games import GameFactory
from tests.factories.libraries import LibraryFactory, LibraryItemFactory, UserFactory


@pytest.mark.django_db
def test_libraries_creation():
    library = LibraryFactory()

    assert library.pk is not None
    assert library.user is not None
    assert library.created_at is not None


@pytest.mark.django_db
def test_library_one_to_one_constraint():
    user = UserFactory()

    LibraryFactory(user=user)

    with pytest.raises(IntegrityError):
        LibraryFactory(user=user)


@pytest.mark.django_db
def test_library_str():
    library = LibraryFactory(is_private=True)

    s = str(library)

    assert 'Library' in s
    assert 'Private' in s


@pytest.mark.django_db
def test_library_privacy_flag():
    library = LibraryFactory(is_private=True)

    assert library.is_private is True


@pytest.mark.django_db
def test_library_item_creation():
    item = LibraryItemFactory()

    assert item.pk is not None
    assert item.library is not None
    assert item.game is not None
    assert item.platform is not None


@pytest.mark.django_db
def test_library_item_default_status():
    item = LibraryItemFactory()

    assert item.status == LibraryItem.Status.PLANNING


@pytest.mark.django_db
def test_library_item_all_statuses_valid():
    library = LibraryFactory()

    statuses = [
        LibraryItem.Status.COMPLETED,
        LibraryItem.Status.PLAYING,
        LibraryItem.Status.PAUSED,
        LibraryItem.Status.DROPPED,
        LibraryItem.Status.PLANNING,
    ]

    for status in statuses:
        item = LibraryItemFactory(library=library, status=status)
        assert item.status == status


@pytest.mark.django_db
def test_library_item_unique_constraint():
    library = LibraryFactory()
    game = GameFactory()
    platform = PlatformFactory()

    LibraryItemFactory(library=library, game=game, platform=platform)

    with pytest.raises(IntegrityError):
        LibraryItemFactory(library=library, game=game, platform=platform)


@pytest.mark.django_db
def test_library_item_same_game_different_platform_allowed():
    library = LibraryFactory()
    game = GameFactory()

    p1 = PlatformFactory()
    p2 = PlatformFactory()

    LibraryItemFactory(library=library, game=game, platform=p1)
    LibraryItemFactory(library=library, game=game, platform=p2)

    assert LibraryItem.objects.count() == 2


@pytest.mark.django_db
def test_library_item_hours_played():
    item = LibraryItemFactory(hours_played=12.5)

    assert float(item.hours_played) == 12.5


@pytest.mark.django_db
def test_library_item_soft_delete_allows_recreation():
    library = LibraryFactory()
    game = GameFactory()
    platform = PlatformFactory()

    item = LibraryItemFactory(
        library=library,
        game=game,
        platform=platform,
    )

    item.deleted_at = timezone.now()
    item.save()

    new_item = LibraryItemFactory(
        library=library,
        game=game,
        platform=platform,
    )

    assert new_item.pk is not None
    
@pytest.mark.django_db
def test_library_item_ordering():
    library = LibraryFactory()

    item1 = LibraryItemFactory(library=library)
    item2 = LibraryItemFactory(library=library)

    items = list(library.items.all().order_by('-created_at'))

    assert items[0].created_at >= items[1].created_at
