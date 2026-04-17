from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.decorators import api_view

from games.models import Game
from shared.decorators import require_fields, require_json_body
from shared.serializers import ErrorResponseSerializer
from users.decorators import auth_required

from .models import Collection, CollectionItem, Wishlist, WishListItem
from .serializers import (
    CollectionItemSchemaSerializer,
    CollectionItemSerializer,
    CollectionSchemaSerializer,
    CollectionSerializer,
    CreateWishlistItemSchemaSerializer,
    SaveCollectionItemSchemaSerializer,
    SaveListSchemaSerializer,
    UpdateWishlistItemSchemaSerializer,
    WishlistItemSchemaSerializer,
    WishlistItemSerializer,
    WishlistSchemaSerializer,
    WishlistSerializer,
)

User = get_user_model()

#############################
# Collection methods
#############################


# Method for making the API restful
@extend_schema(
    responses={200: CollectionSchemaSerializer, 404: None},
    description='Get all collections',
    operation_id='get_all_collections',
)
@extend_schema(
    request=SaveListSchemaSerializer,
    responses={
        201: CollectionSerializer,
        400: ErrorResponseSerializer,
    },
    description='Create a new collection for the authenticated user',
    operation_id='create_collection',
)
@api_view(['GET', 'POST'])
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


@extend_schema_view(
    get=extend_schema(
        responses={200: CollectionSchemaSerializer},
        description='Get all items from a collection',
        parameters=[
            OpenApiParameter(
                name='pk_collection',
                description='ID of the collection',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        operation_id='get_collection',
    ),
    post=extend_schema(
        request=SaveCollectionItemSchemaSerializer,
        responses={
            201: CollectionItemSchemaSerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description='Add a game to your own collection',
        operation_id='add_collection',
    ),
    delete=extend_schema(
        request=None,
        responses={
            204: None,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
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
        operation_id='delete_collection',
    ),
    patch=extend_schema(
        request=SaveListSchemaSerializer,
        responses={200: CollectionSerializer},
        description='Edit the name and/or is_private of a collection',
        operation_id='edit_collection',
    ),
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@csrf_exempt
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
@extend_schema_view(
    get=extend_schema(
        responses={200: CollectionItemSchemaSerializer},
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
        operation_id='get_collection_items',
    ),
    delete=extend_schema(
        request=None,
        responses={
            204: None,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
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
        operation_id='delete_collection_item',
    ),
    patch=extend_schema(
        request={
            'type': 'object',
            'properties': {'is_private': {'type': 'boolean'}},
        },
        responses={200: CollectionItemSchemaSerializer},
        description='Edit the is_private field of a collection item',
        operation_id='update_collection_item',
    ),
)
@api_view(['GET', 'DELETE', 'PATCH'])
@csrf_exempt
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
        CollectionItem, pk=pk_collection_item, collection_id=pk_collection
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


# Method for making the API restful
@extend_schema(
    responses={200: WishlistSchemaSerializer},
    description='Get the authenticated user wishlist',
    operation_id='get_own_wishlist',
)
@api_view(['GET'])
@auth_required
def wishlist_wrapper(request):
    match request.method:
        case 'GET':
            return own_wishlist_detail(request)


@csrf_exempt
@auth_required
def own_wishlist_detail(request):
    wishlist = request.user.wishlist
    serializer = CollectionSerializer(wishlist, request=request)
    return JsonResponse(serializer.serialize())


# Method for making the API restful
@extend_schema_view(
    get=extend_schema(
        responses={200: WishlistSchemaSerializer},
        description='Get all items from the wishlist',
        parameters=[
            OpenApiParameter(
                name='pk_wishlist',
                description='ID of the wishlist',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        operation_id='get_wishlist',
    ),
    post=extend_schema(
        request=CreateWishlistItemSchemaSerializer,
        responses={
            201: WishlistItemSchemaSerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        },
        description='Add a game to the wishlist',
        operation_id='add_wishlist_item',
    ),
    patch=extend_schema(
        request=SaveListSchemaSerializer,
        responses={200: WishlistSerializer},
        description='Edit the name and/or is_private of the wishlist',
        operation_id='edit_wishlist',
    ),
)
@api_view(['GET', 'POST', 'PATCH'])
@csrf_exempt
@auth_required
def wishlist_items_wrapper(request, pk_wishlist: int):
    match request.method:
        case 'GET':
            return get_wishlist(request, pk_wishlist)
        case 'POST':
            return add_self_wishlist_item(request, pk_wishlist)
        case 'PATCH':
            return edit_wishlist(request, pk_wishlist)


@csrf_exempt
def get_wishlist(request, pk_wishlist: int):
    wishlist = get_object_or_404(Wishlist, pk=pk_wishlist)
    serializer = CollectionSerializer(wishlist, request=request)

    return JsonResponse(serializer.serialize(), status=201)


@csrf_exempt
@require_json_body
@require_fields('game_id', 'priority', 'annotation')
@auth_required
def add_self_wishlist_item(request, pk_wishlist: int):
    wishlist = check_wishlist_ownership(request.user, pk_wishlist)

    payload = request.json
    pk_game = payload['game_id']
    priority = payload['priority']
    annotation = payload['annotation']

    game = get_object_or_404(Game, pk=pk_game)

    wishlist_item = WishListItem.objects.create(
        wishlist=wishlist, game=game, priority=priority, annotation=annotation
    )
    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return JsonResponse(serializer.serialize(), status=201)


@require_json_body
@require_fields('name', 'is_private')
@auth_required
def edit_wishlist(request, pk_wishlist: int):
    wishlist = check_wishlist_ownership(request.user, pk_wishlist)

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

    serializer = WishlistSerializer(wishlist, request=request)
    return JsonResponse(serializer.serialize())


@extend_schema(
    methods=['GET'],
    responses={200: WishlistItemSchemaSerializer},
    description='Get a wishlist item',
    operation_id='get_wishlist_item',
)
@extend_schema(
    methods=['DELETE'],
    request=None,
    responses={
        204: None,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    description='Delete a wishlist item',
    operation_id='delete_wishlist_item',
)
@extend_schema(
    methods=['PATCH'],
    request=UpdateWishlistItemSchemaSerializer,
    responses={200: WishlistItemSchemaSerializer},
    description='Edit a wishlist item (priority, annotation, is_private)',
    operation_id='update_wishlist_item',
)
@api_view(['GET', 'DELETE', 'PATCH'])
@csrf_exempt
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
@auth_required
def wishlist_item_detail(request, pk_wishlist_item: int):
    wishlist_item = check_wishlistitem_ownership(request.user, pk_wishlist_item)
    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return JsonResponse(serializer.serialize())


@csrf_exempt
@auth_required
def delete_wishlist_item(request, pk_wishlist_item: int):
    wishlist_item = check_wishlistitem_ownership(request.user, pk_wishlist_item)
    wishlist_item.delete()
    return JsonResponse(status=204)


@csrf_exempt
@require_json_body
@require_fields('priority', 'annotation', 'is_private')
@auth_required
def edit_wishlist_item(request, pk_wishlist_item: int):

    wishlist_item = check_wishlistitem_ownership(request.user, pk_wishlist_item)

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


######################################
# Auxiliar methods
######################################


def check_wishlist_ownership(user, pk_wishlist):
    wishlist = get_object_or_404(Wishlist, pk=pk_wishlist)

    if wishlist.user != user:
        return JsonResponse({'error': 'Forbidden'}, status=403)


def check_wishlistitem_ownership(user, pk_wishlist_item):
    wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    if wishlist_item.wishlist.user != user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
