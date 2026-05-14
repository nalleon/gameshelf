from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch, Q
from django.http import Http404, HttpResponse
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.decorators import api_view

from classifications.models import Platform
from games.models import Game
from shared.decorators import require_fields, require_json_body
from shared.serializers import ErrorResponseSerializer
from users.decorators import auth_required

from .models import Collection, CollectionItem, Item, Wishlist, WishListItem
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
            return own_collection_list(request)
        case 'POST':
            return create_collection(request)


# This method is public to get all existing collections
@csrf_exempt
def own_collection_list(request):
    collections = get_collections_queryset(request.user)
    serializer = CollectionSerializer(collections, request=request)
    return serializer.json_response()


# This method is public to create a new collection collection
@csrf_exempt
@require_json_body
@require_fields('name', 'is_private')
@auth_required
def create_collection(request):
    payload = request.json
    name = payload['name']
    is_private = payload['is_private']
    collection = Collection.objects.create(user=request.user, name=name, is_private=is_private)

    serializer = CollectionSerializer(collection, request=request)
    return Response(serializer.serialize(), status=201)


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
        responses={200: CollectionSchemaSerializer},
        description='Edit the name and/or is_private of a collection',
        operation_id='edit_collection',
    ),
)
@api_view(['POST', 'DELETE', 'PATCH'])
@csrf_exempt
def collection_items_wrapper(request, pk_collection):
    match request.method:
        # case 'GET':
        #     return collection_item_list(request, pk_collection, pk_user)
        case 'POST':
            return add_self_collection_item(request, pk_collection)
        case 'DELETE':
            return delete_collection(request, pk_collection)
        case 'PATCH':
            return edit_collection(request, pk_collection)


# This method is public to get all items from a collection
@api_view(['GET'])
@csrf_exempt
@auth_required
def collection_item_list(request, pk_collection, pk_user):
    user = get_object_or_404(User, pk=pk_user)
    collection = get_collection_with_items(pk_collection, user)
    serializer = CollectionSerializer(collection, request=request)
    return serializer.json_response()


# This method is public to add to its own collection
@csrf_exempt
@require_json_body
@require_fields('game_id', 'platform_id', 'is_private', 'type')
@auth_required
def add_self_collection_item(request, pk_collection):
    payload = request.json
    pk_game = payload['game_id']
    is_private = payload['is_private']
    item_type = payload['type']
    platform_id = payload['platform_id']
    collection = get_object_or_404(Collection, pk=pk_collection)

    if collection.user != request.user:
        return Response({'error': 'Forbidden'}, status=403)

    game = get_object_or_404(Game, pk=pk_game)

    if not game.platforms.filter(id=platform_id).exists():
        return Response(
            {'error': 'This game is not available on the selected platform'}, status=400
        )

    platform = get_object_or_404(Platform, pk=platform_id)

    try:
        validate_item_type_for_game(game, item_type)
    except ValueError as e:
        return Response({'error': str(e)}, status=400)

    exists = CollectionItem.objects.filter(
        collection=collection, game=game, platform=platform, type=item_type, deleted_at__isnull=True
    ).exists()

    if exists:
        return Response({'error': 'Game already exists in collection'}, status=400)

    collection_item = CollectionItem.objects.create(
        game=game, collection=collection, platform=platform, is_private=is_private, type=item_type
    )

    return Response({'id': collection_item.pk}, status=201)


# This method is public to delete a collection
@csrf_exempt
@auth_required
def delete_collection(request, pk_collection: int):
    try:
        collection = get_object_or_404(Collection, pk=pk_collection)
    except Http404:
        return Response({'error': 'Collection not found'}, status=404)

    if collection.user != request.user:
        return Response({'error': 'Forbidden access'}, status=403)

    collection.delete()
    return HttpResponse(status=204)


