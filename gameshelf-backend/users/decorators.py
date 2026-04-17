from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

def auth_required(func):

    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        try:
            jwt_auth = JWTAuthentication()
            user_auth_tuple = jwt_auth.authenticate(request)
            if user_auth_tuple is None:
                raise AuthenticationFailed('Invalid authentication token')
            user, validated_token = user_auth_tuple

        except (InvalidToken, AuthenticationFailed):
            return JsonResponse({'error': 'Invalid authentication token'}, status=401)

        request.user = user
        return func(request, *args, **kwargs)

    return wrapper