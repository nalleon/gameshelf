from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from shared.decorators import require_fields, require_json_body, require_role
from users.decorators import auth_required
from users.models import Profile

from .models import LibraryItem
from .serializers import LibraryItemSerializer

User = get_user_model()


@csrf_exempt
def library_item_list(request):
    library_items = LibraryItem.objects.all()
    serializer = LibraryItemSerializer(library_items, request=request)
    return serializer.json_response()


@csrf_exempt
def library_item_detail(request, pk_library_item: int):
    try:
        library_item = get_object_or_404(LibraryItem, pk=pk_library_item)
    except Http404:
        return JsonResponse({'error': 'LibraryItem not found'}, status=404)

    serializer = LibraryItemSerializer(library_item, request=request)
    return serializer.json_response()


@csrf_exempt
@require_json_body
@require_fields('status', 'pk_game', 'hours_played', 'created_at', 'updated_at', 'pk_author')
@auth_required
# @require_role(Profile.Role.ADMIN)
def add_library_item(request):
    payload = request.json
    status = payload['status']
    pk_game = payload['pk_game']
    hours_played = payload['hours_played']
    created_at = payload['created_at']
    updated_at = payload['updated_at']
    pk_author = payload['pk_author']

    try:
        game = get_object_or_404(Game, pk=pk_game)
    except Http404:
        return JsonResponse({'error': 'Game associated not found'}, status=404)

    try:
        author = get_object_or_404(User, pk=pk_author)
    except Http404:
        return JsonResponse({'error': 'Author associated not found'}, status=404)

    library_item = LibraryItem.objects.create(
        status=status,
        game=game,
        hours_played=hours_played,
        created_at=created_at,
        updated_at=updated_at,
        author=author,
    )
    return JsonResponse({'id': library_item.pk}, status=200)


@csrf_exempt
@require_json_body
@require_fields('status', 'pk_game', 'hours_played', 'created_at', 'updated_at', 'pk_author')
@auth_required
# @require_role(Profile.Role.ADMIN)
def edit_library_item(request, pk_library_item: int):
    payload = request.json
    status = payload['status']
    pk_game = payload['pk_game']
    hours_played = payload['hours_played']
    created_at = payload['created_at']
    updated_at = payload['updated_at']
    pk_author = payload['pk_author']

    try:
        library_item = get_object_or_404(LibraryItem, pk=pk_library_item)
    except Http404:
        return JsonResponse({'error': 'LibraryItem not found'}, status=404)

    if status:
        library_item.status = status

    if pk_game:
        try:
            game = get_object_or_404(Game, pk=pk_game)
        except Http404:
            return JsonResponse({'error': 'Game to associate not found'}, status=404)

        library_item.game = game

    if hours_played:
        library_item.hours_played = hours_played

    if created_at:
        library_item.created_at = created_at

    if updated_at:
        library_item.updated_at = updated_at

    if pk_author:
        try:
            author = get_object_or_404(User, pk=pk_author)
        except Http404:
            return JsonResponse({'error': 'Author to associate not found'}, status=404)

        library_item.author = author

    library_item.save()
    return JsonResponse({'id': library_item.pk}, status=200)


@csrf_exempt
@auth_required
@require_role(Profile.Role.ADMIN)
def delete_library_item(request, pk_library_item: int):
    try:
        library_item = get_object_or_404(LibraryItem, pk=pk_library_item)
    except Http404:
        return JsonResponse({'error': 'LibraryItem not found'}, status=404)

    library_item.delete()
    return JsonResponse(status=200)
