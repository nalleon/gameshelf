from math import ceil

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from classifications.models import Developer, Edition, Genre, Platform, Publisher, Region
from shared.decorators import require_fields, require_json_body, require_role
from shared.serializers import ErrorResponseSerializer
from users.decorators import auth_required
from users.models import Profile

from .models import FavoriteItem, Game, Media, Review
from .serializers import (
    FavoriteItemSerializer,
    FavoriteSchemaSerializer,
    GameSchemaSerializer,
    GameSerializer,
    IGBDRequestGameSchema,
    ReviewMediaUploadSerializer,
    ReviewSchemaSerializer,
    ReviewSerializer,
    SaveFavoriteSchemaSerializer,
    SaveGameSchemaSerializer,
    SaveReviewSchemaSerializer,
    UpdateFavoriteSchemaSerializer,
)
from .services.igdb import import_games, search_games_by_title
from django.db.models import Q
User = get_user_model()


# Fetch games from IGDB
@extend_schema(
    methods=['POST'],
    request=IGBDRequestGameSchema,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'created': {'type': 'integer'},
                'skipped': {'type': 'integer'},
                'total_received': {'type': 'integer'},
            },
        },
        500: None,
    },
    description='Import games from IGDB into the database',
)
@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(
            name='title',
            description='Title of the game to search',
            required=True,
            type=OpenApiTypes.STR,
        ),
    ],
    responses={
        200: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'summary': {'type': 'string', 'nullable': True},
                    'first_release_date': {'type': 'integer', 'nullable': True},
                    'cover_url': {'type': 'string', 'nullable': True},
                    'genres': {'type': 'array', 'items': {'type': 'string'}},
                    'platforms': {'type': 'array', 'items': {'type': 'string'}},
                    'developers': {'type': 'array', 'items': {'type': 'string'}},
                    'publishers': {'type': 'array', 'items': {'type': 'string'}},
                    'age_ratings': {'type': 'array', 'items': {'type': 'string'}},
                },
            },
        },
        400: None,
        500: None,
    },
    description='Search games from IGDB by title',
)
@api_view(['POST', 'GET'])
@csrf_exempt
# @auth_required
def igdb_wrapper(request):
    match request.method:
        case 'POST':
            return import_games(request)
        case 'GET':
            return search_games_by_title(request)


# Games Methods
@extend_schema(
    methods=['GET'],
    description='Get all games',
    parameters=[
        OpenApiParameter(
            name='mature_content',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                'If true, returns all games (both mature and non-mature). '
                'If false, returns only non-mature games.'
            ),
            examples=[
                OpenApiExample('Return all games', value=True),
                OpenApiExample('Only non-mature games', value=False),
            ],
        ),
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Page number (default = 1)',
            examples=[OpenApiExample('First page', value=1)],
        ),
        OpenApiParameter(
            name='page_size',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Number of items per page (default = 15)',
            examples=[OpenApiExample('15 items per page', value=15)],
        ),
    ],
    responses={200: GameSerializer.get_paginated_schema('Game')},
)
@api_view(['GET'])
@csrf_exempt
def game_wrapper(request):
    match request.method:
        case 'GET':
            return game_list(request)


@csrf_exempt
def game_list(request):
    mature_content = request.GET.get('mature_content')
    page = _get_int_param(request, 'page', 1)
    page_size = _get_int_param(request, 'page_size', 15)

    if mature_content is not None:
        mature_content = mature_content.lower() == 'true'

        if mature_content:
            games = Game.objects.all()
        else:
            games = Game.objects.filter(mature_content=False)
    else:
        games = Game.objects.filter(mature_content=False)

    total_count = games.count()
    total_pages = ceil(total_count / page_size)

    start = (page - 1) * page_size
    end = start + page_size

    paginated_games = games[start:end]

    pagination_data = {
        'results': paginated_games,
        'count': total_count,
        'total_pages': total_pages,
        'current_page': page,
        'has_next': page < total_pages,
        'has_previous': page > 1,
    }

    serializer = GameSerializer([], request=request)

    return Response(serializer.serialize_paginated(pagination_data))


