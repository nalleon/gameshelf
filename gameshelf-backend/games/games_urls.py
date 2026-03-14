from django.urls import path

from . import views

# app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('add/', views.add_game, name='add-game'),
    path('<int:pk_game>/', views.game_detail, name='game-detail'),
    path('<int:pk_game>/delete/', views.delete_game, name='delete-game'),
    path('<int:pk_game>/edit/', views.edit_game, name='edit-game'),
]
