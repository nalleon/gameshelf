from django.urls import path

from . import views

# app_name = 'games'

urlpatterns = [
    path('', views.game_wrapper, name='game-wrapper'),
    path('<int:pk_game>/', views.game_detail_wrapper, name='game-detail-wrapper'),
    path('igbd/', views.igdb_wrapper, name='igdb_wrapper'),

]
