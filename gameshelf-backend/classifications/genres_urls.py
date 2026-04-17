from django.urls import path

from . import views

# app_name = 'genres'

urlpatterns = [
    path('', views.genre_wrapper, name='genre-wrapper'),
    path('<int:pk_genre>/', views.genre_detail_wrapper, name='genre-detail-wrapper'),
]
