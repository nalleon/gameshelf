from django.urls import path

from . import views

# app_name = 'reviews'

urlpatterns = [
    path('', views.review_wrapper, name='review-wrapper'),
    path('<int:pk_review>/', views.review_detail_wrapper, name='review-detail-wrapper'),
]
