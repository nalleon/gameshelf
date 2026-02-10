from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from .models import Game, Review, Media, FavoriteItem
from classifications.models import Platform, Genre, Developer, Publisher, Edition, Region
from .serializers import GameSerializer, ReviewSerializer, MediaSerializer, FavoriteItemSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
from users.decorators import auth_required

@csrf_exempt
@require_http_methods('GET')
def platform_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def platform_detail(request, pk_game: int):
    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    serializer = GameSerializer(game, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('title', 'slug', 'description', 'cover', 'released_at', 
                'pk_platforms_list', 'pk_genres_list', 'pk_developers_list', 
                'pk_publishers_list', 'pk_edition', 'pk_region')
@auth_required
@require_role('Admin')
def add_platform(request):
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

    game = Game.objects.create(title=title, slug=slug, description=description, cover=cover, released_at=released_at, 
                                platforms=platforms, genres=genres, developers=developers, publishers=publishers, 
                                edition=edition, region=region)

    return JsonResponse({'id': game.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role('Admin')
def edit_platform(request, pk_game : int):
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
        game.title=title
        
    if slug:        
        game.slug=slug
    
    if description:
        game.description=description
        
    if cover:
        game.cover=cover
        
    if released_at:
        game.released_at=released_at

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

        game.genres=genres

    if pk_developers_list:
        developers = []
        for pk_developer in pk_developers_list:
            try:
                developer = get_object_or_404(Developer, pk_developer)
            except Http404:
                return JsonResponse({'error': 'Developer to associate not found'}, status=404)
            developers.append(developer)
        
        game.developers=developers

    if pk_publishers_list:
        publishers = []
        for pk_publisher in pk_publishers_list:
            try:
                publisher = get_object_or_404(Publisher, pk_publisher)
            except Http404:
                return JsonResponse({'error': 'Publisher to associate not found'}, status=404)

            publishers.append(publisher)

        game.publishers=publishers

    if pk_edition:
        try:
            edition = get_object_or_404(Edition, pk_edition)
        except Http404:
            return JsonResponse({'error': 'Edition to associate not found'}, status=404)

        game.edition=edition
    
    if pk_region:
        try:
            region = get_object_or_404(Region, pk_region)
        except Http404:
            return JsonResponse({'error': 'Region to associate not found'}, status=404)

        game.region=region

    game.save()
    return JsonResponse({'id': game.pk}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_platform(request, pk_game : int):

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    game.delete()
    return JsonResponse(status=200)