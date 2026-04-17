from django.urls import path

from . import views

# app_name = 'platforms'

urlpatterns = [
    path('', views.platform_wrapper, name='platform-wrapper'),
    path('<int:pk_platform>/', views.platform_detail_wrapper, name='platform-detail-wrapper'),
]