def _get_int_param(request, name, default):
    try:
        return max(1, int(request.GET.get(name, default)))
    except (TypeError, ValueError):
        return default

@extend_schema(
    methods=['GET'],
    description='Advanced game search with filters',
    parameters=[

        OpenApiParameter(
            name='q',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Search by game title',
        ),

        OpenApiParameter(
            name='developer',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by developer name',
        ),

        OpenApiParameter(
            name='publisher',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by publisher name',
        ),

        OpenApiParameter(
            name='genre',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            many=True,
            description='Filter by multiple genres',
            examples=[
                OpenApiExample(
                    'Multiple genres',
                    value=['RPG', 'Action']
                )
            ],
        ),

        OpenApiParameter(
            name='region',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by region name',
        ),

        OpenApiParameter(
            name='year',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by release year',
        ),

        OpenApiParameter(
            name='mature_content',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Include mature games',
        ),

        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Page number',
        ),

        OpenApiParameter(
            name='page_size',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Results per page',
        ),
    ],
    responses={200: GameSerializer.get_paginated_schema('Game')},
)
@api_view(['GET'])
@csrf_exempt
def game_search_wrapper(request):

    match request.method:
        case 'GET':
            return game_search(request)
        
@csrf_exempt
def game_search(request):

    q = request.GET.get('q')
    developer = request.GET.get('developer')
    publisher = request.GET.get('publisher')
    genres = request.GET.getlist('genres')
    region = request.GET.get('region')
    year = request.GET.get('year')
    mature_content = request.GET.get('mature_content')
    
    print("GENRES:", genres)  # 👈 AQUÍ

    page = _get_int_param(request, 'page', 1)
    page_size = _get_int_param(request, 'page_size', 15)

    games = Game.objects.all()

    # Mature filter
    if mature_content is not None:

        mature_content = mature_content.lower() == 'true'

        if not mature_content:
            games = games.filter(mature_content=False)

    else:
        games = games.filter(mature_content=False)

    # Search title
    if q:
        games = games.filter(
            Q(title__icontains=q)
        )

    # Developer
    if developer:
        games = games.filter(
            developers__name__icontains=developer
        )

    # Publisher
    if publisher:
        games = games.filter(
            publishers__name__icontains=publisher
        )

    # Genre
    if genres:

        # genre_query = Q()

        for genre in genres:
            games = games.filter(
                genres__name__icontains=genre
            )

        # games = games.filter(genre_query)

    # Region
    if region:
        games = games.filter(
            region__name__icontains=region
        )

    # Year
    if year:
        games = games.filter(
            released_at__year=year
        )

    games = games.distinct()

    total_count = games.count()

    total_pages = ceil(total_count / page_size)

    start = (page - 1) * page_size
    end = start + page_size

    paginated_games = games[start:end]

    pagination_data = {
        'results': paginated_games,
        'count': total_count,
        'total_pages': total_pages,
        'current_page': page,
        'has_next': page < total_pages,
        'has_previous': page > 1,
    }

    serializer = GameSerializer([], request=request)

    return Response(
        serializer.serialize_paginated(pagination_data)
    )

