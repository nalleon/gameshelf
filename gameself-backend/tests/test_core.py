import uuid

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from classifications.models import Classification, Developer, Region, Publisher, Edition, Genre, Platform
from colecctions.models import Item, CollectionItem, WishListItem
from games.models import Game, Review, Media, FavoriteItem 

User = get_user_model()

# ==============================================================================
# Required Apps
# ==============================================================================


@pytest.mark.django_db
def test_required_apps_are_installed():
    REQUIRED_APPS = ('shared', 'classifications', 'colecctions', 'games', 'users')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in REQUIRED_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps, (
            f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
        )
    assert len(custom_apps) >= len(REQUIRED_APPS), (
        'El número de aplicaciones propias definidas en el proyecto no es correcto.'
    )


# ========================================================================================================================================================== #
#                                                         Classifications Models                                                                             #
# ========================================================================================================================================================== # 

# ==============================================================================
# Classification Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_classification_model_is_correctly_configured():
    
    # name
    assert (f := Classification._meta.get_field('name')), 'Classification.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Classification.name no tiene el tipo esperado'
    assert f.unique, 'Classification.name no se ha definido como único'
    assert not f.blank, 'Classification.name no debe admitir valores en blanco'

    # description
    assert (f := Classification._meta.get_field('description')), 'Classification.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Classification.description no tiene el tipo esperado'
    assert not f.blank, 'Classification.description no debe admitir valores en blanco'
    assert f.max_length == 160, 'Classification.description no tiene el valor esperado en max_length'

# ==============================================================================
# Edition Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_edition_model_is_correctly_configured():
    # name
    assert (f := Edition._meta.get_field('name')), 'Edition.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Edition.name no tiene el tipo esperado'
    assert f.unique, 'Edition.name no se ha definido como único'
    assert not f.blank, 'Edition.name no debe admitir valores en blanco'

    # description
    assert (f := Edition._meta.get_field('description')), 'Edition.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Edition.description no tiene el tipo esperado'
    assert not f.blank, 'Edition.description no debe admitir valores en blanco'
    assert f.max_length == 160, 'Edition.description no tiene el valor esperado en max_length'

# ==============================================================================
# Region Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_region_model_is_correctly_configured():
    # name
    assert (f := Region._meta.get_field('name')), 'Region.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Region.name no tiene el tipo esperado'
    assert f.unique, 'Region.name no se ha definido como único'
    assert not f.blank, 'Region.name no debe admitir valores en blanco'

    # acronym
    assert (f := Region._meta.get_field('acronym')), 'Region.acronym no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Region.acronym no tiene el tipo esperado'
    assert not f.blank, 'Region.acronym no debe admitir valores en blanco'
    assert f.max_length == 2, 'Region.acronym no tiene el valor esperado en max_length'
    
    # icon
    assert (f := Region._meta.get_field('icon')), 'Region.icon no se ha definido'
    assert f.get_internal_type() in ['FileField', 'ImageField'], (
        'Region.icon no tiene el tipo esperado'
    )
    assert f.upload_to == 'regions/', 'Region.icon no tiene la ruta de subida esperada'
    assert f.blank, 'Region.icon debe admitir valores en blanco'
    assert f.default == 'regions/default.png', (
        'Region.icon no tiene el valor por defecto esperado'
    )

# ==============================================================================
# Genre Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_genre_model_is_correctly_configured():
    # name
    assert (f := Genre._meta.get_field('name')), 'Genre.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Genre.name no tiene el tipo esperado'
    assert f.unique, 'Genre.name no se ha definido como único'
    assert not f.blank, 'Genre.name no debe admitir valores en blanco'

    # description
    assert (f := Genre._meta.get_field('description')), 'Genre.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Genre.description no tiene el tipo esperado'
    assert not f.blank, 'Genre.description no debe admitir valores en blanco'
    assert f.max_length == 160, 'Genre.description no tiene el valor esperado en max_length'

# ==============================================================================
# Developer Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_developer_model_is_correctly_configured():
    # name
    assert (f := Developer._meta.get_field('name')), 'Developer.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Developer.name no tiene el tipo esperado'
    assert f.unique, 'Developer.name no se ha definido como único'
    assert not f.blank, 'Developer.name no debe admitir valores en blanco'

    # description
    assert (f := Developer._meta.get_field('description')), 'Developer.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Developer.description no tiene el tipo esperado'
    assert not f.blank, 'Developer.description no debe admitir valores en blanco'
    assert f.max_length == 160, 'Developer.description no tiene el valor esperado en max_length'