@require_json_body
@require_fields('name', 'is_private')
@auth_required
def edit_collection(request, pk_collection: int):
    collection = get_object_or_404(Collection, pk=pk_collection)

    if collection.user != request.user:
        return Response({'error': 'Forbidden'}, status=403)

    payload = request.json
    name = payload['name']
    is_private = payload['is_private']

    collection.name = name
    collection.is_private = is_private

    collection.save()

    serializer = CollectionSerializer(collection, request=request)
    return Response(serializer.serialize())


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
    is_owner = request.user.is_authenticated and request.user == collection.user

    if collection.is_private and not is_owner:
        return Response({'error': 'Forbidden'}, status=403)

    collection_item = get_object_or_404(
        CollectionItem,
        pk=pk_collection_item,
        collection=collection,
        deleted_at__isnull=True,
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
        return Response({'error': 'CollectionItem not found'}, status=404)

    if collection_item.collection.user != request.user:
        return Response({'error': 'Forbidden access'}, status=403)

    collection_item.delete()
    return HttpResponse(status=204)


@require_json_body
@require_fields('is_private', 'type', 'platform_id')
@auth_required
def edit_collection_item(request, pk_collection: int, pk_collection_item: int):
    collection_item = get_object_or_404(
        CollectionItem, pk=pk_collection_item, collection_id=pk_collection
    )

    collection = collection_item.collection

    if collection.user != request.user:
        return Response({'error': 'Forbidden'}, status=403)

    payload = request.json
    is_private = payload['is_private']
    item_type = payload['type']
    platform_id = payload['platform_id']

    game = get_object_or_404(Game, pk=collection_item.game.pk)

    if not game.platforms.filter(id=platform_id).exists():
        return Response(
            {'error': 'This game is not available on the selected platform'}, status=400
        )

    platform = get_object_or_404(Platform, pk=platform_id)

    try:
        validate_item_type_for_game(game, item_type)
    except ValueError as e:
        return Response({'error': str(e)}, status=400)

    updated = False

    if is_private != collection_item.is_private:
        collection_item.is_private = is_private
        updated = True

    if item_type != collection_item.type:
        collection_item.type = item_type
        updated = True

    if platform != collection_item.platform:
        collection_item.platform = platform
        updated = True

    if updated:
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
    wishlist = get_wishlist_with_items(request.user.wishlist.pk, request.user)

    serializer = WishlistSerializer(wishlist, request=request)
    return Response(serializer.serialize())


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
@auth_required
def get_wishlist(request, pk_wishlist: int):
    wishlist = get_wishlist_with_items(pk_wishlist, request.user)

    serializer = WishlistSerializer(wishlist, request=request)
    return Response(serializer.serialize(), status=200)


@csrf_exempt
@require_json_body
@require_fields('game_id', 'platform_id', 'priority', 'annotation', 'is_private', 'type')
@auth_required
def add_self_wishlist_item(request, pk_wishlist: int):
    wishlist = check_wishlist_ownership(request.user, pk_wishlist)

    payload = request.json
    pk_game = payload['game_id']
    priority = payload['priority']
    annotation = payload['annotation']
    is_private = payload['is_private']
    item_type = payload['type']
    platform_id = payload['platform_id']

    game = get_object_or_404(Game, pk=pk_game)

    if not game.platforms.filter(id=platform_id).exists():
        return Response(
            {'error': 'This game is not available on the selected platform'}, status=400
        )

    platform = get_object_or_404(Platform, pk=platform_id)

    try:
        validate_item_type_for_game(game, item_type)
    except ValueError as e:
        return Response({'error': str(e)}, status=400)

    if WishListItem.objects.filter(
        wishlist=wishlist, game=game, type=item_type, platform=platform, deleted_at__isnull=True
    ).exists():
        return Response({'error': 'Game already exists in wishlist'}, status=400)

    wishlist_item = WishListItem.objects.create(
        wishlist=wishlist,
        game=game,
        platform=platform,
        priority=priority,
        annotation=annotation,
        is_private=is_private,
        type=item_type,
    )
    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return Response(serializer.serialize(), status=201)


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

    wishlist = get_wishlist_with_items(pk_wishlist, request.user)

    serializer = WishlistSerializer(wishlist, request=request)
    return Response(serializer.serialize(), status=200)


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

    is_owner = request.user.is_authenticated and request.user == wishlist_item.wishlist.user

    if wishlist_item.is_private and not is_owner:
        raise PermissionDenied('Forbidden')

    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return Response(serializer.serialize())


@csrf_exempt
@auth_required
def delete_wishlist_item(request, pk_wishlist_item: int):
    wishlist_item = check_wishlistitem_ownership(request.user, pk_wishlist_item)
    wishlist_item.delete()
    return HttpResponse(status=204)


@csrf_exempt
@require_json_body
@require_fields('priority', 'platform_id', 'annotation', 'is_private', 'type')
@auth_required
def edit_wishlist_item(request, pk_wishlist_item: int):

    wishlist_item = check_wishlistitem_ownership(request.user, pk_wishlist_item)

    payload = request.json
    updated = False

    game = get_object_or_404(Game, pk=wishlist_item.game.pk)
    if not game.platforms.filter(id=payload['platform_id']).exists():
        return Response(
            {'error': 'This game is not available on the selected platform'}, status=400
        )

    platform = get_object_or_404(Platform, pk=payload['platform_id'])

    try:
        validate_item_type_for_game(game, payload['type'])
    except ValueError as e:
        return Response({'error': str(e)}, status=400)

    if 'priority' in payload:
        wishlist_item.priority = payload['priority']
        updated = True
    if 'annotation' in payload:
        wishlist_item.annotation = payload['annotation']
        updated = True
    if 'is_private' in payload:
        wishlist_item.is_private = payload['is_private']
        updated = True
    if platform != wishlist_item.platform:
        wishlist_item.platform = platform
        updated = True

    if updated:
        wishlist_item.save()

    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return Response(serializer.serialize())


######################################
# Auxiliar methods
######################################


def check_wishlist_ownership(user, pk_wishlist):
    wishlist = get_object_or_404(Wishlist, pk=pk_wishlist)

    if wishlist.user != user:
        raise PermissionDenied('Forbidden')

    return wishlist


def check_wishlistitem_ownership(user, pk_wishlist_item):
    wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    if wishlist_item.wishlist.user != user:
        raise PermissionDenied('Forbidden')
    return wishlist_item


# def get_collections_queryset(user):
#     qs = Collection.objects.all()

#     if not user.is_authenticated:
#         qs = qs.filter(is_private=False)
#         items_qs = CollectionItem.objects.filter(deleted_at__isnull=True, is_private=False)
#     else:
#         qs = qs.filter(Q(is_private=False) | Q(user=user))

#         items_qs = CollectionItem.objects.filter(deleted_at__isnull=True)

#     return qs.annotate(
#         total_all=Count('items', filter=Q(items__deleted_at__isnull=True)),
#         total_public=Count(
#             'items', filter=Q(items__deleted_at__isnull=True, items__is_private=False)
#         ),
#         total_private=Count(
#             'items', filter=Q(items__deleted_at__isnull=True, items__is_private=True)
#         ),
#     ).prefetch_related(Prefetch('items', queryset=items_qs))

def get_collections_queryset(user):
    # Si el usuario no está autenticado, no debería ver colecciones "propias"
    if not user.is_authenticated:
        return Collection.objects.none()

    # Filtramos ESTRICTAMENTE por el usuario autenticado
    qs = Collection.objects.filter(user=user)
    
    # Traemos solo los ítems que no estén borrados de esas colecciones
    items_qs = CollectionItem.objects.filter(deleted_at__isnull=True)

    return qs.annotate(
        total_all=Count('items', filter=Q(items__deleted_at__isnull=True)),
        total_public=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=False)
        ),
        total_private=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=True)
        ),
    ).prefetch_related(Prefetch('items', queryset=items_qs))


