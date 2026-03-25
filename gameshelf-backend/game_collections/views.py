from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view

from games.models import Game
from shared.decorators import require_fields, require_http_methods, require_json_body, require_role
from users.decorators import auth_required
from users.models import Profile

from .models import Collection, CollectionItem, WishListItem, Wishlist
from .serializers import (
    CollectionItemSchemaSerializer,
    CollectionItemSerializer,
    CollectionSchemaSerializer,
    CollectionSerializer,
    SaveCollectionItemSchemaSerializer,
    SaveListSchemaSerializer,
    WishlistItemSerializer,
)

User = get_user_model()

#############################
# Collection methods
#############################


# Method for making the API restful
@extend_schema(
    responses={200: CollectionSchemaSerializer, 404: None},
    description='Get all collections',
    operation_id='get_collections',
)
@extend_schema(
    request=SaveListSchemaSerializer,
    responses={
        201: CollectionSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Create a new collection for the authenticated user',
    operation_id='create_collection',
)
@api_view(['GET', 'POST'])
@require_http_methods('GET', 'POST')
def collection_wrapper(request):
    match request.method:
        case 'GET':
            return collection_list(request)
        case 'POST':
            return create_collection(request)


# This method is public to get all existing collections
@csrf_exempt
def collection_list(request):
    collections = Collection.objects.all()
    serializer = CollectionSerializer(collections, request=request)
    return serializer.json_response()


# This method is public to create a new collection collection
@csrf_exempt
@require_json_body
@require_fields('name')
@auth_required
def create_collection(request):
    payload = request.json
    name = payload['name']

    collection = Collection.objects.create(
        user=request.user,
        name=name,
    )

    serializer = CollectionSerializer(collection, request=request)
    return JsonResponse(serializer.serialize(), status=201)


# Method for making the API restful
@extend_schema(
    responses=CollectionSchemaSerializer,
    description='Get all items from a collection',
)
@extend_schema(
    request=SaveCollectionItemSchemaSerializer,
    responses={
        201: CollectionItemSchemaSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        403: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Add a game to your own collection',
)
@extend_schema(
    request=None,
    responses={
        204: None,
        403: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Delete a game from your collection',
    parameters=[
        OpenApiParameter(
            name='pk_collection',
            description='ID of the collection',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
)
@extend_schema(
    methods=['PATCH'],
    request={
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'is_private': {'type': 'boolean'}
        },
        'required': [],
    },
    responses=CollectionSerializer,
    description='Edit the name and/or is_private of a collection',
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@csrf_exempt
@require_http_methods('GET', 'POST', 'DELETE', 'PATCH')
def collection_items_wrapper(request, pk_collection):
    match request.method:
        case 'GET':
            return collection_item_list(request, pk_collection)
        case 'POST':
            return add_self_collection_item(request, pk_collection)
        case 'DELETE':
            return delete_collection(request, pk_collection)
        case 'PATCH':
            return edit_collection(request, pk_collection)

# This method is public to get all items from a collection
@csrf_exempt
@require_http_methods('GET')
def collection_item_list(request, pk_collection):
    collection = get_object_or_404(Collection, pk=pk_collection)
    serializer = CollectionSerializer(collection, request=request)
    return JsonResponse(serializer.serialize(), safe=False)


# This method is public to add to its own collection
@csrf_exempt
@require_json_body
@require_fields('game_id')
@auth_required
def add_self_collection_item(request, pk_collection):
    payload = request.json
    pk_game = payload['game_id']

    collection = get_object_or_404(Collection, pk=pk_collection)

    if collection.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    game = get_object_or_404(Game, pk=pk_game)

    collection_item = CollectionItem.objects.create(game=game, collection=collection)

    return JsonResponse({'id': collection_item.pk}, status=201)


# This method is public to delete a collection
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_collection(request, pk_collection: int):
    try:
        collection = get_object_or_404(Collection, pk=pk_collection)
    except Http404:
        return JsonResponse({'error': 'Collection not found'}, status=404)

    if collection.user != request.user:
        return JsonResponse({'error': 'Forbidden access'}, status=403)

    collection.delete()
    return JsonResponse(status=204)

@require_json_body
@require_fields('name', 'is_private')
@auth_required
def edit_collection(request, pk_collection: int):
    collection = get_object_or_404(Collection, pk=pk_collection)

    if collection.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    payload = request.json
    name = payload['name']
    is_private = payload['is_private']

    collection.name = name
    collection.is_private = is_private
   
    collection.save()

    serializer = CollectionSerializer(collection, request=request)
    return JsonResponse(serializer.serialize())


# Method for making the API restful
@extend_schema(
    methods=['GET'],
    responses=CollectionItemSchemaSerializer,
    description='Get an item from a collection',
    parameters=[
        OpenApiParameter(
            name='pk_collection',
            description='ID of the collection',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name='pk_collection_item',
            description='ID of the collection item',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
)
@extend_schema(
    methods=['DELETE'],
    request=None,
    responses={
        204: None,
        403: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Delete a game from your collection',
    parameters=[
        OpenApiParameter(
            name='pk_collection',
            description='ID of the collection',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name='pk_collection_item',
            description='ID of the collection item',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
)
@extend_schema(
    methods=['PATCH'],
    request={
        'type': 'object',
        'properties': {
            'is_private': {'type': 'boolean'}
        },
        'required': [],
    },
    responses=CollectionItemSchemaSerializer,
    description='Edit the is_private field of a collection item',
)
@api_view(['GET', 'DELETE', 'PATCH'])
@csrf_exempt
@require_http_methods('GET', 'DELETE', 'PATCH')
def collection_item_detail_wrapper(request, pk_collection: int, pk_collection_item: int):
    match request.method:
        case 'GET':
            return collection_item_detail(request, pk_collection, pk_collection_item)
        case 'DELETE':
            return delete_collection_item(request, pk_collection, pk_collection_item)
        case 'PATCH':
            return edit_collection_item(request, pk_collection, pk_collection_item)


# This method is public to get an item form a collection
@csrf_exempt
def collection_item_detail(request, pk_collection: int, pk_collection_item: int):

    collection = get_object_or_404(Collection, pk=pk_collection)

    collection_item = get_object_or_404(
        CollectionItem, pk=pk_collection_item, collection=collection
    )

    serializer = CollectionItemSerializer(collection_item, request=request)
    return serializer.json_response()


# This method is public to delete an item of a collection
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_collection_item(request, pk_collection: int, pk_collection_item: int):
    try:
        collection_item = get_object_or_404(
            CollectionItem, pk=pk_collection_item, collection_id=pk_collection
        )
    except Http404:
        return JsonResponse({'error': 'CollectionItem not found'}, status=404)

    if collection_item.collection.user != request.user:
        return JsonResponse({'error': 'Forbidden access'}, status=403)

    collection_item.delete()
    return JsonResponse(status=204)

@require_json_body
@require_fields('is_private')
@auth_required
def edit_collection_item(request, pk_collection: int, pk_collection_item: int):
    collection_item = get_object_or_404(
        CollectionItem,
        pk=pk_collection_item,
        collection_id=pk_collection
    )

    collection = collection_item.collection

    if collection.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    payload = request.json
    is_private = payload['is_private']
    
    if is_private != collection_item.is_private:
        collection_item.is_private = is_private
        collection_item.save()

    serializer = CollectionItemSerializer(collection_item, request=request)
    return serializer.json_response()


#############################
# Wishlist methods
#############################

# Wrapper para la wishlist del usuario
@extend_schema(
    responses={200: CollectionSchemaSerializer},
    description='Get the authenticated user wishlist',
    operation_id='get_wishlist',
)
@extend_schema(
    request=SaveListSchemaSerializer,
    responses={
        201: CollectionSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Create the wishlist for the authenticated user (only one allowed)',
    operation_id='create_wishlist',
)
@api_view(['GET', 'POST'])
@require_http_methods('GET', 'POST')
@auth_required
def wishlist_wrapper(request):
    match request.method:
        case 'GET':
            return wishlist_detail(request)
        case 'POST':
            return create_wishlist(request)


@csrf_exempt
@auth_required
def wishlist_detail(request):
    # Solo hay una wishlist por usuario
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    serializer = CollectionSerializer(wishlist, request=request)
    return JsonResponse(serializer.serialize())


@csrf_exempt
@require_json_body
@require_fields('name', 'is_private')
@auth_required
def create_wishlist(request):
    if Wishlist.objects.filter(user=request.user).exists():
        return JsonResponse({'error': 'User already has a wishlist'}, status=400)

    payload = request.json
    wishlist = Wishlist.objects.create(
        user=request.user,
        name=payload['name'],
        is_private=payload['is_private']
    )
    serializer = CollectionSerializer(wishlist, request=request)
    return JsonResponse(serializer.serialize(), status=201)


# Wrapper para items de la wishlist
@extend_schema(
    responses=CollectionSchemaSerializer,
    description='Get all items from the wishlist',
)
@extend_schema(
    request=SaveCollectionItemSchemaSerializer,
    responses={
        201: CollectionItemSchemaSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        403: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Add a game to the wishlist',
)
@extend_schema(
    methods=['PATCH'],
    request={
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'is_private': {'type': 'boolean'}
        },
        'required': [],
    },
    responses=CollectionSerializer,
    description='Edit the name and/or is_private of the wishlist',
)
@api_view(['GET', 'POST', 'PATCH'])
@csrf_exempt
@require_http_methods('GET', 'POST', 'PATCH')
@auth_required
def wishlist_items_wrapper(request, pk_wishlist: int):
    wishlist = get_object_or_404(Wishlist, pk=pk_wishlist)

    if wishlist.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    match request.method:
        case 'GET':
            return ''
        case 'POST':
            return add_self_wishlist_item(request, wishlist)
        case 'PATCH':
            return edit_wishlist(request, wishlist)


@csrf_exempt
@require_json_body
@require_fields('game_id', 'priority', 'annotation')
@auth_required
def add_self_wishlist_item(request, wishlist: Wishlist):
    payload = request.json
    pk_game = payload['game_id']
    priority = payload['priority']
    annotation = payload['annotation']

    game = get_object_or_404(Game, pk=pk_game)

    wishlist_item = WishListItem.objects.create(
        wishlist=wishlist,
        game=game,
        priority=priority,
        annotation=annotation
    )
    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return JsonResponse(serializer.serialize(), status=201)


@require_json_body
@auth_required
def edit_wishlist(request, wishlist: Wishlist):
    payload = request.json
    updated = False

    if 'name' in payload:
        wishlist.name = payload['name']
        updated = True
    if 'is_private' in payload:
        wishlist.is_private = payload['is_private']
        updated = True

    if updated:
        wishlist.save()

    serializer = CollectionSerializer(wishlist, request=request)
    return JsonResponse(serializer.serialize())


# Wrapper para item individual de la wishlist
@extend_schema(
    methods=['GET'],
    responses=WishlistItemSerializer,
    description='Get a wishlist item',
)
@extend_schema(
    methods=['DELETE'],
    request=None,
    responses={
        204: None,
        403: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Delete a wishlist item',
)
@extend_schema(
    methods=['PATCH'],
    request={
        'type': 'object',
        'properties': {
            'priority': {'type': 'integer'},
            'annotation': {'type': 'string'},
            'is_private': {'type': 'boolean'},
        },
        'required': [],
    },
    responses=WishlistItemSerializer,
    description='Edit a wishlist item (priority, annotation, is_private)',
)
@api_view(['GET', 'DELETE', 'PATCH'])
@csrf_exempt
@require_http_methods('GET', 'DELETE', 'PATCH')
@auth_required
def wishlist_item_detail_wrapper(request, pk_wishlist_item: int):
    match request.method:
        case 'GET':
            return wishlist_item_detail(request, pk_wishlist_item)
        case 'DELETE':
            return delete_wishlist_item(request, pk_wishlist_item)
        case 'PATCH':
            return edit_wishlist_item(request, pk_wishlist_item)


@csrf_exempt
@require_http_methods('GET')
@auth_required
def wishlist_item_detail(request, pk_wishlist_item: int):
    wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    if wishlist_item.wishlist.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return JsonResponse(serializer.serialize())


@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_wishlist_item(request, pk_wishlist_item: int):
    wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    if wishlist_item.wishlist.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    wishlist_item.delete()
    return JsonResponse(status=204)


@csrf_exempt
@require_json_body
@auth_required
def edit_wishlist_item(request, pk_wishlist_item: int):
    wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    if wishlist_item.wishlist.user != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    payload = request.json
    updated = False
    if 'priority' in payload:
        wishlist_item.priority = payload['priority']
        updated = True
    if 'annotation' in payload:
        wishlist_item.annotation = payload['annotation']
        updated = True
    if 'is_private' in payload:
        wishlist_item.is_private = payload['is_private']
        updated = True

    if updated:
        wishlist_item.save()

    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return JsonResponse(serializer.serialize())