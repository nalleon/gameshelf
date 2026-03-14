from django.urls import path

from . import views

# app_name = 'genres'

urlpatterns = [
    path('', views.genre_list, name='genre-list'),
    path('add/', views.add_genre, name='add-genre'),
    path('<int:pk_genre>/', views.genre_detail, name='genre-detail'),
    path('<int:pk_genre>/delete/', views.delete_genre, name='delete-genre'),
    path('<int:pk_genre>/edit/', views.edit_genre, name='edit-genre'),
]
