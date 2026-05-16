import pytest

from tests.factories.games import (
    FavoriteItemFactory,
    GameFactory,
    PlatformFactory,
    ReviewFactory,
)

# -------------------------
# GAMES
# -------------------------


@pytest.mark.django_db
def test_game_list(client):
    GameFactory.create_batch(5, mature_content=False)

    response = client.get('/api/games/')

    assert response.status_code == 200
    assert 'results' in response.json()


@pytest.mark.django_db
def test_game_list_mature_filter(client):
    GameFactory(mature_content=True)
    GameFactory(mature_content=False)

    response = client.get('/api/games/?mature_content=false')

    data = response.json()
    assert all(not g['mature_content'] for g in data['results'])


@pytest.mark.django_db
def test_game_detail(client):
    game = GameFactory()

    response = client.get(f'/api/games/{game.pk}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_game_detail_not_found(client):
    response = client.get('/api/games/9999/')

    assert response.status_code == 404
    assert response.json()['error'] == 'Game not found'


@pytest.mark.django_db
def test_edit_game_admin(client_admin):
    game = GameFactory()

    payload = {
        'title': 'New title',
        'slug': 'new-slug',
        'description': 'desc',
        'cover_default': 'url',
        'released_at': '2020-01-01',
        'pk_platforms_list': [],
        'pk_genres_list': [],
        'pk_developers_list': [],
        'pk_publishers_list': [],
        'pk_edition': None,
        'pk_region': None,
    }

    response = client_admin.put(f'/api/games/{game.pk}/', payload, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_game_not_found(client_admin):
    response = client_admin.put('/api/games/999/', {}, format='json')

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_game(client_admin):
    game = GameFactory()

    response = client_admin.delete(f'/api/games/{game.pk}/')

    assert response.status_code == 204


# -------------------------
# FAVORITES
# -------------------------


@pytest.mark.django_db
def test_add_favorite_limit(client_admin, admin_user):
    FavoriteItemFactory.create_batch(10, user=admin_user)

    game = GameFactory()
    platform = PlatformFactory()

    response = client_admin.post(
        '/api/favorites/toggle/',
        {'pk_game': game.pk, 'pk_platform': platform.pk},
        format='json'
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Maximum number of favorites reached'


@pytest.mark.django_db
def test_favorite_list(client_admin, admin_user):
    FavoriteItemFactory.create_batch(3, user=admin_user)

    response = client_admin.get(f'/api/favorites/user/{admin_user.pk}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_favorite(client_admin):
    game = GameFactory()
    platform = PlatformFactory()

    payload = {
        'pk_game': game.pk,
        'pk_platform': platform.pk,
    }

    response = client_admin.post(
        '/api/favorites/toggle/',
        payload,
        format='json'
    )

    assert response.status_code in [200, 201]


@pytest.mark.django_db
def test_add_favorite_duplicate(client_admin, admin_user):
    game = GameFactory()
    platform = PlatformFactory()

    FavoriteItemFactory(
        user=admin_user,
        game=game,
        platform=platform,
    )

    payload = {
        'pk_game': game.pk,
        'pk_platform': platform.pk,
    }

    response = client_admin.post(
        '/api/favorites/toggle/',
        payload,
        format='json'
    )

    assert response.status_code in [200, 204]


@pytest.mark.django_db
def test_add_favorite_game_not_found(client_admin):
    platform = PlatformFactory()

    response = client_admin.post(
        '/api/favorites/toggle/',
        {'pk_game': 999, 'pk_platform': platform.pk},
        format='json',
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_favorite(client_admin):
    user = client_admin.user
    platform = PlatformFactory()

    fav = FavoriteItemFactory(
        user=user,
        platform=platform,
        order=1,
    )

    payload = {
        'order': 2,
        'pk_platform': platform.pk,
    }

    response = client_admin.patch(
        f'/api/favorites/{fav.pk}/',
        payload,
        format='json',
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_favorite(client_admin):
    user = client_admin.user

    fav = FavoriteItemFactory(user=user)

    response = client_admin.delete(
        f'/api/favorites/{fav.pk}/'
    )

    assert response.status_code == 204


# -------------------------
# REVIEWS
# -------------------------


@pytest.mark.django_db
def test_review_list(client):
    ReviewFactory.create_batch(3)

    response = client.get('/api/reviews/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_review(client_admin):
    game = GameFactory()

    payload = {
        'content': 'Nice',
        'recommend': True,
        'game_id': game.pk,
    }

    response = client_admin.post('/api/reviews/', payload, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_review_game_not_found(client_admin):
    response = client_admin.post(
        '/api/reviews/',
        {'content': 'x', 'recommend': True, 'game_id': 999},
        format='json',
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_review_detail_not_found(client):
    response = client.get('/api/reviews/999/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_review_ok(client_admin, admin_user):
    review = ReviewFactory(author=admin_user)

    response = client_admin.delete(f'/api/reviews/{review.pk}/')

    assert response.status_code == 204