from django.urls import path

from . import views


# app_name = 'game_collections'

urlpatterns = [
    path('', views.collection_wrapper, name='collection_wrapper'),
    path('<int:pk_collection>/', views.collection_items_wrapper, name='collection_items_wrapper'),
    path('<int:pk_collection>/items/<int:pk_collection_item>/', views.collection_item_detail_wrapper, name='collection_item_detail_wrapper'),
]
