from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model


from .models import Item, CollectionItem, WishListItem 
from games.models import Game
from .serializers import ItemSerializer, CollectionItemSerializer, WishlistItemSerializer
from games.serializers import GameSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
from users.decorators import auth_required

User = get_user_model()

# CollectionItem Methods
@csrf_exempt
@require_http_methods('GET')
def collection_item_list(request):
    collection_items = CollectionItem.objects.all()
    serializer = CollectionItemSerializer(collection_items, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def collection_item_detail(request, pk_collection_item: int):
    try:
        collection_item = get_object_or_404(CollectionItem, pk=pk_collection_item)
    except Http404:
        return JsonResponse({'error': 'CollectionItem not found'}, status=404)

    serializer = CollectionItemSerializer(collection_item, request=request)
    return serializer.json_response()

# This method is public to add to its own library
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game')
@auth_required
def add_to_self_collection_item(request):
    payload = request.json
    pk_game = payload['pk_game']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    author = request.user

    collection_item = CollectionItem.objects.create(game=game, author=author)
    return JsonResponse({'id': collection_item.pk}, status=200)

# This method is for admins, to add for other users
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('pk_game', 'pk_author')
@auth_required
@require_role('Admin')
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
@require_role('Admin')
def edit_collection_item(request, pk_collection_item : int):
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


@csrf_exempt
@require_http_methods('POST')
@auth_required
def delete_collection_item(request, pk_collection_item : int):

    try:
        collection_item = get_object_or_404(CollectionItem, pk=pk_collection_item)
    except Http404:
        return JsonResponse({'error': 'CollectionItem not found'}, status=404)
    
    if collection_item.author != request.user:
        if request.user.role != 'Admin':
            return JsonResponse({'error': 'Forbbiden Access'}, status=403)

    collection_item.delete()
    return JsonResponse(status=200)