@extend_schema(
    methods=['GET'],
    responses={200: GameSchemaSerializer, 404: None},
    description='Get details of a specific game',
    parameters=[
        OpenApiParameter(
            name='pk_game',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
        ),
    ],
)
@extend_schema(
    methods=['PUT'],
    request=SaveGameSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        404: None,
    },
    description='Update an existing game',
)
@extend_schema(
    methods=['DELETE'],
    responses={204: None, 404: None},
    description='Delete an existing game',
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def game_detail_wrapper(request, pk_game: int):
    match request.method:
        case 'GET':
            return game_detail(request, pk_game)
        case 'PUT':
            return edit_game(request, pk_game)
        case 'DELETE':
            return delete_game(request, pk_game)


@csrf_exempt
def game_detail(request, pk_game: int):
    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return Response({'error': 'Game not found'}, status=404)

    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_game(request, pk_game: int):


    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return Response({'error': 'Game not found'}, status=404)

    payload = request.json
    title = payload['title']
    slug = payload['slug']
    description = payload['description']
    cover_default = payload['cover_default']
    released_at = payload['released_at']
    pk_platforms_list = payload['pk_platforms_list']
    pk_genres_list = payload['pk_genres_list']
    pk_developers_list = payload['pk_developers_list']
    pk_publishers_list = payload['pk_publishers_list']
    pk_edition = payload['pk_edition']
    pk_region = payload['pk_region']
    
    if title:
        game.title = title

    if slug:
        game.slug = slug

    if description:
        game.description = description

    if cover_default:
        game.cover_default = cover_default

    if released_at:
        game.released_at = released_at

    if pk_platforms_list:
        platforms = []
        for pk_platform in pk_platforms_list:
            try:
                platform = get_object_or_404(Platform, pk_platform)
            except Http404:
                return Response({'error': 'Platform to associate not found'}, status=404)
            platforms.append(platform)

        game.platforms = platforms

    if pk_genres_list:
        genres = []
        for pk_genre in pk_genres_list:
            try:
                genre = get_object_or_404(Genre, pk_genre)
            except Http404:
                return Response({'error': 'Genre to associate not found'}, status=404)
            genres.append(genre)

        game.genres = genres

    if pk_developers_list:
        developers = []
        for pk_developer in pk_developers_list:
            try:
                developer = get_object_or_404(Developer, pk_developer)
            except Http404:
                return Response({'error': 'Developer to associate not found'}, status=404)
            developers.append(developer)

        game.developers = developers

    if pk_publishers_list:
        publishers = []
        for pk_publisher in pk_publishers_list:
            try:
                publisher = get_object_or_404(Publisher, pk_publisher)
            except Http404:
                return Response({'error': 'Publisher to associate not found'}, status=404)

            publishers.append(publisher)

        game.publishers = publishers

    if pk_edition:
        try:
            edition = get_object_or_404(Edition, pk_edition)
        except Http404:
            return Response({'error': 'Edition to associate not found'}, status=404)

        game.edition = edition

    if pk_region:
        try:
            region = get_object_or_404(Region, pk_region)
        except Http404:
            return Response({'error': 'Region to associate not found'}, status=404)

        game.region = region

    game.save()
    return Response({'id': game.pk}, status=200)


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_game(request, pk_game: int):

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return Response({'error': 'Game not found'}, status=404)

    game.delete()
    return Response(status=204)


# Reviews Methods


@extend_schema(
    methods=['GET'],
    description='Get all reviews',
    operation_id='get_reviews',
    parameters=[
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Page number (default = 1)',
            examples=[OpenApiExample('First page', value=1)],
        ),
        OpenApiParameter(
            name='page_size',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Number of items per page (default = 15)',
            examples=[OpenApiExample('15 items per page', value=15)],
        ),
    ],
    responses={200: ReviewSerializer.get_paginated_schema('Review')},
)
@extend_schema(
    request=SaveReviewSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Create a new review',
    operation_id='add_review',
    methods=['POST'],
)
@api_view(['GET', 'POST'])
@csrf_exempt
def review_wrapper(request):
    match request.method:
        case 'GET':
            return review_list(request)
        case 'POST':
            return add_review(request)


@csrf_exempt
def review_list(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 15))
    reviews = Review.objects.all()

    total_count = reviews.count()
    total_pages = ceil(total_count / page_size)

    start = (page - 1) * page_size
    end = start + page_size

    paginated_games = reviews[start:end]

    pagination_data = {
        'results': paginated_games,
        'count': total_count,
        'total_pages': total_pages,
        'current_page': page,
        'has_next': page < total_pages,
        'has_previous': page > 1,
    }

    serializer = ReviewSerializer([], request=request)

    return Response(serializer.serialize_paginated(pagination_data))


# Public Method
@csrf_exempt
@require_json_body
@require_fields('content', 'recommend', 'game_id')
@auth_required
def add_review(request):
    payload = request.json
    content = payload['content']
    recommend = payload['recommend']
    game_id = payload['game_id']

    try:
        game = get_object_or_404(Game, pk=game_id)
    except Http404:
        return Response({'error': 'Game associated not found'}, status=404)

    user = request.user

    review = Review.objects.create(content=content, recommend=recommend, game=game, author=user)
    return Response({'id': review.pk}, status=200)