# ==============================================================================
# Publisher Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_publisher_model_is_correctly_configured():
    # name
    assert (f := Publisher._meta.get_field('name')), 'Publisher.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Publisher.name no tiene el tipo esperado'
    assert f.unique, 'Publisher.name no se ha definido como único'
    assert not f.blank, 'Publisher.name no debe admitir valores en blanco'

    # description
    assert (f := Publisher._meta.get_field('description')), 'Publisher.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Publisher.description no tiene el tipo esperado'
    assert not f.blank, 'Publisher.description no debe admitir valores en blanco'
    assert f.max_length == 160, 'Publisher.description no tiene el valor esperado en max_length'

# ==============================================================================
# Platform Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_platform_model_is_correctly_configured():
    # name
    assert (f := Platform._meta.get_field('name')), 'Platform.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Platform.name no tiene el tipo esperado'
    assert f.unique, 'Platform.name no se ha definido como único'
    assert not f.blank, 'Platform.name no debe admitir valores en blanco'

    # description
    assert (f := Platform._meta.get_field('description')), 'Platform.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Platform.description no tiene el tipo esperado'
    assert not f.blank, 'Platform.description no debe admitir valores en blanco'
    assert f.max_length == 160, 'Platform.description no tiene el valor esperado en max_length'


# ========================================================================================================================================================== #
#                                                         Colecctions Models                                                                                 #
# ========================================================================================================================================================== # 

# ==============================================================================
# Item Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_item_model_is_correctly_configured():
    
    # type
    assert (f := Item._meta.get_field('type')), 'Item.type no se ha definido'
    assert f.get_internal_type() == 'CharField', (
        'Item.type no tiene el tipo esperado'
    )
    assert set(dict(f.choices).keys()) == set(['P', 'D']), (
        'Item.type no tiene las opciones esperadas'
    )
    assert not f.blank, 'Item.type no debe admitir valores en blanco'
    assert f.default == 'D', 'Item.type no tiene el valor por defecto esperado'


    # game
    assert (f := Item._meta.get_field('game')), 'Item.game no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Item.game no tiene el tipo esperado'
    assert f.remote_field.on_delete.__name__ == 'SET_NULL', (
        'Item.game no tiene el método de borrado esperado'
    )
    assert f.blank, 'Item.game debe admitir valores en blanco'


    # author
    assert (f := Item._meta.get_field('author')), 'Item.author no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Item.author no tiene el tipo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Item.author no tiene el método de borrado esperado'
    )
    assert not f.blank, 'Item.author no debe admitir valores en blanco'


    # created_at
    assert (f := Item._meta.get_field('created_at')), 'Item.created_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Item.created_at no tiene el tipo esperado'
    assert f.auto_now_add, 'Item.created_at no tiene auto_now_add activado'
    assert not f.auto_now, 'Item.created_at tiene auto_now activado pero no debería'


