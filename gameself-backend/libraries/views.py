from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import LibraryItem


from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
from users.decorators import auth_required


@csrf_exempt
@require_http_methods('GET')
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def platform_detail(request, pk_platform: int):
    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)

    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields('name', 'description')
@auth_required
@require_role('Admin')
def add_platform(request):
    payload = request.json
    name = payload['name']
    description = payload['description']

    platform = Platform.objects.create(name=name, description=description)
    return JsonResponse({'id': platform.pk}, status=200)

@csrf_exempt
@require_http_methods('PUT')
@require_json_body
@auth_required
@require_role('Admin')
def edit_platform(request, pk_platform : int):
    payload = request.json
    name = payload['name']
    description = payload['description']

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    
    if name:
        platform.name = name

    if description:
        platform.description = description

    platform.save()
    return JsonResponse({'id': platform.pk}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_role('Admin')
def delete_platform(request, pk_platform : int):

    try:
        platform = get_object_or_404(Platform, pk=pk_platform)
    except Http404:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    
    platform.delete()
    return JsonResponse(status=200)