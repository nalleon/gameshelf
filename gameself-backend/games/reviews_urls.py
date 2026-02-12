from django.urls import path

from . import views

# app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review-list'),
    path('add/', views.add_review, name='add-review'),
    path('<int:pk_review>/', views.review_detail, name='review-detail'),
    path('<int:pk_review>/delete/', views.delete_review, name='delete-review'),
    path('<int:pk_review>/edit/', views.edit_review, name='edit-review'),
]
