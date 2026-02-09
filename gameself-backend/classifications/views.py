from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from .models import Platform, Genre, Developer, Publisher, Edition, Region
from .serializers import PlatformSerializer, GenreSerializer, DeveloperSerializer, PublisherSerializer, EditionSerializer, RegionSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
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
@require_role('Admin')
def add_platform(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    platform = Platform.objects.create(name=name, description=description)
    return JsonResponse({'id': platform.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def edit_platform(request, pk_platform : int):
    payload = request.json
    name = payload['name']
    description = payload['description']

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    
    if name:
        platform.name = name

    if description:
        platform.description = description

    platform.save()
    return JsonResponse({'id': platform.pk}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_platform(request, pk_platform : int):

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    
    platform.delete()
    return JsonResponse(status=200)

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
@require_role('Admin')
def add_genre(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    genre = Genre.objects.create(name=name, description=description)
    return JsonResponse({'id': genre.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def edit_genre(request, pk_genre : int):
    payload = request.json
    name = payload['name']
    description = payload['description']

    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)
    
    if name:
        genre.name = name

    if description:
        genre.description = description

    genre.save()
    return JsonResponse({'id': genre.pk}, status=200)

@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_genre(request, pk_genre : int):
    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)
    
    genre.delete()
    return JsonResponse(status=200)

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
@require_role('Admin')
def add_developer(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    developer = Developer.objects.create(name=name, description=description)
    return JsonResponse({'id': developer.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def edit_developer(request, pk_developer : int):
    payload = request.json
    name = payload['name']
    description = payload['description']

    try:
        developer = get_object_or_404(Developer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)
    
    if name:
        developer.name = name

    if description:
        developer.description = description

    developer.save()
    return JsonResponse({'id': developer.pk}, status=200)

@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_developer(request, pk_developer : int):
    try:
        developer = get_object_or_404(Developer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)
    
    developer.delete()
    return JsonResponse(status=200)

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
@require_role('Admin')
def add_publisher(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    publisher = Publisher.objects.create(name=name, description=description)
    return JsonResponse({'id': publisher.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def edit_publisher(request, pk_publisher : int):
    payload = request.json
    name = payload['name']
    description = payload['description']

    try:
        publisher = get_object_or_404(Publisher, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)
    
    if name:
        publisher.name = name

    if description:
        publisher.description = description

    publisher.save()
    return JsonResponse({'id': publisher.pk}, status=200)

@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_publisher(request, pk_publisher : int):
    try:
        publisher = get_object_or_404(Publisher, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)
    
    publisher.delete()
    return JsonResponse(status=200)

@csrf_exempt
@require_http_methods('GET')
def edition_list(request):
    editions = Edition.objects.all()
    serializer = EditionSerializer(editions, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def edition_detail(request, pk_edition: int):
    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)

    serializer = EditionSerializer(edition, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def add_edition(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    edition = Edition.objects.create(name=name, description=description)
    return JsonResponse({'id': edition.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def edit_edition(request, pk_edition: int):
    payload = request.json
    name = payload['name']
    description = payload['description']

    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)
    
    if name:
        edition.name = name

    if description:
        edition.description = description

    edition.save()
    return JsonResponse({'id': edition.pk}, status=200)

@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_edition(request, pk_edition : int):
    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)
    
    edition.delete()
    return JsonResponse(status=200)

@csrf_exempt
@require_http_methods('GET')
def region_list(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def region_detail(request, pk_region: int):
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    serializer = RegionSerializer(region, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description', 'acronym', 'icon')
@auth_required
@require_role('Admin')
def add_region(request):
    payload = request.json
    name = payload['name']
    description = payload['description']
    acronym = payload['acronym']
    icon = payload['icon']  #TODO: Question - No hay que manejar de alguna forma el icono aquí? Lógica del front?

    region = Region.objects.create(name=name, description=description, acronym=acronym, icon=icon)
    return JsonResponse({'id': region.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@require_fields('name', 'description', 'acronym', 'icon')
@auth_required
@require_role('Admin')
def edit_region(request, pk_region: int):
    payload = request.json
    name = payload['name']
    description = payload['description']
    acronym = payload['acronym']
    icon = payload['icon']  #TODO: Question - No hay que manejar de alguna forma el icono aquí? Lógica del front?

    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)
    
    if name:
        region.name = name

    if description:
        region.description = description

    if acronym:
        region.acronym = acronym

    if icon:
        region.icon = icon

    region.save()
    return JsonResponse({'id': region.pk}, status=200)

@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_region(request, pk_region : int):
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)
    
    region.delete()
    return JsonResponse(status=200)