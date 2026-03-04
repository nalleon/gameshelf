from django.urls import path

from . import views


# app_name = 'game_collections'

urlpatterns = [
    path('', views.collection_item_list, name='collection_item-list'),
    path('add/', views.add_collection_item, name='add-collection_item'),
    path('self-add/', views.add_self_collection_item, name='add-self-collection_item'),
    path('<int:pk_collection_item>/', views.collection_item_detail, name='collection_item-detail'),
    path('<int:pk_collection_item>/delete/', views.delete_collection_item, name='delete-collection_item'),
    path('<int:pk_collection_item>/edit/', views.edit_collection_item, name='edit-collection_item'),
]
