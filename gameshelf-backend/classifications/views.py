from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.decorators import api_view

from shared.decorators import require_fields, require_http_methods, require_json_body, require_role
from users.decorators import auth_required
from users.models import Profile

from .models import Developer, Edition, Genre, Platform, Publisher, Region

from .serializers import (
    ClassificationSchemaSerializer,
    DeveloperSerializer,
    EditionSerializer,
    GenreSchemaSerializer,
    GenreSerializer,
    PlatformSchemaSerializer,
    PlatformSerializer,
    PublisherSerializer,
    RegionSchemaSerializer,
    RegionSerializer,
    SaveGenreSchemaSerializer,
    SavePlatformSchemaSerializer,
    SaveRegionSchemaSerializer,
    SaveClassificationSchemaSerializer
)


@extend_schema(
    responses={200: PlatformSchemaSerializer, 404: None},
    description='Get all platforms',
    operation_id='get_platforms',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: PlatformSchemaSerializer, 404: None},
    description='Get details of a specific platform',
    operation_id='get_platform_detail',
    parameters=[
        OpenApiParameter(
            name='pk_platform',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the platform to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def platform_detail(request, pk_platform: int):
    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)

    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()


@extend_schema(
    request=SavePlatformSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Create a new platform',
    operation_id='add_platform',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_platform(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    platform = Platform.objects.create(name=name, description=description)
    return JsonResponse({'id': platform.pk}, status=200)


@extend_schema(
    request=SavePlatformSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Update an existing platform',
    operation_id='update_platform',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_platform',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the platform to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_platform(request, pk_platform: int):
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


@extend_schema(
    responses={200: None, 404: None},
    description='Delete an existing platform',
    operation_id='delete_platform',
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name='pk_platform',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the platform to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_platform(request, pk_platform: int):

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)

    platform.delete()
    return JsonResponse(status=200)


# Genre methods


@extend_schema(
    responses={200: GenreSchemaSerializer, 404: None},
    description='Get all genres',
    operation_id='get_genres',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: GenreSchemaSerializer, 404: None},
    description='Get details of a specific genre',
    operation_id='get_genre_detail',
    parameters=[
        OpenApiParameter(
            name='pk_genre',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the genre to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def genre_detail(request, pk_genre: int):
    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)

    serializer = GenreSerializer(genre, request=request)
    return serializer.json_response()


@extend_schema(
    request=SaveGenreSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Create a new genre',
    operation_id='add_genre',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_genre(request):
    payload = request.json
    name = payload['name']
    description = payload['description']
    acronym = payload['acronym']

    genre = Genre.objects.create(name=name, description=description, acronym=acronym)
    return JsonResponse({'id': genre.pk}, status=200)


@extend_schema(
    request=SaveGenreSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Update an existing genre',
    operation_id='update_genre',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_genre',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the genre to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_genre(request, pk_genre: int):
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

    if description:
        genre.description = description

    genre.save()
    return JsonResponse({'id': genre.pk}, status=200)


@extend_schema(
    responses={200: None, 404: None},
    description='Delete an existing genre',
    operation_id='delete_genre',
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name='pk_genre',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the genre to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_genre(request, pk_genre: int):
    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)

    genre.delete()
    return JsonResponse(status=200)


@extend_schema(
    responses={200: ClassificationSchemaSerializer, 404: None},
    description='Get all developers',
    operation_id='get_developers',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def developer_list(request):
    developers = Developer.objects.all()
    serializer = DeveloperSerializer(developers, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: ClassificationSchemaSerializer, 404: None},
    description='Get details of a specific developer',
    operation_id='get_developer_detail',
    parameters=[
        OpenApiParameter(
            name='pk_developer',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the developer to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def developer_detail(request, pk_developer: int):
    try:
        developer = get_object_or_404(DeveloperSerializer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    serializer = DeveloperSerializer(developer, request=request)
    return serializer.json_response()


@extend_schema(
    request=ClassificationSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Create a new developer',
    operation_id='add_developer',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_developer(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    developer = Developer.objects.create(name=name, description=description)
    return JsonResponse({'id': developer.pk}, status=200)


@extend_schema(
    request=ClassificationSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Update an existing developer',
    operation_id='update_developer',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_developer',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the developer to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_developer(request, pk_developer: int):
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


@extend_schema(
    request=ClassificationSchemaSerializer,
    responses={200: None, 404: None},
    description='Delete an existing developer',
    operation_id='delete_developer',
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name='pk_developer',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the developer to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_developer(request, pk_developer: int):
    try:
        developer = get_object_or_404(Developer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    developer.delete()
    return JsonResponse(status=200)


@extend_schema(
    responses={200: ClassificationSchemaSerializer, 404: None},
    description='Get all publishers',
    operation_id='get_publishers',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def publisher_list(request):
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: ClassificationSchemaSerializer, 404: None},
    description='Get details of a specific publisher',
    operation_id='get_publisher_detail',
    parameters=[
        OpenApiParameter(
            name='pk_publisher',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the publisher to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def publisher_detail(request, pk_publisher: int):
    try:
        publisher = get_object_or_404(PublisherSerializer, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

    serializer = PublisherSerializer(publisher, request=request)
    return serializer.json_response()


@extend_schema(
    request=SaveClassificationSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Create a new publisher',
    operation_id='add_publisher',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_publisher(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    publisher = Publisher.objects.create(name=name, description=description)
    return JsonResponse({'id': publisher.pk}, status=200)


@extend_schema(
    request=SaveClassificationSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Update an existing publisher',
    operation_id='update_publisher',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_publisher',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the publisher to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_publisher(request, pk_publisher: int):
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


@extend_schema(
    responses={200: None, 404: None},
    description='Delete an existing publisher',
    operation_id='delete_publisher',
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name='pk_publisher',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the publisher to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_publisher(request, pk_publisher: int):
    try:
        publisher = get_object_or_404(Publisher, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

    publisher.delete()
    return JsonResponse(status=200)


@extend_schema(
    responses={200: ClassificationSchemaSerializer, 404: None},
    description='Get all editions',
    operation_id='get_editions',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def edition_list(request):
    editions = Edition.objects.all()
    serializer = EditionSerializer(editions, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: ClassificationSchemaSerializer, 404: None},
    description='Get details of a specific edition',
    operation_id='get_edition_detail',
    parameters=[
        OpenApiParameter(
            name='pk_edition',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the edition to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def edition_detail(request, pk_edition: int):
    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)

    serializer = EditionSerializer(edition, request=request)
    return serializer.json_response()


@extend_schema(
    request=SaveClassificationSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Create a new edition',
    operation_id='add_edition',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_edition(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    edition = Edition.objects.create(name=name, description=description)
    return JsonResponse({'id': edition.pk}, status=200)


@extend_schema(
    request=SaveClassificationSchemaSerializer,
    responses={
        200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
        400: None,
        404: None,
    },
    description='Update an existing edition',
    operation_id='update_edition',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_edition',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the edition to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
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


@extend_schema(
    responses={200: None, 404: None},
    description='Delete an existing edition',
    operation_id='delete_edition',
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name='pk_edition',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the edition to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_edition(request, pk_edition: int):
    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)

    edition.delete()
    return JsonResponse(status=200)


# Region


@extend_schema(
    responses={200: RegionSchemaSerializer, 404: None},
    description='Get all regions',
    operation_id='get_regions',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def region_list(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, request=request)
    return serializer.json_response()


@extend_schema(
    responses={200: RegionSchemaSerializer, 404: None},
    description='Get details of a specific region',
    operation_id='get_region_detail',
    parameters=[
        OpenApiParameter(
            name='pk_region',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the region to view',
            required=True,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def region_detail(request, pk_region: int):
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    serializer = RegionSerializer(region, request=request)
    return serializer.json_response()


@extend_schema(
    request=SaveRegionSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Create a new region',
    operation_id='add_region',
    methods=['POST'],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'acronym', 'icon')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_region(request):
    payload = request.json
    name = payload['name']
    acronym = payload['acronym']
    icon = payload[
        'icon'
    ]  # TODO: Question - No hay que manejar de alguna forma el icono aquí? Lógica del front?

    region = Region.objects.create(name=name, acronym=acronym, icon=icon)
    return JsonResponse({'id': region.pk}, status=200)


@extend_schema(
    request=SaveRegionSchemaSerializer,
    responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
    description='Update an existing region',
    operation_id='update_region',
    methods=['PUT'],
    parameters=[
        OpenApiParameter(
            name='pk_region',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the region to update',
            required=True,
        ),
    ],
)
@api_view(['PUT'])
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_region(request, pk_region: int):
    payload = request.json
    name = payload['name']
    acronym = payload['acronym']
    icon = payload[
        'icon'
    ]  # TODO: Question - No hay que manejar de alguna forma el icono aquí? Lógica del front?

    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    if name:
        region.name = name

    if acronym:
        region.acronym = acronym

    if icon:
        region.icon = icon

    region.save()
    return JsonResponse({'id': region.pk}, status=200)


@extend_schema(
    responses={200: None, 404: None},
    description='Delete an existing region',
    operation_id='delete_region',
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name='pk_region',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the region to delete',
            required=True,
        ),
    ],
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_region(request, pk_region: int):
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    region.delete()
    return JsonResponse(status=200)
