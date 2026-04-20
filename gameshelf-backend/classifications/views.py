from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
from rest_framework.decorators import api_view

from shared.decorators import require_fields, require_json_body, require_role
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
    SaveClassificationSchemaSerializer,
    SaveGenreSchemaSerializer,
    SavePlatformSchemaSerializer,
    SaveRegionSchemaSerializer,
    EditionSchemaSerializer,
    SaveEditionSchemaSerializer
)


@extend_schema_view(
    get=extend_schema(
        responses={200: PlatformSchemaSerializer, 404: None},
        description='Get platforms or platform detail',
        operation_id='get_platforms',
        parameters=[
            OpenApiParameter(
                name='pk_platform',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the platform to view',
                required=False,
            ),
        ],
    )
)
@api_view(['GET'])
@csrf_exempt
def platform_wrapper(request, pk_platform: int = None):

    match request.method:
        case 'GET':
            if pk_platform:
                return platform_detail(request, pk_platform)
            return platform_list(request)


@csrf_exempt
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@extend_schema_view(
    get=extend_schema(
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
    ),
    put=extend_schema(
        request=SavePlatformSchemaSerializer,
        responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
        description='Update an existing platform',
        operation_id='update_platform',
        parameters=[
            OpenApiParameter(
                name='pk_platform',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the platform to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        responses={200: None, 404: None},
        description='Delete an existing platform',
        operation_id='delete_platform',
        parameters=[
            OpenApiParameter(
                name='pk_platform',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the platform to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def platform_detail_wrapper(request, pk_platform: int):

    match request.method:
        case 'GET':
            return platform_detail(request, pk_platform)

        case 'PUT':
            return edit_platform(request, pk_platform)

        case 'DELETE':
            return delete_platform(request, pk_platform)


@csrf_exempt
def platform_detail(request, pk_platform: int):
    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)

    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_platform(request, pk_platform: int):
    payload = request.json
    name = payload['name']

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)

    if name:
        platform.name = name

    platform.save()
    return JsonResponse({'id': platform.pk}, status=200)


@csrf_exempt
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


@extend_schema_view(
    get=extend_schema(
        responses={200: GenreSchemaSerializer, 404: None},
        description='Get all genres',
        operation_id='get_genres',
    )
)
@api_view(['GET'])
@csrf_exempt
@auth_required
def genre_wrapper(request):

    match request.method:
        case 'GET':
            return genre_list(request)


@csrf_exempt
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, request=request)
    return serializer.json_response()


@extend_schema_view(
    get=extend_schema(
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
    ),
    put=extend_schema(
        request=SaveGenreSchemaSerializer,
        responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
        description='Update an existing genre',
        operation_id='update_genre',
        parameters=[
            OpenApiParameter(
                name='pk_genre',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the genre to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        responses={200: None, 404: None},
        description='Delete an existing genre',
        operation_id='delete_genre',
        parameters=[
            OpenApiParameter(
                name='pk_genre',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the genre to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def genre_detail_wrapper(request, pk_genre: int):

    match request.method:
        case 'GET':
            return genre_detail(request, pk_genre)

        case 'PUT':
            return edit_genre(request, pk_genre)

        case 'DELETE':
            return delete_genre(request, pk_genre)


@csrf_exempt
def genre_detail(request, pk_genre: int):
    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)

    serializer = GenreSerializer(genre, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_genre(request, pk_genre: int):
    payload = request.json
    name = payload['name']

    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)

    if name:
        genre.name = name

    genre.save()
    return JsonResponse({'id': genre.pk}, status=200)


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_genre(request, pk_genre: int):
    try:
        genre = get_object_or_404(Genre, pk=pk_genre)
    except Http404:
        return JsonResponse({'error': 'Genre not found'}, status=404)

    genre.delete()
    return JsonResponse(status=200)


# Developer methods
@extend_schema_view(
    get=extend_schema(
        responses={200: ClassificationSchemaSerializer, 404: None},
        description='Get all developers',
        operation_id='get_developers',
    ),
)
@api_view(['GET'])
@csrf_exempt
def developer_wrapper(request):

    match request.method:
        case 'GET':
            return developer_list(request)


@csrf_exempt
def developer_list(request):
    developers = Developer.objects.all()
    serializer = DeveloperSerializer(developers, request=request)
    return serializer.json_response()


@extend_schema_view(
    get=extend_schema(
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
    ),
    put=extend_schema(
        request=ClassificationSchemaSerializer,
        responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
        description='Update an existing developer',
        operation_id='update_developer',
        parameters=[
            OpenApiParameter(
                name='pk_developer',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the developer to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        request=ClassificationSchemaSerializer,
        responses={200: None, 404: None},
        description='Delete an existing developer',
        operation_id='delete_developer',
        parameters=[
            OpenApiParameter(
                name='pk_developer',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the developer to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def developer_detail_wrapper(request, pk_developer: int):

    match request.method:
        case 'GET':
            return developer_detail(request, pk_developer)

        case 'PUT':
            return edit_developer(request, pk_developer)

        case 'DELETE':
            return delete_developer(request, pk_developer)


@csrf_exempt
def developer_detail(request, pk_developer: int):
    try:
        developer = get_object_or_404(Developer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    serializer = DeveloperSerializer(developer, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_developer(request, pk_developer: int):
    payload = request.json
    name = payload['name']

    try:
        developer = get_object_or_404(Developer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    if name:
        developer.name = name


    developer.save()
    return JsonResponse({'id': developer.pk}, status=200)


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_developer(request, pk_developer: int):
    try:
        developer = get_object_or_404(Developer, pk=pk_developer)
    except Http404:
        return JsonResponse({'error': 'Developer not found'}, status=404)

    developer.delete()
    return JsonResponse(status=200)


# Publisher methods
@extend_schema_view(
    get=extend_schema(
        responses={200: ClassificationSchemaSerializer, 404: None},
        description='Get all publishers',
        operation_id='get_publishers',
    ),
)
@api_view(['GET'])
@csrf_exempt
def publisher_wrapper(request):
    match request.method:
        case 'GET':
            return publisher_list(request)


@csrf_exempt
def publisher_list(request):
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, request=request)
    return serializer.json_response()


@extend_schema_view(
    get=extend_schema(
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
    ),
    put=extend_schema(
        request=SaveClassificationSchemaSerializer,
        responses={
            200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
            400: None,
            404: None,
        },
        description='Update an existing publisher',
        operation_id='update_publisher',
        parameters=[
            OpenApiParameter(
                name='pk_publisher',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the publisher to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        responses={200: None, 404: None},
        description='Delete an existing publisher',
        operation_id='delete_publisher',
        parameters=[
            OpenApiParameter(
                name='pk_publisher',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the publisher to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def publisher_detail_wrapper(request, pk_publisher: int):

    match request.method:
        case 'GET':
            return publisher_detail(request, pk_publisher)

        case 'PUT':
            return edit_publisher(request, pk_publisher)

        case 'DELETE':
            return delete_publisher(request, pk_publisher)


@csrf_exempt
def publisher_detail(request, pk_publisher: int):
    try:
        publisher = get_object_or_404(Publisher, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

    serializer = PublisherSerializer(publisher, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_publisher(request, pk_publisher: int):
    payload = request.json
    name = payload['name']

    try:
        publisher = get_object_or_404(Publisher, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

    if name:
        publisher.name = name


    publisher.save()
    return JsonResponse({'id': publisher.pk}, status=200)


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_publisher(request, pk_publisher: int):
    try:
        publisher = get_object_or_404(Publisher, pk=pk_publisher)
    except Http404:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

    publisher.delete()
    return JsonResponse(status=200)


# Edition methods


@extend_schema_view(
    get=extend_schema(
        responses={200: EditionSchemaSerializer, 404: None},
        description='Get all editions',
        operation_id='get_editions',
    ),
    post=extend_schema(
        request=SaveEditionSchemaSerializer,
        responses={
            200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
            400: None,
            404: None,
        },
        description='Create a new edition',
        operation_id='add_edition',
    ),
)
@api_view(['GET', 'POST'])
@csrf_exempt
def edition_wrapper(request):

    match request.method:
        case 'GET':
            return edition_list(request)

        case 'POST':
            return add_edition(request)


@csrf_exempt
def edition_list(request):
    editions = Edition.objects.all()
    serializer = EditionSerializer(editions, request=request)
    return serializer.json_response()


@csrf_exempt
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


@extend_schema_view(
    get=extend_schema(
        responses={200: EditionSchemaSerializer, 404: None},
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
    ),
    put=extend_schema(
        request=SaveEditionSchemaSerializer,
        responses={
            200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
            400: None,
            404: None,
        },
        description='Update an existing edition',
        operation_id='update_edition',
        parameters=[
            OpenApiParameter(
                name='pk_edition',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the edition to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        responses={200: None, 404: None},
        description='Delete an existing edition',
        operation_id='delete_edition',
        parameters=[
            OpenApiParameter(
                name='pk_edition',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the edition to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def edition_detail_wrapper(request, pk_edition: int):

    match request.method:
        case 'GET':
            return edition_detail(request, pk_edition)

        case 'PUT':
            return edit_edition(request, pk_edition)

        case 'DELETE':
            return delete_edition(request, pk_edition)


@csrf_exempt
def edition_detail(request, pk_edition: int):
    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)

    serializer = EditionSerializer(edition, request=request)
    return serializer.json_response()


@csrf_exempt
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


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_edition(request, pk_edition: int):
    try:
        edition = get_object_or_404(Edition, pk=pk_edition)
    except Http404:
        return JsonResponse({'error': 'Edition not found'}, status=404)

    edition.delete()
    return JsonResponse(status=200)


# Region methods


@extend_schema_view(
    get=extend_schema(
        responses={200: RegionSchemaSerializer, 404: None},
        description='Get all regions',
        operation_id='get_regions',
    ),
)
@api_view(['GET'])
@csrf_exempt
def region_wrapper(request):

    match request.method:
        case 'GET':
            return region_list(request)


@csrf_exempt
def region_list(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, request=request)
    return serializer.json_response()


@extend_schema_view(
    get=extend_schema(
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
    ),
    put=extend_schema(
        request=SaveRegionSchemaSerializer,
        responses={200: {'type': 'object', 'properties': {'id': {'type': 'integer'}}}, 404: None},
        description='Update an existing region',
        operation_id='update_region',
        parameters=[
            OpenApiParameter(
                name='pk_region',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the region to update',
                required=True,
            ),
        ],
    ),
    delete=extend_schema(
        responses={200: None, 404: None},
        description='Delete an existing region',
        operation_id='delete_region',
        parameters=[
            OpenApiParameter(
                name='pk_region',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the region to delete',
                required=True,
            ),
        ],
    ),
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def region_detail_wrapper(request, pk_region: int):

    match request.method:
        case 'GET':
            return region_detail(request, pk_region)

        case 'PUT':
            return edit_region(request, pk_region)

        case 'DELETE':
            return delete_region(request, pk_region)


@csrf_exempt
def region_detail(request, pk_region: int):
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    serializer = RegionSerializer(region, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_region(request, pk_region: int):
    payload = request.json
    name = payload['name']
    acronym = payload['acronym']
   
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    if name:
        region.name = name

    if acronym:
        region.acronym = acronym

    region.save()
    return JsonResponse({'id': region.pk}, status=200)


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_region(request, pk_region: int):
    try:
        region = get_object_or_404(Region, pk=pk_region)
    except Http404:
        return JsonResponse({'error': 'Region not found'}, status=404)

    region.delete()
    return JsonResponse(status=200)