@extend_schema(
    responses={200: ReviewSchemaSerializer, 404: None},
    description='Get review detail',
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
@extend_schema(
    request=SaveReviewSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        403: None,
        404: None,
    },
    description='Update an existing review',
    operation_id='update_review',
    methods=['PATCH'],
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
@extend_schema(
    request=ReviewSchemaSerializer,
    responses={
        204: None,
        400: None,
        403: None,
        404: None,
    },
    description='Delete an existing review',
    operation_id='delete_review',
    methods=['DELETE'],
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
@api_view(['GET', 'PATCH', 'DELETE'])
@csrf_exempt
def review_detail_wrapper(request, pk_review: int):
    match request.method:
        case 'GET':
            return review_detail(request, pk_review)
        case 'PATCH':
            return edit_review(request, pk_review)
        case 'DELETE':
            return delete_review(request, pk_review)


@csrf_exempt
def review_detail(request, pk_review: int):
    try:
        review = get_object_or_404(Review, pk=pk_review)
    except Http404:
        return Response({'error': 'Review not found'}, status=404)

    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


# Public method
@csrf_exempt
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
        return Response({'error': 'Review not found'}, status=404)

    if request.user != review.author:
        if request.user.role != 'Admin':
            return Response({'error': 'Forbbiden Access'}, status=403)

    if content:
        review.content = content

    if recommend:
        review.recommend = recommend

    if pk_game:
        try:
            game = get_object_or_404(Game, pk_game)
        except Http404:
            return Response({'error': 'Game to associate not found'}, status=404)

        review.game = game

    if pk_author:
        if request.user.role != 'Admin':
            return Response({'error': 'Forbbiden Access'}, status=403)

        try:
            author = get_object_or_404(User, pk_author)
        except Http404:
            return Response({'error': 'Author to associate not found'}, status=404)

        review.author = author

    review.save()
    return Response({'id': review.pk}, status=200)


# Public method


@csrf_exempt
@auth_required
def delete_review(request, pk_review: int):

    try:
        review = get_object_or_404(Review, pk=pk_review)
    except Http404:
        return Response({'error': 'Review not found'}, status=404)

    if request.user != review.author:
        if request.user.role != 'Admin':
            return Response({'error': 'Forbbiden Access'}, status=403)

    review.delete()
    return Response(status=204)


@extend_schema(
    request=ReviewMediaUploadSerializer,
    responses={
        200: {
            'type': 'object',
            'properties': {'ids': {'type': 'array', 'items': {'type': 'integer'}}},
        },
        400: None,
        403: None,
        404: None,
    },
    description='Upload media files to a review',
    operation_id='add_review_media',
)
@parser_classes([MultiPartParser, FormParser])
@api_view(['POST'])
@csrf_exempt
@auth_required
def add_review_media(request, pk_review: int):
    try:
        review = get_object_or_404(Review, pk=pk_review)
    except Http404:
        return Response({'error': 'Review not found'}, status=404)

    if request.user != review.author:
        return Response({'error': 'Forbidden'}, status=403)

    files = request.FILES.getlist('images')

    if not files:
        return Response({'error': 'At least one image is required'}, status=400)

    media_ids = []

    for file in files:
        media = Media.objects.create(review=review, image=file)
        media_ids.append(media.pk)

    return Response({'ids': media_ids}, status=200)


@extend_schema_view(
    delete=extend_schema(
        responses={200: None, 403: None, 404: None},
        description='Delete a review media item',
        operation_id='delete_review_media',
        parameters=[
            OpenApiParameter(
                name='pk_media',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the media to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['DELETE'])
@csrf_exempt
@auth_required
def delete_review_media(request, pk_media: int):

    try:
        media = get_object_or_404(Media, pk=pk_media)
    except Http404:
        return Response({'error': 'Media not found'}, status=404)

    if request.user != media.review.author:
        return Response({'error': 'Forbidden'}, status=403)

    media.delete()
    return Response({}, status=204)


# Favorite Methods
@extend_schema_view(
    get=extend_schema(
        responses={200: FavoriteSchemaSerializer, 404: None},
        description='Get all favoriteitem',
        operation_id='get_favorites',
    ),
    post=extend_schema(
        request=SaveFavoriteSchemaSerializer,
        responses={
            200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description='Add a new favorite',
        operation_id='add_self_favorite',
    ),
)
@api_view(['GET', 'POST'])
@csrf_exempt
@auth_required
def favorites_wrapper(request):
    match request.method:
        case 'POST':
            return add_favorite_item(request)
        case 'GET':
            return favorite_item_list(request)


@csrf_exempt
def favorite_item_list(request):
    favorite_items = request.user.favorites.all()
    serializer = FavoriteItemSerializer(favorite_items, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@require_fields('pk_game', 'pk_platform')
@auth_required
def add_favorite_item(request):

    payload = request.json
    pk_game = payload['pk_game']
    pk_platform = payload['pk_platform']
    user = request.user

    if FavoriteItem.objects.filter(user=user).count() >= 10:
        return Response(
            {'error': 'Maximum number of favorites reached'},
            status=400
        )
    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return Response({'error': 'Game asociated not found'}, status=404)

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return Response({'error': 'Platform asociated not found'}, status=404)
    
    if FavoriteItem.objects.filter(user=user, game=game, platform=platform).exists():
        return Response({'error': 'Game with platform already in favorites'}, status=400)


    last_order = FavoriteItem.objects.filter(user=user).aggregate(max_order=Max('order'))[
        'max_order'
    ]

    favorite_item = FavoriteItem.objects.create(game=game, platform=platform, user=user, order=(last_order or 0) + 1)

    return Response({'id': favorite_item.pk}, status=200)


@extend_schema_view(
    patch=extend_schema(
        request=UpdateFavoriteSchemaSerializer,
        responses={
            200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description='Update an existing favorite',
        operation_id='update_favorite',
        parameters=[
            OpenApiParameter(
                name='pk_favorite',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the favorite to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        responses={
            204: None,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
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
    ),
)
@api_view(['PATCH', 'DELETE'])
@csrf_exempt
@auth_required
def favorites_detail_wrapper(request, pk_favorite: int):
    match request.method:
        case 'PATCH':
            return edit_favorite_item(request, pk_favorite)

        case 'DELETE': 
            return delete_favorite_item(request, pk_favorite)


@csrf_exempt
@require_json_body
@auth_required
def edit_favorite_item(request, pk_favorite: int):

    payload = request.json
    new_order = payload['order']

    try:
        favorite_item = get_object_or_404(FavoriteItem, pk=pk_favorite)
    except Http404:
        return Response({'error': 'Favorite not found'}, status=404)

    if request.user != favorite_item.user:
        return Response({'error': 'Unable to edit another user favorites'}, status=403)

    old_order = favorite_item.order

    if new_order == old_order:
        return Response({'id': favorite_item.pk}, status=200)

    user_favorites = FavoriteItem.objects.filter(user=request.user)

    if new_order > old_order:
        user_favorites.filter(order__gt=old_order, order__lte=new_order).update(
            order=models.F('order') - 1
        )
    else:
        user_favorites.filter(order__lt=old_order, order__gte=new_order).update(
            order=models.F('order') + 1
        )

    favorite_item.order = new_order
    
    new_pk_platform = payload['pk_platform']
    
    if new_pk_platform:
        new_platform = get_object_or_404(Platform, pk=new_pk_platform)

        if new_platform != favorite_item.platform:
            favorite_item.platform = new_platform
            
    favorite_item.save()

    return Response({'id': favorite_item.pk}, status=200)


@csrf_exempt
@auth_required
def delete_favorite_item(request, pk_favorite_item: int):
    try:
        favorite_item = get_object_or_404(FavoriteItem, pk=pk_favorite_item)
    except Http404:
        return Response({'error': 'Favorite not found'}, status=404)

    if request.user != favorite_item.user:
        return Response({'error': 'Forbbiden Access'}, status=403)

    favorite_item.delete()
    return Response(status=204)
