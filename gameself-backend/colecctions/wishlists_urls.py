from django.urls import path

from . import views

# app_name = 'wishlists'

urlpatterns = [
    path('', views.wishlist_item_list, name='wishlist_item-list'),
    path('add/', views.add_wishlist_item, name='add-wishlist_item'),
    path('self-add/', views.add_self_wishlist_item, name='add-self-wishlist_item'),
    path('<int:pk_wishlist_item>/', views.wishlist_item_detail, name='wishlist_item-detail'),
    path('<int:pk_wishlist_item>/delete/', views.delete_wishlist_item, name='delete-wishlist_item'),
    path('<int:pk_wishlist_item>/edit/', views.edit_wishlist_item, name='edit-wishlist_item'),
]
