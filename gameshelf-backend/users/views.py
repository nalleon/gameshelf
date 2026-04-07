import json

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.decorators import api_view


from .models import Profile
from games.models import Game, FavoriteItem
from .serializers import ProfileSerializer, LoginSchemaSerializer, RegisterSchemaSerializer
from games.serializers import GameSerializer, ReviewSerializer, FavoriteItemSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
from users.decorators import auth_required
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@extend_schema(
    request=RegisterSchemaSerializer,
    responses={
        201: {
            'type': 'object',
            'properties': {
                'token': {'type': 'string'}
            }
        },
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Register a new user',
    operation_id='register',
    methods=['POST']
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('username', 'password', 'email')
def user_register(request):

    payload = request.json

    username = payload['username']
    password = payload['password']
    email = payload['email']

    first_name = payload.get('first_name')
    last_name = payload.get('last_name')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    if email and User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name or "",
        last_name=last_name or "",
        email=email
    )

    Profile.objects.create(user=user)
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "token": str(refresh.access_token)
    }, status=201)
    
@extend_schema(
    request=LoginSchemaSerializer,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'token': {'type': 'string'}
            }
        },
        401: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    description='Login with a user',
    operation_id='login',
    methods=['POST']
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('login', 'password')
def user_login(request):

    payload = request.json

    login = payload['login']
    password = payload['password']

    user = None

    if "@" in login:
        user = User.objects.filter(email=login).first()
        if user:
            user = authenticate(username=user.username, password=password)
    else:
        user = authenticate(username=login, password=password)

    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "token": str(refresh.access_token)
    }, status=201)
    

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
# @require_role(Profile.Role.ADMIN)
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
# @require_role(Profile.Role.ADMIN)
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
# @require_role(Profile.Role.ADMIN)
# def delete_profile(request, pk_profile : int):

#     try:
#         profile = get_object_or_404(Profile, pk=pk_profile)
#     except Http404:
#         return JsonResponse({'error': 'Profile not found'}, status=404)
    
#     profile.delete()
#     return JsonResponse(status=200)