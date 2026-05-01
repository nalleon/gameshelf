import pytest
from django.db import IntegrityError
from django.utils.text import slugify

from games.models import FavoriteItem, Game

from tests.factories.games import FavoriteItemFactory, GameFactory, MediaFactory, ReviewFactory


# @pytest.mark.django_db
# class TestGameModel:
#     def test_game_creation(self):
#         game = GameFactory(title='Super Mario')
#         assert game.id is not None
#         assert 'Super Mario' in str(game)
#         assert game.slug == slugify('Super Mario')

#     def test_game_slug_uniqueness_with_year(self):
#         game1 = GameFactory(title='Zelda', released_at='2023-01-01')
#         game2 = GameFactory(title='Zelda', released_at='2024-01-01')

#         assert game1.slug == 'zelda'
#         assert game2.slug == 'zelda-2024'

#     def test_game_slug_collision_incremental(self):
#         game1 = GameFactory(title='Sonic', released_at='2020-01-01')
#         game2 = Game(title='Sonic', released_at='2020-01-01', igdb_id=99)
#         game2.save()

#         assert game1.slug == 'sonic'
#         assert game2.slug == 'sonic-2020-1'

#     def test_game_unique_together_constraint(self):
#         game = GameFactory()
#         with pytest.raises(IntegrityError):
#             Game.objects.create(
#                 title=game.title, released_at=game.released_at, region=game.region, igdb_id=123
#             )


# @pytest.mark.django_db
# class TestReviewModel:
#     def test_review_creation_and_str(self):
#         review = ReviewFactory(content='Excelente juego')
#         assert review.id is not None
#         assert 'Excelente juego' in str(review)
#         assert review.game.reviews.count() == 1


# @pytest.mark.django_db
# class TestMediaModel:
#     def test_media_creation_and_str(self):
#         media = MediaFactory()
#         assert media.id is not None
#         assert f'Media(id={media.pk}' in str(media)
#         assert media.review.media_items.count() == 1


# @pytest.mark.django_db
# class TestFavoriteItemModel:
#     def test_favorite_creation_and_str(self):
#         fav = FavoriteItemFactory()
#         assert fav.id is not None
#         assert f'game="{fav.game}"' in str(fav)

#     def test_favorite_unique_user_game(self):
#         fav = FavoriteItemFactory()
#         with pytest.raises(IntegrityError):
#             FavoriteItem.objects.create(user=fav.user, game=fav.game)

#     def test_favorite_ordering(self):
#         fav1 = FavoriteItemFactory(order=2)
#         fav2 = FavoriteItemFactory(order=1)
#         favorites = FavoriteItem.objects.all()
#         assert favorites[0] == fav2
#         assert favorites[1] == fav1
