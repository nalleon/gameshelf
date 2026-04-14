from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from shared.decorators import require_fields, require_http_methods, require_json_body
from users.decorators import auth_required

from .models import Profile, UserToken
from .serializers import LoginSchemaSerializer, ProfileSerializer, RegisterSchemaSerializer, TokenResponseSerializer, ChangePasswordSerializer, EmailRequestSerializer
from shared.serializers import MessageResponseSerializer, ErrorResponseSerializer
from django.utils import timezone
from datetime import timedelta
from .tasks import deliver_activation_email, deliver_password_reset_email, deliver_verification_email 

User = get_user_model()       

@extend_schema(
    tags=['Auth'],
    request=RegisterSchemaSerializer,
    responses={
        201: TokenResponseSerializer,
        400: ErrorResponseSerializer,
    },
    description='Register a new user',
    operation_id='registerUser',
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
        first_name=first_name or '',
        last_name=last_name or '',
        email=email,
    )

    Profile.objects.create(user=user)
    refresh = RefreshToken.for_user(user)

    return JsonResponse({'token': str(refresh.access_token)}, status=201)


@extend_schema(
    tags=['Auth'],
    request=LoginSchemaSerializer,
    responses={
        201: TokenResponseSerializer,
        401: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
    },
    description='Login with username or email',
    operation_id='loginUser',
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

    if '@' in login:
        user = User.objects.filter(email=login).first()
        if user:
            user = authenticate(username=user.username, password=password)
    else:
        user = authenticate(username=login, password=password)

    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    if hasattr(user, 'profile') and user.profile.deleted_at is not None:
        return JsonResponse({'error': 'Account is deactivated'}, status=403)

    refresh = RefreshToken.for_user(user)

    return JsonResponse({'token': str(refresh.access_token)}, status=201)


# Profile Methods
@extend_schema(
    tags=['Profile'],
    responses=ProfileSerializer,
    description='Get all profiles',
    operation_id='listProfiles',
)
@csrf_exempt
@require_http_methods('GET')
def profile_list(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, request=request)
    return serializer.json_response()

@extend_schema(
    tags=['Profile'],
    parameters=[
        OpenApiParameter(
            name='pk_profile',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Profile ID'
        )
    ],
    responses={
        200: ProfileSerializer,
        404: ErrorResponseSerializer,
    },
    description='Get profile detail',
    operation_id='retrieveProfile',
)
@csrf_exempt
@require_http_methods('GET')
def profile_detail(request, pk_profile: int):
    try:
        profile = get_object_or_404(Profile, pk=pk_profile)
    except Http404:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()

@extend_schema(
    tags=['Auth'],
    request=EmailRequestSerializer,
    responses={
        200: MessageResponseSerializer,
    },
    description='Request password reset email',
    operation_id='requestPasswordReset',
)
@api_view(['POST'])
@require_json_body
@require_fields('email')
# TODO: redirect to frontend
def request_password_reset(request):
    payload = request.json
    email = payload['email']

    user = User.objects.filter(email=email).first()

    if user:
        token = UserToken.objects.create(
            user=user,
            type=UserToken.TokenType.CHANGE_PASSWORD,
            expires_at=timezone.now() + timedelta(hours=1)
        )

        deliver_password_reset_email.delay(
            base_url=request.build_absolute_uri(),
            user=user,
            token=str(token.token)
        )

    return JsonResponse({'message': 'If account exists, email sent'})

@extend_schema(
    tags=['Auth'],
    request=ChangePasswordSerializer,
    responses={
        200: MessageResponseSerializer,
        400: ErrorResponseSerializer,
        401: ErrorResponseSerializer,
    },
    description='Change current user password',
    operation_id='changePassword',
)
@api_view(['POST'])
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('old_password', 'new_password')
@auth_required
def change_password(request):
    user = request.user
    payload = request.json

    if not user.check_password(payload['old_password']):
        return JsonResponse({'error': 'Invalid old password'}, status=400)

    user.set_password(payload['new_password'])
    user.save()
    UserToken.objects.filter(
        user=user,
        type=UserToken.TokenType.CHANGE_PASSWORD
    ).delete()

    return JsonResponse({'message': 'Password updated successfully'}, status=200)


@extend_schema(
    tags=['Auth'],
    request=None,
    responses={
        200: MessageResponseSerializer,
        401: ErrorResponseSerializer,
    },
    description='Send verification email to the authenticated user',
    operation_id='sendVerificationEmail',
)
@api_view(['POST'])
@auth_required
def send_verification_email(request):
    user = request.user

    token = UserToken.objects.create(
        user=user,
        type=UserToken.TokenType.VERIFY_EMAIL,
        expires_at=timezone.now() + timedelta(hours=24)
    )

    deliver_verification_email.delay(
        base_url=request.build_absolute_uri(),
        user=user,
        token=str(token.token)
    )

    return JsonResponse({'message': 'Verification email sent'})


@csrf_exempt
def verify_email(request, token):
    try:
        token_obj = UserToken.objects.get(
            token=token,
            type=UserToken.TokenType.VERIFY_EMAIL
        )
    except UserToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    if not token_obj.is_valid():
        return JsonResponse({'error': 'Token expired'}, status=400)

    profile = token_obj.user.profile
    profile.verified = True
    profile.save(update_fields=['verified'])

    token_obj.delete()

    return JsonResponse({'message': 'Email verified'})


@extend_schema(
    tags=['Auth'],
    responses={
        200: MessageResponseSerializer,
        401: ErrorResponseSerializer,
    },
    description='Deactivate account (soft delete profile)',
    operation_id='deactivateAccount',
)
@api_view(['DELETE'])
@csrf_exempt
@require_http_methods('DELETE')
@auth_required
def deactivate_account(request):
    user = request.user

    try:
        profile = user.profile
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    profile.delete()
    
    return JsonResponse({'message': 'Account deactivated'}, status=200)

@extend_schema(
    tags=['Auth'],
    request=EmailRequestSerializer,
    responses={
        200: MessageResponseSerializer,
    },
    description='Send account activation email if the account exists',
    operation_id='sendActivationEmail',
)
@api_view(['POST'])
@require_json_body
@require_fields('email')
def send_activation_email(request):
    email = request.json['email']

    profile = Profile.all_objects.select_related('user').filter(
        user__email=email
    ).first()

    user = profile.user if profile else None

    if user:
        token = UserToken.objects.create(
            user=user,
            type=UserToken.TokenType.ACTIVATE_ACCOUNT,
            expires_at=timezone.now() + timedelta(hours=24)
        )

        deliver_activation_email.delay(
            base_url=request.build_absolute_uri(),
            user=user, 
            token=str(token.token)
        )

    return JsonResponse({'message': 'If account exists, email sent'})


@csrf_exempt
def restore_account(request, token):
    try:
        token_obj = UserToken.objects.get(
            token=token,
            type=UserToken.TokenType.VERIFY_EMAIL
        )
    except UserToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    if not token_obj.is_valid():
        return JsonResponse({'error': 'Token expired'}, status=400)

    profile = token_obj.user.profile
    token_obj.delete()

    if profile.deleted_at is None:
        return JsonResponse({'message': 'Account already active'}, status=200)

    profile.restore()
    token_obj.delete()
    
    return JsonResponse({'message': 'Account restored'}, status=200)


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


