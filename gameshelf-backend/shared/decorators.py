import json
from http import HTTPStatus

from rest_framework.response import Response

def require_http_methods(*methods):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return Response(
                    {'error': 'Method not allowed'}, status=HTTPStatus.METHOD_NOT_ALLOWED
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_json_body(func):
    def wrapper(request, *args, **kwargs):
        try:
            request.json = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON body'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def require_fields(*fields):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for field in fields:
                if field not in request.json:
                    return Response({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_role(expected_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            profile = getattr(request.user, 'profile', None)
            if profile is None:
                return Response({'error': 'User profile not found'}, status=403)

            if profile.role != expected_role:
                return Response({'error': 'Forbidden Access'}, status=403)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