# ==============================================================================
# CollectionItem Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_collection_item_model_is_correctly_configured():

    # game
    assert (f := CollectionItem._meta.get_field('game')), 'CollectionItem.game no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'CollectionItem.game no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'game', (
        'CollectionItem.game no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'SET_NULL', (
        'CollectionItem.game no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'collection_items', 'CollectionItem.game no tiene el related_name esperado'
    assert f.blank, 'CollectionItem.game debe admitir valores en blanco'


    # author
    assert (f := CollectionItem._meta.get_field('author')), 'CollectionItem.author no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'CollectionItem.author no tiene el tipo esperado'
    assert f.related_model == User, 'CollectionItem.author no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'CollectionItem.author no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'collection', (
        'CollectionItem.author no tiene el related_name esperado'
    )
    assert not f.blank, 'CollectionItem.author no debe admitir valores en blanco'


# ==============================================================================
# WhishlistItem Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_wishlist_item_model_is_correctly_configured():

    # priority
    assert (f := WishListItem._meta.get_field('priority')), 'WishListItem.priority no se ha definido'
    assert f.get_internal_type() == 'PositiveSmallIntegerField', 'WishListItem.priority no tiene el tipo esperado'
    assert not f.blank, 'WishListItem.priority no debe admitir valores en blanco'
    validators = {v.__class__.__name__: v for v in f.validators}
    assert 'MinValueValidator' in validators, (
        'WishListItem.priority no tiene un validador para el valor mínimo'
    )
    assert validators['MinValueValidator'].limit_value == 1, (
        'WishListItem.priority no tiene el valor mínimo esperado'
    )
    assert 'MaxValueValidator' in validators, (
        'WishListItem.priority no tiene un validador para el valor máximo'
    )
    assert validators['MaxValueValidator'].limit_value == 10, (
        'WishListItem.priority no tiene el valor máximo esperado'
    )
    assert f.default == 5 , 'WishListItem.priority no tiene el valor por defecto esperado'


    # annotation
    assert (f := WishListItem._meta.get_field('annotation')), 'WishListItem.annotation no se ha definido'
    assert f.get_internal_type() == 'CharField', 'WishListItem.annotation no tiene el tipo esperado'
    assert not f.blank, 'WishListItem.annotation no debe admitir valores en blanco'
    assert f.max_length == 100, 'WishListItem.annotation no tiene el valor esperado en max_length'


    # game
    assert (f := WishListItem._meta.get_field('game')), 'WishListItem.game no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'WishListItem.game no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'game', (
        'WishListItem.game no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'SET_NULL', (
        'WishListItem.game no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'wishlist_items', 'WishListItem.game no tiene el related_name esperado'
    assert f.blank, 'WishListItem.game debe admitir valores en blanco'


    # author
    assert (f := WishListItem._meta.get_field('author')), 'WishListItem.author no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'WishListItem.author no tiene el tipo esperado'
    assert f.related_model == User, 'WishListItem.author no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'CollectWishListItemionItem.author no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'wishlist', (
        'WishListItem.author no tiene el related_name esperado'
    )
    assert not f.blank, 'WishListItem.author no debe admitir valores en blanco'


# ========================================================================================================================================================== #
#                                                               Games Models                                                                                 #
# ========================================================================================================================================================== # 


# ==============================================================================
# Game Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_game_model_is_correctly_configured():

    # title
    assert (f := Game._meta.get_field('title')), 'Game.title no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Game.title no tiene el tipo esperado'
    assert not f.blank, 'Game.name no debe admitir valores en blanco'

    # slug
    assert (f := Game._meta.get_field('slug')), 'Game.slug no se ha definido'
    assert f.get_internal_type() == 'SlugField', 'Game.slug no tiene el tipo esperado'
    assert f.unique, 'Game.slug no se ha definido como único'
    assert not f.blank, 'Game.slug no debe admitir valores en blanco'

    # released_at
    assert (f := Game._meta.get_field('released_at')), 'Game.released_at no se ha definido'
    assert f.get_internal_type() == 'DateField', 'Game.released_at no tiene el tipo esperado'
    assert not f.auto_now_add, 'Game.released_at tiene auto_now_add activado pero no debería'
    assert not f.auto_now, 'Game.released_at tiene auto_now activado pero no debería'

    # platforms
    assert (f := Game._meta.get_field('platforms')), 'Game.platforms no se ha definido'
    assert f.get_internal_type() == 'ManyToManyField', 'Game.platforms no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'platform', (
        'Game.platforms no referencia al modelo esperado'
    )
    assert f.remote_field.related_name == 'games', (
        'Game.platforms no tiene el related_name esperado'
    )
    assert not f.blank, 'Game.platforms no debe admitir valores en blanco'

    # genres
    assert (f := Game._meta.get_field('genres')), 'Game.genres no se ha definido'
    assert f.get_internal_type() == 'ManyToManyField', 'Game.genres no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'genre', (
        'Game.genres no referencia al modelo esperado'
    )
    assert f.remote_field.related_name == 'games', (
        'Game.genres no tiene el related_name esperado'
    )
    assert not f.blank, 'Game.genres no debe admitir valores en blanco'

    # developers
    assert (f := Game._meta.get_field('developers')), 'Game.developers no se ha definido'
    assert f.get_internal_type() == 'ManyToManyField', 'Game.developers no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'developer', (
        'Game.developers no referencia al modelo esperado'
    )
    assert f.remote_field.related_name == 'games', (
        'Game.developers no tiene el related_name esperado'
    )
    assert not f.blank, 'Game.developers no debe admitir valores en blanco'

    # publishers
    assert (f := Game._meta.get_field('publishers')), 'Game.publishers no se ha definido'
    assert f.get_internal_type() == 'ManyToManyField', 'Game.publishers no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'publisher', (
        'Game.publishers no referencia al modelo esperado'
    )
    assert f.remote_field.related_name == 'games', (
        'Game.publishers no tiene el related_name esperado'
    )
    assert not f.blank, 'Game.publishers no debe admitir valores en blanco'

    # edition
    assert (f := Game._meta.get_field('edition')), 'Game.edition no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Game.edition no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'edition', (
        'Game.edition no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'SET_NULL', (
        'Game.edition no tiene el método de borrado esperado'
    )
    assert f.blank, 'Game.edition debe admitir valores en blanco'

    # region
    assert (f := Game._meta.get_field('region')), 'Game.region no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Game.region no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'region', (
        'Game.region no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'SET_NULL', (
        'Game.region no tiene el método de borrado esperado'
    )
    assert f.blank, 'Game.region debe admitir valores en blanco'


