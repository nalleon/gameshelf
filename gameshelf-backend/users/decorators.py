from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


from functools import wraps

def auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return func(request, *args, **kwargs)

        try:
            jwt_auth = JWTAuthentication()
            user_auth_tuple = jwt_auth.authenticate(request)

            if user_auth_tuple is None:
                return Response({'error': 'Invalid authentication token'}, status=401)

            request.user, _ = user_auth_tuple

        except (InvalidToken, AuthenticationFailed):
            return Response({'error': 'Invalid authentication token'}, status=401)

        return func(request, *args, **kwargs)

    return wrapper