def get_collection_with_items(pk_collection, user):
    collection_qs = Collection.objects.filter(pk=pk_collection)

    is_owner = user.is_authenticated and collection_qs.filter(user=user).exists()

    if not is_owner:
        collection_qs = collection_qs.filter(is_private=False)

    collection_qs = collection_qs.annotate(
        total_all=Count('items', filter=Q(items__deleted_at__isnull=True)),
        total_public=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=False)
        ),
        total_private=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=True)
        ),
    )

    if is_owner:
        items_qs = CollectionItem.objects.filter(deleted_at__isnull=True)
    else:
        items_qs = CollectionItem.objects.filter(deleted_at__isnull=True, is_private=False)

    collection = collection_qs.prefetch_related(Prefetch('items', queryset=items_qs)).first()

    if not collection:
        raise PermissionDenied()

    return collection


def get_wishlist_queryset(user):
    qs = Wishlist.objects.filter(user=user)

    if not user.is_authenticated:
        qs = qs.filter(is_private=False)
        items_qs = WishListItem.objects.filter(deleted_at__isnull=True, is_private=False)
    else:
        qs = qs.filter(Q(is_private=False) | Q(user=user))

        items_qs = WishListItem.objects.filter(deleted_at__isnull=True)

    return qs.annotate(
        total_all=Count('items', filter=Q(items__deleted_at__isnull=True)),
        total_public=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=False)
        ),
        total_private=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=True)
        ),
    ).prefetch_related(Prefetch('items', queryset=items_qs))


def get_wishlist_with_items(pk_wishlist, user):
    wishlist_qs = Wishlist.objects.filter(pk=pk_wishlist)

    is_owner = user.is_authenticated and wishlist_qs.filter(user=user).exists()

    if not is_owner:
        wishlist_qs = wishlist_qs.filter(is_private=False)

    wishlist_qs = wishlist_qs.annotate(
        total_all=Count('items', filter=Q(items__deleted_at__isnull=True)),
        total_public=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=False)
        ),
        total_private=Count(
            'items', filter=Q(items__deleted_at__isnull=True, items__is_private=True)
        ),
    )

    if is_owner:
        items_qs = WishListItem.objects.filter(deleted_at__isnull=True)
    else:
        items_qs = WishListItem.objects.filter(deleted_at__isnull=True, is_private=False)

    wishlist = wishlist_qs.prefetch_related(Prefetch('items', queryset=items_qs)).first()

    if not wishlist:
        raise PermissionDenied()

    return wishlist


def validate_item_type_for_game(game, item_type):
    only_digital_keywords = {'pc', 'mobile'}

    platform_names = [p.name.lower() for p in game.platforms.all()]

    def is_only_digital(name: str) -> bool:
        return any(keyword in name for keyword in only_digital_keywords)

    if platform_names and all(is_only_digital(name) for name in platform_names):
        if item_type != Item.Type.DIGITAL:
            raise ValueError('This game can only be added as Digital')
