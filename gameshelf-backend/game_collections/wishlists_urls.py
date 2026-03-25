from django.urls import path

from . import views

# app_name = 'game_collections'

urlpatterns = [
    path('', views.wishlist_wrapper, name='wishlist_wrapper'),
    path('<int:pk_wishlist>/', views.wishlist_items_wrapper, name='wishlist_items_wrapper'),
    path('<int:pk_wishlist>/items/<int:pk_wishlist_item>', views.wishlist_item_detail_wrapper, name='wishlist_item_detail_wrapper'),
]
