from django.urls import path

from . import views

# app_name = 'publishers'

urlpatterns = [
    path('', views.publisher_wrapper, name='publisher-wrapper'),
    path('<int:pk_publisher>/', views.publisher_detail_wrapper, name='publisher-detail-wrapper'),
]
