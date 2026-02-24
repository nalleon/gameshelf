from django.urls import path

from . import views

# app_name = 'favorite'

urlpatterns = [
    path('', views.favorite_item_list, name='favorite_item-list'),
    path('add/', views.add_favorite_item, name='add-favorite_item'),
    path('self-add/', views.add_self_favorite_item, name='add-self-favorite_item'),
    path('<int:pk_favorite_item>/', views.favorite_item_detail, name='favorite_item-detail'),
    path('<int:pk_favorite_item>/delete/', views.delete_favorite_item, name='delete-favorite_item'),
    path('<int:pk_favorite_item>/edit/', views.edit_favorite_item, name='edit-favorite_item'),
]
