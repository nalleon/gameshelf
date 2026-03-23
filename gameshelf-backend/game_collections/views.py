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

from .models import Collection, CollectionItem, WishListItem
from .serializers import (
    CollectionItemSchemaSerializer,
    CollectionItemSerializer,
    CollectionSerializer,
    SaveListSchemaSerializer,
    WishlistItemSerializer,
    CollectionSchemaSerializer,
    WishlistSchemaSerializer,
    SaveCollectionItemSchemaSerializer
)

User = get_user_model()


@extend_schema(
    request=SaveListSchemaSerializer,
    responses={
        201: CollectionSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Create a new collection for the authenticated user',
    operation_id='create_collection',
)
@api_view(['POST'])
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


# This method is public to get all items from a collection
@extend_schema(
    responses={200: CollectionSchemaSerializer, 404: None},
    description='Get all collections',
    operation_id='get_collections',
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def collection_list(request):
    collections = Collection.objects.all()
    serializer = CollectionSerializer(collections, request=request)
    return serializer.json_response()


# This method is public to get all items from a collection
@extend_schema(
    responses=CollectionSchemaSerializer,
    description='Get all items from a collection',
    parameters=[
        OpenApiParameter(
            name='pk_collection',
            description='ID of the collection',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
)
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def collection_item_list(request, pk_collection):
    collection = get_object_or_404(Collection, pk=pk_collection)
    serializer = CollectionSerializer(collection, request=request)
    return JsonResponse(serializer.serialize(), safe=False)


# This method is public to get an item form a collection
@extend_schema(
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
@api_view(['GET'])
@csrf_exempt
@require_http_methods('GET')
def collection_item_detail(request, pk_collection: int, pk_collection_item: int):
    
    collection = get_object_or_404(Collection, pk=pk_collection)

    collection_item = get_object_or_404(
        CollectionItem,
        pk=pk_collection_item,
        collection=collection
    )

    serializer = CollectionItemSerializer(collection_item, request=request)
    return serializer.json_response()


# This method is public to add to its own collection
@extend_schema(
    request=SaveCollectionItemSchemaSerializer,
    responses={
        201: CollectionItemSchemaSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        403: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Add a game to your own collection',
    parameters=[
        OpenApiParameter(
            name='pk_collection',
            description='ID of the collection',
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
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

    collection_item = CollectionItem.objects.create(
        game=game,
        collection=collection
    )

    return JsonResponse({'id': collection_item.pk}, status=201)


# This method is for admins, to add for other users
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game', 'pk_author')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_collection_item(request):
    payload = request.json
    pk_game = payload['pk_game']
    pk_author = payload['pk_author']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    try:
        author = get_object_or_404(User, pk=pk_author)
    except Http404:
        return JsonResponse({'error': 'User not found'}, status=404)

    collection_item = CollectionItem.objects.create(game=game, author=author)
    return JsonResponse({'id': collection_item.pk}, status=200)


# This method is for admin only, a user only wants to add or delete from collection
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_collection_item(request, pk_collection_item: int):
    payload = request.json
    pk_game = payload['pk_game']
    pk_author = payload['pk_author']

    try:
        collection_item = get_object_or_404(CollectionItem, pk=pk_collection_item)
    except Http404:
        return JsonResponse({'error': 'CollectionItem not found'}, status=404)

    if pk_game:
        try:
            game = get_object_or_404(Game, pk=pk_game)
        except Http404:
            return JsonResponse({'error': 'Game not found'}, status=404)
        collection_item.game = game

    if pk_author:
        try:
            author = get_object_or_404(User, pk=pk_author)
        except Http404:
            return JsonResponse({'error': 'User not found'}, status=404)
        collection_item.author = author

    collection_item.save()
    return JsonResponse({'id': collection_item.pk}, status=200)


# This method is public to delete an item of a collection
@csrf_exempt
@require_http_methods('POST')
@auth_required
def delete_collection_item(request, pk_collection_item: int):

    try:
        collection_item = get_object_or_404(CollectionItem, pk=pk_collection_item)
    except Http404:
        return JsonResponse({'error': 'CollectionItem not found'}, status=404)

    if collection_item.author != request.user:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    collection_item.delete()
    return JsonResponse(status=200)


# WishlistItem Methods
@csrf_exempt
@require_http_methods('GET')
def wishlist_item_list(request):
    wishlist_items = WishListItem.objects.all()
    serializer = WishlistItemSerializer(wishlist_items, request=request)
    return serializer.json_response()


# This method is public to see an wishlist item
@csrf_exempt
@require_http_methods('GET')
def wishlist_item_detail(request, pk_wishlist_item: int):
    try:
        wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    except Http404:
        return JsonResponse({'error': 'WishListItem not found'}, status=404)

    serializer = WishlistItemSerializer(wishlist_item, request=request)
    return serializer.json_response()


# This method is public to add to its own wishlist
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game', 'priority', 'annotation')
@auth_required
def add_self_wishlist_item(request):
    payload = request.json
    pk_game = payload['pk_game']
    priority = payload['priority']
    annotation = payload['annotation']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    author = request.user

    wishlist_item = WishListItem.objects.create(
        priority=priority, annotation=annotation, game=game, author=author
    )
    return JsonResponse({'id': wishlist_item.pk}, status=200)


# This method is for admins, to add for other users
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game', 'pk_author', 'priority', 'annotation')
@auth_required
@require_role(Profile.Role.ADMIN)
def add_wishlist_item(request):
    payload = request.json
    pk_game = payload['pk_game']
    priority = payload['priority']
    annotation = payload['annotation']
    pk_author = payload['pk_author']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)

    try:
        author = get_object_or_404(User, pk=pk_author)
    except Http404:
        return JsonResponse({'error': 'User not found'}, status=404)

    wishlist_item = WishListItem.objects.create(
        priority=priority, annotation=annotation, game=game, author=author
    )
    return JsonResponse({'id': wishlist_item.pk}, status=200)


# This method is for admin only, a user only wants to add or delete from wishlist
@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role(Profile.Role.ADMIN)
def edit_wishlist_item(request, pk_wishlist_item: int):
    payload = request.json
    pk_game = payload['pk_game']
    priority = payload['priority']
    annotation = payload['annotation']
    pk_author = payload['pk_author']

    try:
        wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    except Http404:
        return JsonResponse({'error': 'CollectionItem not found'}, status=404)

    if pk_game:
        try:
            game = get_object_or_404(Game, pk=pk_game)
        except Http404:
            return JsonResponse({'error': 'Game not found'}, status=404)
        wishlist_item.game = game

    if pk_author:
        try:
            author = get_object_or_404(User, pk=pk_author)
        except Http404:
            return JsonResponse({'error': 'User not found'}, status=404)
        wishlist_item.author = author

    if priority:
        wishlist_item.priority = priority

    if annotation:
        wishlist_item.annotation = annotation

    wishlist_item.save()
    return JsonResponse({'id': wishlist_item.pk}, status=200)


# This method is public to delete a wishlist collection
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def delete_wishlist_item(request, pk_wishlist_item: int):
    try:
        wishlist_item = get_object_or_404(WishListItem, pk=pk_wishlist_item)
    except Http404:
        return JsonResponse({'error': 'WishListItem not found'}, status=404)

    if wishlist_item.author != request.user:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    wishlist_item.delete()
    return JsonResponse(status=200)
