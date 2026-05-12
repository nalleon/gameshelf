from django.urls import path

from . import views

# app_name = 'favorite'

urlpatterns = [
    # path('', views.favorites_wrapper, name='favorites-wrapper'),
    path('<int:pk_favorite>/', views.favorites_detail_wrapper, name='favorites-detail-wrapper'),
    path('toggle/', views.toggle_favorite, name='favorites-toggle'), # Falta por añadir en swagger
    path('user/<int:user_pk>/', views.favorites_wrapper, name='user-favorites'),
]
