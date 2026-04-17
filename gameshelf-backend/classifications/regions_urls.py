from django.urls import path

from . import views

# app_name = 'regions'

urlpatterns = [
    path('', views.region_wrapper, name='region-wrapper'),
    path('<int:pk_region>/', views.region_detail_wrapper, name='region-detail-wrapper'),
]