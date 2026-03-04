"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/', auth, name='auth'),
    # path('api/users/', include('users.urls')),
    path('api/games/', include('games.games_urls')),
    path('api/reviews/', include('games.reviews_urls')),
    path('api/medias/', include('games.medias_urls')),
    path('api/favorite/', include('games.favorite_items_urls')),
    path('api/platforms/', include('classifications.platforms_urls')),
    path('api/genres/', include('classifications.genres_urls')),
    path('api/developers/', include('classifications.developers_urls')),
    path('api/publishers/', include('classifications.publishers_urls')),
    path('api/regions/', include('classifications.regions_urls')),
    path('api/editions/', include('classifications.editions_urls')),
    path('api/libraries/', include('libraries.urls')),
    path('api/collections/', include('game_collections.collections_urls')),
    path('api/wishlist/', include('game_collections.wishlists_urls')),
]