# ==============================================================================
# Review Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_review_model_is_correctly_configured():

    # content
    assert (f := Review._meta.get_field('content')), 'Review.content no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Review.content no tiene el tipo esperado'
    assert not f.blank, 'Review.content no debe admitir valores en blanco'


    # recommend
    assert (f := Review._meta.get_field('recommend')), 'Review.recommend no se ha definido'
    assert f.get_internal_type() == 'BooleanField', 'Review.recommend no tiene el tipo esperado'
    assert not f.blank, 'Review.recommend no debe admitir valores en blanco'


    # game
    assert (f := Review._meta.get_field('game')), 'Review.game no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Review.game no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'game', (
        'Review.game no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Review.game no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'reviews', 'Review.game no tiene el related_name esperado'
    assert not f.blank, 'Review.game no debe admitir valores en blanco'


    # author
    assert (f := Review._meta.get_field('author')), 'Review.author no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Review.author no tiene el tipo esperado'
    assert f.related_model == User, 'Review.author no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Review.author no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'reviews', (
        'Review.author no tiene el related_name esperado'
    )
    assert not f.blank, 'Review.author no debe admitir valores en blanco'

    # created_at
    assert (f := Review._meta.get_field('created_at')), 'Review.created_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Review.created_at no tiene el tipo esperado'
    assert f.auto_now_add, 'Review.created_at no tiene auto_now_add activado'
    assert not f.auto_now, 'Review.created_at tiene auto_now activado pero no debería'


    # updated_at
    assert (f := Review._meta.get_field('updated_at')), 'Review.updated_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Review.updated_at no tiene el tipo esperado'
    assert not f.auto_now_add, 'Review.updated_at tiene auto_now_add activado pero no debería'
    assert f.auto_now, 'Review.updated_at no tiene auto_now activado'


# ==============================================================================
# Media Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_media_model_is_correctly_configured():

    # image
    assert (f := Media._meta.get_field('image')), 'Media.image no se ha definido'
    assert f.get_internal_type() in ['FileField', 'ImageField'], (
        'Media.image no tiene el tipo esperado'
    )
    assert f.upload_to == 'reviews/', 'Media.image no tiene la ruta de subida esperada'
    assert f.blank, 'Media.image debe admitir valores en blanco'
    assert f.default == 'reviews/default.png', (
        'Media.image no tiene el valor por defecto esperado'
    )


    # review
    assert (f := Media._meta.get_field('review')), 'Media.review no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Media.review no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'review', (
        'Media.review no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Media.review no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'medias', (
        'Media.review no tiene el related_name esperado'
    )
    assert not f.blank, 'Media.review no debe admitir valores en blanco'


# ==============================================================================
# FavoriteItem Model
# ==============================================================================

@pytest.mark.score(2)
@pytest.mark.django_db
def test_favorite_item_model_is_correctly_configured():

    # game
    assert (f := FavoriteItem._meta.get_field('game')), 'FavoriteItem.game no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'FavoriteItem.game no tiene el tipo esperado'
    assert f.related_model._meta.model_name == 'game', (
        'FavoriteItem.game no referencia al modelo esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'FavoriteItem.game no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'favorites', 'FavoriteItem.game no tiene el related_name esperado'
    assert not f.blank, 'FavoriteItem.game no debe admitir valores en blanco'


    # user
    assert (f := FavoriteItem._meta.get_field('user')), 'FavoriteItem.user no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'FavoriteItem.user no tiene el tipo esperado'
    assert f.related_model == User, 'FavoriteItem.user no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'FavoriteItem.user no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'favorites', (
        'FavoriteItem.user no tiene el related_name esperado'
    )
    assert not f.blank, 'FavoriteItem.user no debe admitir valores en blanco'