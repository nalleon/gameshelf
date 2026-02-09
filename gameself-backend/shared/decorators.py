import json
from http import HTTPStatus

from django.http import JsonResponse


def require_http_methods(*methods):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse(
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
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def require_fields(*fields):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for field in fields:
                if field not in request.json:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator