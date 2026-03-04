import json

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model


from .models import Profile
from games.models import Game, FavoriteItem
from .serializers import ProfileSerializer, ProfileSerializer
from games.serializers import GameSerializer, ReviewSerializer, FavoriteItemSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
from users.decorators import auth_required


@csrf_exempt
def auth(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    try:
        profilename = payload['profilename']
        password = payload['password']
    except KeyError:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if profile := authenticate(profilename=profilename, password=password):
        try:
            return JsonResponse({'token': profile.token.key})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Token not found'}, status=404)

    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@csrf_exempt
def user_login():
    return


@csrf_exempt
def user_register():
    return


@csrf_exempt
def user_logout():
    return


# Profile Methods
@csrf_exempt
@require_http_methods('GET')
def profile_list(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def profile_detail(request, pk_profile: int):
    try:
        profile = get_object_or_404(Profile, pk=pk_profile)
    except Http404:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()

# @csrf_exempt
# @require_http_methods('POST')
# @require_json_body
# @require_fields('name', 'description')
# @auth_required
# @require_role('Admin')
# def add_profile(request):
#     payload = request.json
#     name = payload['name']
#     description = payload['description']

#     profile = Profile.objects.create(name=name, description=description)
#     return JsonResponse({'id': profile.pk}, status=200)

# @csrf_exempt
# @require_http_methods('PUT')
# @require_json_body
# @auth_required
# @require_role('Admin')
# def edit_profile(request, pk_profile : int):
#     payload = request.json
#     name = payload['name']
#     description = payload['description']

#     try:
#         profile = get_object_or_404(Profile, pk=pk_profile)
#     except Http404:
#         return JsonResponse({'error': 'Profile not found'}, status=404)
    
#     if name:
#         profile.name = name

#     if description:
#         profile.description = description

#     profile.save()
#     return JsonResponse({'id': profile.pk}, status=200)


# @csrf_exempt
# @require_http_methods('POST')
# @auth_required
# @require_role('Admin')
# def delete_profile(request, pk_profile : int):

#     try:
#         profile = get_object_or_404(Profile, pk=pk_profile)
#     except Http404:
#         return JsonResponse({'error': 'Profile not found'}, status=404)
    
#     profile.delete()
#     return JsonResponse(status=200)