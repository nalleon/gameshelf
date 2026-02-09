import json

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def auth(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    try:
        username = payload['username']
        password = payload['password']
    except KeyError:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if user := authenticate(username=username, password=password):
        try:
            return JsonResponse({'token': user.token.key})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Token not found'}, status=404)

    return JsonResponse({'error': 'Invalid credentials'}, status=401)