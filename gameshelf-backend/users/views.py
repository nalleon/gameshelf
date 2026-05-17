from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, OpenApiRequest, OpenApiTypes, extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from shared.decorators import require_fields, require_json_body
from shared.serializers import ErrorResponseSerializer, MessageResponseSerializer
from users.decorators import auth_required

from .models import Profile, UserToken
from .serializers import (
    ChangePasswordSerializer,
    EmailRequestSerializer,
    LoggedProfileSerializer,
    LoginSchemaSerializer,
    ProfileSerializer,
    RegisterSchemaSerializer,
    TokenResponseSerializer,
    UpdateProfileSerializer,
    ActivateAccountSerializer
)
from .tasks import (
    deliver_activation_email,
    deliver_password_reset_email,
    deliver_verification_email,
)

User = get_user_model()


# Profile Methods
@extend_schema(
    tags=['profile'],
    responses={
        200: ProfileSerializer,
        404: ErrorResponseSerializer,
    },
    description='Get profile detail from user token',
    operation_id='retrieveMyProfile',
)
@api_view(['GET'])
@csrf_exempt
@auth_required
def profile_me(request):
    profile = request.user.profile
    serializer = LoggedProfileSerializer(profile, request=request)
    return serializer.json_response()


@extend_schema(
    tags=['profile'],
    responses={200: ProfileSerializer},
    description='Get all profiles',
    operation_id='listProfiles',
)
@api_view(['GET'])
@csrf_exempt
def profile_wrapper(request):
    match request.method:
        case 'GET':
            return profile_list(request)


@csrf_exempt
def profile_list(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, request=request)
    return serializer.json_response()


@extend_schema(
    tags=['profile'],
    parameters=[
        OpenApiParameter(
            name='pk_profile',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Profile ID',
        )
    ],
    responses={
        200: LoggedProfileSerializer,
        404: ErrorResponseSerializer,
    },
    description='Get profile detail',
    operation_id='retrieveProfile',
)
@extend_schema(
    tags=['profile'],
    request=OpenApiRequest(
        request=UpdateProfileSerializer,
        encoding={
            'avatar': {'contentType': 'image/*'},
        },
    ),
    responses={
        200: LoggedProfileSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    description='Edit profile (partial update)',
    operation_id='editProfile',
)
@api_view(['GET', 'PATCH'])
@csrf_exempt
def profile_detail_wrapper(request, pk_profile: int):
    match request.method:
        case 'GET':
            return profile_detail(request, pk_profile)
        case 'PATCH':
            return profile_edit(request, pk_profile)


@csrf_exempt
def profile_detail(request, pk_profile: int):
    try:
        profile = get_object_or_404(Profile, pk=pk_profile)
    except Http404:
        return Response({'error': 'Profile not found'}, status=404)

    serializer = LoggedProfileSerializer(profile, request=request)
    return serializer.json_response()


@csrf_exempt
# @require_json_body
@auth_required
def profile_edit(request, pk_profile: int):

    try:
        profile = get_object_or_404(Profile, pk=pk_profile)
    except Http404:
        return Response({'error': 'Profile not found'}, status=404)

    if request.user != profile.user:
        return Response({'error': 'Forbidden'}, status=403)

    data = request.data
    files = request.FILES

    if 'library_private' in data:
        val = str(data['library_private']).lower() == 'true'
        library = request.user.library
        library.is_private = val
        library.save()

    # Procesamos Wishlist (OneToOne)
    if 'wishlist_private' in data:
        val = str(data['wishlist_private']).lower() == 'true'
        wishlist = request.user.wishlist
        wishlist.is_private = val
        wishlist.save()

    # Procesamos todas las Colecciones
    if 'collections_private' in data:
        val = str(data['collections_private']).lower() == 'true'
        request.user.collections.all().update(is_private=val)

    if 'bio' in data:
        profile.bio = data['bio']

    if 'avatar' in files:
        profile.avatar = files['avatar']

    if 'color_bg' in data and profile.verified:
        profile.color_bg = data['color_bg']

    user = profile.user

    if 'username' in data:
        if User.objects.filter(username=data['username']).exclude(pk=user.pk).exists():
            return Response({'error': 'Username already taken'}, status=400)
        user.username = data['username']

    if 'first_name' in data:
        user.first_name = data['first_name']

    if 'last_name' in data:
        user.last_name = data['last_name']

    profile.save()
    user.save()

    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


@extend_schema(
    tags=['profile'],
    parameters=[
        OpenApiParameter(
            name='q',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Search query (username, first name or last name)',
            required=True,
        )
    ],
    responses={200: ProfileSerializer},
    description='Search profiles by username or name',
    operation_id='searchProfiles',
)
@api_view(['GET'])
def search_by_name(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=400)

    profiles = Profile.objects.select_related('user').filter(
        Q(user__username__icontains=query)
        | Q(user__first_name__icontains=query)
        | Q(user__last_name__icontains=query)
    )

    serializer = ProfileSerializer(profiles, request=request)
    return serializer.json_response()


# Auth methods
@extend_schema(
    tags=['auth'],
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
# @require_fields('username', 'password', 'email')
def user_register(request):

    payload = request.data

    username = payload.get('username')
    password = payload.get('password')
    email = payload.get('email')

    first_name = payload.get('first_name', '')
    last_name = payload.get('last_name', '')
    avatar = request.FILES.get('avatar')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if email and User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    # Profile.objects.create(user=user, avatar=avatar if avatar else None)
    if avatar:
        Profile.objects.create(user=user, avatar=avatar)
    else:
        Profile.objects.create(user=user)

    refresh = RefreshToken.for_user(user)

    return Response({'token': str(refresh.access_token)}, status=201)


@extend_schema(
    tags=['auth'],
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
        return Response({'error': 'Invalid credentials'}, status=401)

    if hasattr(user, 'profile') and user.profile.deleted_at is not None:
        return Response({'error': 'Account is deactivated'}, status=403)

    refresh = RefreshToken.for_user(user)

    return Response({'token': str(refresh.access_token)}, status=201)


@extend_schema(
    tags=['auth'],
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
def request_password_reset(request):
    payload = request.json
    email = payload['email']

    user = User.objects.filter(email=email).first()

    if user:
        token = UserToken.objects.create(
            user=user,
            type=UserToken.TokenType.CHANGE_PASSWORD,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        deliver_password_reset_email.delay(user=user, token=str(token.token))

    return Response({'message': 'If account exists, email sent'})


@extend_schema(
    tags=['auth'],
    request=TokenResponseSerializer,
    responses={
        200: MessageResponseSerializer,
        400: ErrorResponseSerializer,
    },
    description='Validate password reset token',
    operation_id='validatePasswordResetToken',
)
@api_view(['POST'])
@require_json_body
@require_fields('token')
def validate_password_reset_token(request):

    token = request.json['token'].strip().upper()

    try:
        token_obj = UserToken.objects.get(token=token, type=UserToken.TokenType.CHANGE_PASSWORD)

    except UserToken.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=400)

    if not token_obj.is_valid():
        return Response({'error': 'Token expired'}, status=400)

    token_obj.validated = True
    token_obj.save(update_fields=['validated'])

    return Response({'message': 'Token valid'})


@extend_schema(
    tags=['auth'],
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
@require_json_body
@require_fields('token', 'new_password')
def change_password(request):
    payload = request.json
    token = payload['token']

    token = UserToken.objects.get(token=token, type=UserToken.TokenType.CHANGE_PASSWORD)
    if not token.validated:
        return Response({'error': 'Invalid token'}, status=401)

    user = token.user

    user.set_password(payload['new_password'])
    user.save()
    token.delete()

    return Response({'message': 'Password updated successfully'}, status=200)


@extend_schema(
    tags=['auth'],
    request=None,
    responses={
        200: MessageResponseSerializer,
        400: ErrorResponseSerializer,
    },
    description='Send verification email to the authenticated user',
    operation_id='sendVerificationEmail',
)
@api_view(['POST'])
@auth_required
def send_verification_email(request):
    user = request.user

    if user.profile.verified:
        return Response({'error': 'Account already verified'}, status=400)

    token = UserToken.objects.create(
        user=user,
        type=UserToken.TokenType.VERIFY_EMAIL,
        expires_at=timezone.now() + timedelta(minutes=10),
    )

    deliver_verification_email.delay(user=user, token=str(token.token))

    return Response({'message': 'Verification email sent'})


@extend_schema(
    tags=['auth'],
    request=TokenResponseSerializer,
    responses={
        200: MessageResponseSerializer,
        400: ErrorResponseSerializer,
    },
    description='Verify user email using 10-char code',
    operation_id='verifyEmail',
)
@api_view(['POST'])
@csrf_exempt
def verify_email(request):
    token = request.data.get('token')

    if not token:
        return Response({'error': 'Token is required'}, status=400)

    try:
        token_obj = UserToken.objects.get(token=token, type=UserToken.TokenType.VERIFY_EMAIL)
    except UserToken.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=400)

    if not token_obj.is_valid():
        return Response({'error': 'Token expired'}, status=400)

    profile = token_obj.user.profile
    profile.verified = True
    profile.save(update_fields=['verified'])

    token_obj.delete()

    return Response({'message': 'Email verified'})


@extend_schema(
    tags=['auth'],
    responses={
        200: MessageResponseSerializer,
        401: ErrorResponseSerializer,
        404: ErrorResponseSerializer
    },
    description='Deactivate account (soft delete profile)',
    operation_id='deactivateAccount',
)
@api_view(['DELETE'])
@csrf_exempt
@auth_required
def deactivate_account(request):
    user = request.user

    try:
        profile = user.profile
    except ObjectDoesNotExist:
        return Response({'error': 'Profile not found'}, status=404)

    if not profile.verified:
        return Response({'error': 'Profile not verified'}, status=401)

    profile.delete()

    return Response({'message': 'Account deactivated'}, status=200)


@extend_schema(
    tags=['auth'],
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

    profile = Profile.all_objects.select_related('user').filter(user__email=email).first()
    user = profile.user if profile else None

    if user:
        token = UserToken.objects.create(
            user=user,
            type=UserToken.TokenType.ACTIVATE_ACCOUNT,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        deliver_activation_email.delay(user=user, token=str(token.token))

    return Response({'message': 'If account exists, email sent'})


@extend_schema(
    tags=['auth'],
    request=ActivateAccountSerializer,
    responses={
        200: MessageResponseSerializer,
        400: ErrorResponseSerializer,
    },
    description='Restore previously deleted account using activation code',
    operation_id='restoreAccount',
)
@api_view(['POST'])
@require_json_body
@require_fields('token', 'email')
@csrf_exempt
def restore_account(request):
    payload = request.data

    token = payload.get('token', '').strip().upper()
    email = payload.get('email', '').strip().lower()

    try:
        token_obj = UserToken.objects.get(
            token=token,
            type=UserToken.TokenType.ACTIVATE_ACCOUNT,
            user__email=email
        )
    except UserToken.DoesNotExist:
        return Response({'error': 'Invalid token or email'}, status=400)

    if not token_obj.is_valid():
        return Response({'error': 'Token expired'}, status=400)

    profile = token_obj.user.profile

    if profile.deleted_at is None:
        return Response({'message': 'Account already active'}, status=200)

    profile.restore()
    token_obj.delete()

    return Response({'message': 'Account restored'}, status=200)