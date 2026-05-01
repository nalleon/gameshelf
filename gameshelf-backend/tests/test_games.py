from datetime import date

import pytest
from django.db import IntegrityError

from tests.factories.classifications import RegionFactory
from tests.factories.games import (
    FavoriteItemFactory,
    GameFactory,
    MediaFactory,
    ReviewFactory,
    UserFactory,
)

# -------------------------
# GAME
# -------------------------


@pytest.mark.django_db
def test_game_slug_is_generated():
    game = GameFactory(title='The Last of Us')

    assert game.slug == 'the-last-of-us'


@pytest.mark.django_db
def test_game_slug_with_same_title_uses_year():
    region = RegionFactory()

    g1 = GameFactory(title='Halo', released_at=date(2020, 1, 1), region=region)
    g2 = GameFactory(title='Halo', released_at=date(2021, 1, 1), region=region)
    assert g1.slug == 'halo'
    assert g2.slug.startswith('halo-2021')


@pytest.mark.django_db
def test_game_slug_collision_increments():
    region = RegionFactory()

    g1 = GameFactory(title='Halo', released_at=date(2020, 1, 1), region=region)
    g2 = GameFactory(title='Halo', released_at=date(2021, 1, 1), region=region)

    assert g2.slug == 'halo-2021'
    assert g2.slug != g1.slug


@pytest.mark.django_db
def test_game_str_contains_fields():
    game = GameFactory(title='Zelda')

    s = str(game)

    assert str(game.pk) in s
    assert 'Zelda' in s
    assert game.slug in s


@pytest.mark.django_db
def test_game_unique_together():
    region = RegionFactory()

    GameFactory(title='FIFA', released_at=date(2022, 1, 1), region=region)

    with pytest.raises(IntegrityError):
        GameFactory(title='FIFA', released_at=date(2022, 1, 1), region=region)


@pytest.mark.django_db
def test_game_relationships_are_created():
    game = GameFactory()

    assert game.platforms.count() > 0
    assert game.genres.count() > 0
    assert game.developers.count() > 0
    assert game.publishers.count() > 0


# -------------------------
# REVIEW
# -------------------------


@pytest.mark.django_db
def test_review_creation():
    review = ReviewFactory()

    assert review.pk is not None
    assert review.game is not None
    assert review.author is not None


@pytest.mark.django_db
def test_review_str():
    review = ReviewFactory()

    s = str(review)

    assert str(review.pk) in s
    assert review.content[:10] in s


@pytest.mark.django_db
def test_review_timestamps():
    review = ReviewFactory()

    assert review.created_at is not None
    assert review.updated_at is not None


# -------------------------
# MEDIA
# -------------------------


@pytest.mark.django_db
def test_media_creation():
    media = MediaFactory()

    assert media.pk is not None
    assert media.review is not None


@pytest.mark.django_db
def test_media_str():
    media = MediaFactory()

    s = str(media)

    assert str(media.pk) in s
    assert str(media.review.pk) in s


# -------------------------
# FAVORITE
# -------------------------


@pytest.mark.django_db
def test_favorite_item_creation():
    fav = FavoriteItemFactory()

    assert fav.pk is not None
    assert fav.user is not None
    assert fav.game is not None


@pytest.mark.django_db
def test_favorite_unique_constraint():
    user = UserFactory()
    game = GameFactory()

    FavoriteItemFactory(user=user, game=game)

    with pytest.raises(IntegrityError):
        FavoriteItemFactory(user=user, game=game)


@pytest.mark.django_db
def test_favorite_ordering():
    user = UserFactory()

    f1 = FavoriteItemFactory(user=user, order=2)
    f2 = FavoriteItemFactory(user=user, order=1)

    favorites = list(user.favorites.all())

    assert favorites[0].order == 1
    assert favorites[1].order == 2


@pytest.mark.django_db
def test_favorite_str():
    fav = FavoriteItemFactory()

    s = str(fav)

    assert str(fav.pk) in s
    assert str(fav.game.pk) in s
    assert str(fav.user.pk) in s
