from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.decorators import api_view
from games.models import Game
from shared.decorators import require_fields, require_json_body, require_role
from users.decorators import auth_required
from users.models import Profile
from django.db.models import Q, Prefetch, Count
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import LibraryItem, Library
from .serializers import LibraryItemSerializer, LibrarySerializer, LibrarySchemaSerializer, LibraryItemSchemaSerializer
from django.http import HttpResponse
from shared.serializers import ErrorResponseSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        description='Get own library',
        responses={200: LibrarySerializer},
    ),
    patch=extend_schema(
        description='Edit own library',
        request=LibrarySchemaSerializer,
        responses={
            200: LibrarySerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
        },
    ),
    post=extend_schema(
        description='Add item to library',
        request=LibraryItemSchemaSerializer,
        responses={
            201: LibraryItemSerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    ),
)
@api_view(['GET', 'PATCH', 'POST'])
def library_wrapper(request):
    match request.method:
        case 'GET':
            return get_own_library(request)
        case 'PATCH':
            return edit_own_library(request)
        case 'POST':
            return add_library_item(request)
        
@csrf_exempt
@auth_required
def get_own_library(request):
    library = get_library_with_items(request.user, request.user)

    serializer = LibrarySerializer(library, request=request)
    return JsonResponse(serializer.serialize())

@csrf_exempt
@require_json_body
@require_fields('is_private')
@auth_required
def edit_own_library(request):
    library = request.user.library

    library.is_private = request.json['is_private']
    library.save()

    serializer = LibrarySerializer(library, request=request)
    return JsonResponse(serializer.serialize())

@csrf_exempt
@require_json_body
@require_fields('game_id', 'status', 'is_private')
@auth_required
def add_library_item(request):
    library = request.user.library

    game = get_object_or_404(Game, pk=request.json['game_id'])

    if LibraryItem.objects.filter(
        library=library,
        game=game,
        deleted_at__isnull=True
    ).exists():
        return JsonResponse({'error': 'Game already in library'}, status=400)


    item = LibraryItem.objects.create(
        library=library,
        game=game,
        status=request.json['status'],
        is_private=request.json['is_private'],
        hours_played=request.json.get('hours_played', 0)
    )

    return JsonResponse({'id': item.pk}, status=201)


@extend_schema_view(
    get=extend_schema(
        description='Get library item',
        responses={
            200: LibraryItemSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    ),
    patch=extend_schema(
        description='Edit library item',
        request=LibraryItemSchemaSerializer,
        responses={
            200: LibraryItemSerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    ),
    delete=extend_schema(
        description='Delete library item',
        responses={
            204: None,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
    ),
)
@api_view(['GET', 'PATCH', 'DELETE'])
def library_detail_wrapper(request, pk_item: int):
    match request.method:
        case 'GET':
            return get_library_item(request, pk_item)

        case 'PATCH':
            return edit_library_item(request, pk_item)

        case 'DELETE':
            return delete_library_item(request, pk_item)
        

      
    
@csrf_exempt
def get_library_item(request, pk_item):
    item = get_object_or_404(LibraryItem, pk=pk_item)

    is_owner = request.user == item.library.user

    if item.is_private and not is_owner:
        raise PermissionDenied()

    serializer = LibraryItemSerializer(item, request=request)
    return JsonResponse(serializer.serialize())

@csrf_exempt
@require_json_body
@auth_required
def edit_library_item(request, pk_item: int):
    item = get_object_or_404(LibraryItem, pk=pk_item)

    if item.library.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    payload = request.json
    updated = False

    if 'status' in payload and payload['status'] != item.status:
        item.status = payload['status']
        updated = True

    if 'hours_played' in payload and payload['hours_played'] != item.hours_played:
        item.hours_played = payload['hours_played']
        updated = True

    if 'is_private' in payload and payload['is_private'] != item.is_private:
        item.is_private = payload['is_private']
        updated = True

    if updated:
        item.save()

    serializer = LibraryItemSerializer(item, request=request)
    return JsonResponse(serializer.serialize())

@csrf_exempt
def delete_library_item(request, pk_item):
    item = get_object_or_404(LibraryItem, pk=pk_item)

    if item.library.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    item.delete()
    return HttpResponse(status=204)

@extend_schema(
    responses={200: LibrarySerializer},
    description='Get a user library (public or own depending on permissions)',
    operation_id='get_library',
    parameters=[
        OpenApiParameter(
            name='pk_user',
            description='ID of the user whose library is being requested',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_library(request, pk_user):
    user = get_object_or_404(User, pk=pk_user)

    library = get_library_with_items(user, request.user)

    if not library:
        return JsonResponse(
            {'error': 'Library not accessible'}, 
            status=404
        )

    serializer = LibrarySerializer(library, request=request)
    return JsonResponse(serializer.serialize())
  
# Aux methods

def get_library_with_items(user_owner, requester):
    qs = Library.objects.filter(user=user_owner)

    is_owner = requester.is_authenticated and requester == user_owner

    if not is_owner:
        qs = qs.filter(is_private=False)

    qs = qs.annotate(
        total_all=Count('items', filter=Q(items__deleted_at__isnull=True)),
        total_public=Count(
            'items',
            filter=Q(items__deleted_at__isnull=True, items__is_private=False)
        ),
        total_private=Count(
            'items',
            filter=Q(items__deleted_at__isnull=True, items__is_private=True)
        ),
    )

    items_qs = LibraryItem.objects.filter(
        deleted_at__isnull=True,
        is_private=False if not is_owner else Q()
    )

    library = qs.prefetch_related(
        Prefetch('items', queryset=items_qs)
    ).first()

    return library