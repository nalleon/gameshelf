from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.decorators import api_view

from classifications.models import Developer, Edition, Genre, Platform, Publisher, Region
from shared.decorators import require_fields, require_http_methods, require_json_body, require_role
from users.decorators import auth_required

from .models import FavoriteItem, Game, Media, Review
from .serializers import (
    FavoriteItemSerializer,
    FavoriteSchemaSerializer,
    GameSchemaSerializer,
    GameSerializer,
    MediaSchemaSerializer,
    MediaSerializer,
    ReviewSchemaSerializer,
    ReviewSerializer,
)

User = get_user_model()


# Games Methods
@extend_schema(
    responses={200: GameSchemaSerializer, 404: None},
    description='Get all games',
    operation_id='get_games',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: GameSchemaSerializer, 404: None},
    description='Get details of a specific game',
    operation_id='get_game_detail',
    parameters=[
        OpenApiParameter(
            name='pk_game',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the game to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def game_detail(request, pk_game: int):
    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


@extend_schema(
    request=GameSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Create a new game',
    operation_id='add_game',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields(
    'title',
    'slug',
    'description',
    'cover',
    'released_at',
    'pk_platforms_list',
    'pk_genres_list',
    'pk_developers_list',
    'pk_publishers_list',
    'pk_edition',
    'pk_region',
)
@auth_required
@require_role('Admin')
def add_game(request):
    payload = request.json
    title = payload['title']
    slug = payload['slug']
    description = payload['description']
    cover = payload['cover']
    released_at = payload['released_at']
    pk_platforms_list = payload['pk_platforms_list']
    pk_genres_list = payload['pk_genres_list']
    pk_developers_list = payload['pk_developers_list']
    pk_publishers_list = payload['pk_publishers_list']
    pk_edition = payload['pk_edition']
    pk_region = payload['pk_region']

    platforms = []
    for pk_platform in pk_platforms_list:
        try:
            platform = get_object_or_404(Platform, pk_platform)
        except Http404:
            return JsonResponse({'error': 'Platform associated not found'}, status=404)

        platforms.append(platform)

    genres = []
    for pk_genre in pk_genres_list:
        try:
            genre = get_object_or_404(Genre, pk_genre)
        except Http404:
            return JsonResponse({'error': 'Genre associated not found'}, status=404)

        genres.append(genre)

    developers = []
    for pk_developer in pk_developers_list:
        try:
            developer = get_object_or_404(Developer, pk_developer)
        except Http404:
            return JsonResponse({'error': 'Developer associated not found'}, status=404)

        developers.append(developer)

    publishers = []
    for pk_publisher in pk_publishers_list:
        try:
            publisher = get_object_or_404(Publisher, pk_publisher)
        except Http404:
            return JsonResponse({'error': 'Publisher associated not found'}, status=404)

        publishers.append(publisher)

    try:
        edition = get_object_or_404(Edition, pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition associated not found'}, status=404)

    try:
        region = get_object_or_404(Region, pk_region)
    except Http404:
        return JsonResponse({'error': 'Region associated not found'}, status=404)

    game = Game.objects.create(
        title=title,
        slug=slug,
        description=description,
        cover=cover,
        released_at=released_at,
        platforms=platforms,
        genres=genres,
        developers=developers,
        publishers=publishers,
        edition=edition,
        region=region,
    )

    return JsonResponse({'id': game.pk}, status=200)


@extend_schema(
    request=GameSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Update an existing game',
    operation_id='update_game',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_game',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the game to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role('Admin')
def edit_game(request, pk_game: int):
    payload = request.json
    title = payload['title']
    slug = payload['slug']
    description = payload['description']
    cover = payload['cover']
    released_at = payload['released_at']
    pk_platforms_list = payload['pk_platforms_list']
    pk_genres_list = payload['pk_genres_list']
    pk_developers_list = payload['pk_developers_list']
    pk_publishers_list = payload['pk_publishers_list']
    pk_edition = payload['pk_edition']
    pk_region = payload['pk_region']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    if title:
        game.title = title

    if slug:
        game.slug = slug

    if description:
        game.description = description

    if cover:
        game.cover = cover

    if released_at:
        game.released_at = released_at

    if pk_platforms_list:
        platforms = []
        for pk_platform in pk_platforms_list:
            try:
                platform = get_object_or_404(Platform, pk_platform)
            except Http404:
                return JsonResponse({'error': 'Platform to associate not found'}, status=404)
            platforms.append(platform)

        game.platforms = platforms

    if pk_genres_list:
        genres = []
        for pk_genre in pk_genres_list:
            try:
                genre = get_object_or_404(Genre, pk_genre)
            except Http404:
                return JsonResponse({'error': 'Genre to associate not found'}, status=404)
            genres.append(genre)

        game.genres = genres

    if pk_developers_list:
        developers = []
        for pk_developer in pk_developers_list:
            try:
                developer = get_object_or_404(Developer, pk_developer)
            except Http404:
                return JsonResponse({'error': 'Developer to associate not found'}, status=404)
            developers.append(developer)

        game.developers = developers

    if pk_publishers_list:
        publishers = []
        for pk_publisher in pk_publishers_list:
            try:
                publisher = get_object_or_404(Publisher, pk_publisher)
            except Http404:
                return JsonResponse({'error': 'Publisher to associate not found'}, status=404)

            publishers.append(publisher)

        game.publishers = publishers

    if pk_edition:
        try:
            edition = get_object_or_404(Edition, pk_edition)
        except Http404:
            return JsonResponse({'error': 'Edition to associate not found'}, status=404)

        game.edition = edition

    if pk_region:
        try:
            region = get_object_or_404(Region, pk_region)
        except Http404:
            return JsonResponse({'error': 'Region to associate not found'}, status=404)

        game.region = region

    game.save()
    return JsonResponse({'id': game.pk}, status=200)


@extend_schema(
    responses={
        200: None,
        404: None,
    },
    description='Delete an existing game',
    operation_id='delete_game',
    parameters=[
        OpenApiParameter(
            name='pk_game',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the game to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
@require_role('Admin')
def delete_game(request, pk_game: int):

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    game.delete()
    return JsonResponse(status=200)


# Reviews Methods


@extend_schema(
    responses={200: ReviewSchemaSerializer, 404: None},
    description='Get all reviews',
    operation_id='get_reviews',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: ReviewSchemaSerializer, 404: None},
    description='Get all reviews',
    operation_id='get_review_detail',
    parameters=[
        OpenApiParameter(
            name='pk_review',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the review to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def review_detail(request, pk_review: int):
    try:
        review = get_object_or_404(Review, pk=pk_review)
    except Http404:
        return JsonResponse({'error': 'Review not found'}, status=404)

    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


# Public Method
@extend_schema(
    request=ReviewSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Create a new review',
    operation_id='add_review',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('content', 'recommend', 'pk_game')
@auth_required
def add_review(request):
    payload = request.json
    content = payload['content']
    recommend = payload['recommend']
    pk_game = payload['pk_game']

    try:
        game = get_object_or_404(Game, pk_game)
    except Http404:
        return JsonResponse({'error': 'Game associated not found'}, status=404)

    user = request.user

    review = Review.objects.create(content=content, recommend=recommend, game=game, user=user)
    return JsonResponse({'id': review.pk}, status=200)


# Public method
@extend_schema(
    request=ReviewSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Update an existing review',
    operation_id='update_review',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_review',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the review to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
def edit_review(request, pk_review: int):
    payload = request.json
    content = payload['content']
    recommend = payload['recommend']
    pk_game = payload['pk_game']
    pk_author = payload['pk_author']

    try:
        review = get_object_or_404(Review, pk=pk_review)
    except Http404:
        return JsonResponse({'error': 'Review not found'}, status=404)

    if request.user != review.author:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    if content:
        review.content = content

    if recommend:
        review.recommend = recommend

    if pk_game:
        try:
            game = get_object_or_404(Game, pk_game)
        except Http404:
            return JsonResponse({'error': 'Game to associate not found'}, status=404)

        review.game = game

    if pk_author:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

        try:
            author = get_object_or_404(User, pk_author)
        except Http404:
            return JsonResponse({'error': 'Author to associate not found'}, status=404)

        review.author = author

    review.save()
    return JsonResponse({'id': review.pk}, status=200)


# Public method
@extend_schema(
    request=ReviewSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Delete an existing review',
    operation_id='update_review',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_review',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the review to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_review(request, pk_review: int):

    try:
        review = get_object_or_404(Review, pk=pk_review)
    except Http404:
        return JsonResponse({'error': 'Review not found'}, status=404)

    if request.user != review.author:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    review.delete()
    return JsonResponse(status=200)


##############################
# Media Methods
##############################


@extend_schema(
    responses={200: MediaSchemaSerializer, 404: None},
    description='Get all medias',
    operation_id='get_medias',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def media_list(request):
    medias = Media.objects.all()
    serializer = MediaSerializer(medias, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: MediaSchemaSerializer, 404: None},
    description='Get details of a specific media',
    operation_id='get_media_detail',
    parameters=[
        OpenApiParameter(
            name='pk_media',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the media to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def media_detail(request, pk_media: int):
    try:
        media = get_object_or_404(Media, pk=pk_media)
    except Http404:
        return JsonResponse({'error': 'Media not found'}, status=404)

    serializer = MediaSerializer(media, request=request)
    return serializer.json_response()


@extend_schema(
    request=MediaSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 400: None},
    description='Create a media',
    operation_id='add_media',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('image', 'pk_review')
@auth_required
def add_media(request):
    payload = request.json
    image = payload['image']
    pk_review = payload['pk_review']

    try:
        review = get_object_or_404(Review, pk_review)
    except Http404:
        return JsonResponse({'error': 'Review associated not found'}, status=404)

    if request.user != review.author:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    media = Media.objects.create(image=image, review=review)
    return JsonResponse({'id': media.pk}, status=200)


@extend_schema(
    request=MediaSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Update an existing media',
    operation_id='update_media',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_media',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the media to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role('Admin')
def edit_media(request, pk_media: int):
    payload = request.json
    image = payload['image']
    pk_review = payload['pk_review']

    try:
        media = get_object_or_404(Media, pk=pk_media)
    except Http404:
        return JsonResponse({'error': 'Media not found'}, status=404)

    if request.user != media.review.author:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    if image:
        media.image = image

    if pk_review:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

        try:
            review = get_object_or_404(Review, pk_review)
        except Http404:
            return JsonResponse({'error': 'Review to associate not found'}, status=404)

        media.review = review

    media.save()
    return JsonResponse({'id': media.pk}, status=200)


@extend_schema(
    request=MediaSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Delete an existing media',
    operation_id='delete_media',
    parameters=[
        OpenApiParameter(
            name='pk_media',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the media to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_media(request, pk_media: int):

    try:
        media = get_object_or_404(Media, pk=pk_media)
    except Http404:
        return JsonResponse({'error': 'Media not found'}, status=404)

    if request.user != media.review.author:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    media.delete()
    return JsonResponse(status=200)


# FavoriteItem Methods
@extend_schema(
    responses={200: FavoriteSchemaSerializer, 404: None},
    description='Get details of a specific favoriteitem',
    operation_id='get_favorite_detail',
    parameters=[
        OpenApiParameter(
            name='pk_media',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the favoriteitem to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def favorite_item_list(request):
    favorite_items = FavoriteItem.objects.all()
    serializer = FavoriteItemSerializer(favorite_items, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: FavoriteSchemaSerializer, 404: None},
    description='Get details of a specific media',
    operation_id='get_favorite_detail',
    parameters=[
        OpenApiParameter(
            name='pk_media',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the media to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def favorite_item_detail(request, pk_favorite_item: int):
    try:
        favorite_item = get_object_or_404(FavoriteItem, pk=pk_favorite_item)
    except Http404:
        return JsonResponse({'error': 'FavoriteItem not found'}, status=404)

    serializer = FavoriteItemSerializer(favorite_item, request=request)
    return serializer.json_response()


# Public Method
@extend_schema(
    request=FavoriteSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Add a new favorite',
    operation_id='add_self_favorite',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game')
@auth_required
def add_self_favorite_item(request):
    payload = request.json
    pk_game = payload['pk_game']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game asociated not found'}, status=404)

    user = request.user

    favorite_item = FavoriteItem.objects.create(game=game, user=user)
    return JsonResponse({'id': favorite_item.pk}, status=200)


@extend_schema(
    request=FavoriteSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Add a new favorite',
    operation_id='add_favorite',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game', 'pk_user')
@auth_required
def add_favorite_item(request):
    payload = request.json
    pk_game = payload['pk_game']
    pk_user = payload['pk_user']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game asociated not found'}, status=404)

    try:
        user = get_object_or_404(User, pk=pk_user)
    except Http404:
        return JsonResponse({'error': 'User asociated not found'}, status=404)

    favorite_item = FavoriteItem.objects.create(game=game, user=user)
    return JsonResponse({'id': favorite_item.pk}, status=200)


# Private Method because normal users wants only to add or delete from favorites
@extend_schema(
    request=FavoriteSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Update an existing favorite',
    operation_id='update_favorite',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_favorite',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the favorite to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role('Admin')
def edit_favorite_item(request, pk_favorite_item: int):
    payload = request.json
    pk_game = payload['pk_game']
    pk_user = payload['pk_user']

    try:
        favorite_item = get_object_or_404(FavoriteItem, pk=pk_favorite_item)
    except Http404:
        return JsonResponse({'error': 'FavoriteItem not found'}, status=404)

    if pk_game:
        try:
            game = get_object_or_404(Game, pk=pk_game)
        except Http404:
            return JsonResponse({'error': 'Game to asociate not found'}, status=404)
        favorite_item.game = game

    if pk_user:
        try:
            user = get_object_or_404(User, pk=pk_user)
        except Http404:
            return JsonResponse({'error': 'User to asociate not found'}, status=404)
        favorite_item.user = user

    favorite_item.save()
    return JsonResponse({'id': favorite_item.pk}, status=200)


@extend_schema(
    request=FavoriteSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Delete an existing favorite',
    operation_id='delete_favorite',
    parameters=[
        OpenApiParameter(
            name='pk_favorite',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the favorite to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_favorite_item(request, pk_favorite_item: int):
    try:
        favorite_item = get_object_or_404(FavoriteItem, pk=pk_favorite_item)
    except Http404:
        return JsonResponse({'error': 'FavoriteItem not found'}, status=404)

    if request.user != favorite_item.user:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    favorite_item.delete()
    return JsonResponse(status=200)
