from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from .models import Game, Review, Media, FavoriteItem
from .serializers import GameSerializer, ReviewSerializer, MediaSerializer, FavoriteItemSerializer

from shared.decorators import require_http_methods, require_fields, require_json_body, require_role
from users.decorators import auth_required