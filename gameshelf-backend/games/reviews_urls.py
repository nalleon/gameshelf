from django.urls import path

from . import views

# app_name = 'reviews'

urlpatterns = [
    path('', views.review_wrapper, name='review-wrapper'),
    path('<int:pk_review>/', views.review_detail_wrapper, name='review-detail-wrapper'),
    path('<int:pk_review>/media/', views.add_review_media, name='add-review-media'),
    path('media/<int:pk_media>/', views.delete_review_media, name='delete-review-media'),

]
