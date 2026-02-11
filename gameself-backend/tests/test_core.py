import uuid

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from classifications.models import Classification, Developer, Region, Publisher, Edition, Genre, Platform
from colecctions.models import Item, CollectionItem, WishListItem

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
    assert (f := CollectionItem._meta.get_field('author')), 'CollectionItem.author no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'CollectionItem.author no tiene el tipo esperado'
    assert f.related_model == User, 'CollectionItem.author no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'CollectionItem.author no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'wishlist', (
        'CollectionItem.author no tiene el related_name esperado'
    )
    assert not f.blank, 'CollectionItem.author no debe admitir valores en blanco'