from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from .models import Platform, Genre, Developer, Publisher, Edition, Region
from .serializers import PlatformSerializer, GenreSerializer, DeveloperSerializer, PublisherSerializer, EditionSerializer, RegionSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body
from users.decorators import auth_required

@csrf_exempt
@require_http_methods('GET')
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def platform_detail(request, pk_platform: int):
    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)

    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def add_platform(request):
    
    return ''

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def edit_platform(request, pk_platform : int):
    return ''

@csrf_exempt
@require_http_methods('POST')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def delete_platform(request, pk_platform : int):
    return ''

@csrf_exempt
@require_http_methods('GET')
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def genre_detail(request, pk_genre: int):
    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)

    serializer = GenreSerializer(genre, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def add_genre(request):
    return ''

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def edit_genre(request, pk_genre : int):
    return ''

@csrf_exempt
@require_http_methods('POST')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def delete_genre(request, pk_genre : int):
    return ''

@csrf_exempt
@require_http_methods('GET')
def developer_list(request):
    developers = Developer.objects.all()
    serializer = DeveloperSerializer(developers, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def developer_detail(request, pk_developer: int):
    try:
        developer = get_object_or_404(DeveloperSerializer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    serializer = DeveloperSerializer(developer, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def add_developer(request):
    return ''

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def edit_developer(request, pk_developer : int):
    return ''

@csrf_exempt
@require_http_methods('POST')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def delete_developer(request, pk_developer : int):
    return ''

@csrf_exempt
@require_http_methods('GET')
def publisher_list(request):
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def publisher_detail(request, pk_publisher: int):
    try:
        publisher = get_object_or_404(PublisherSerializer, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

    serializer = PublisherSerializer(publisher, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def add_publisher(request):
    return ''

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def edit_publisher(request, pk_publisher : int):
    return ''

@csrf_exempt
@require_http_methods('POST')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def delete_publisher(request, pk_publisher : int):
    return ''

@csrf_exempt
@require_http_methods('GET')
def edition_list(request):
    editions = Edition.objects.all()
    serializer = EditionSerializer(editions, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def edition_detail(request, pk_publisher: int):
    try:
        edition = get_object_or_404(Edition, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    serializer = EditionSerializer(edition, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def add_edition(request):
    return ''

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def edit_edition(request, pk_edition: int):
    return ''

@csrf_exempt
@require_http_methods('POST')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def delete_edition(request, pk_edition : int):
    return ''

@csrf_exempt
@require_http_methods('GET')
def region_list(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def region_detail(request, pk_publisher: int):
    try:
        region = get_object_or_404(Edition, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    serializer = RegionSerializer(region, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description', 'acronym', 'icon')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def add_region(request):
    return ''

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description', 'acronym', 'icon')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def edit_region(request, pk_region: int):
    return ''

@csrf_exempt
@require_http_methods('POST')
@auth_required
#TODO: decorador para que el usuario tenga rol admin
def delete_region(request, pk_region : int):
    return ''