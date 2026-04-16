from django.urls import path

from . import views

# app_name = 'developers'

urlpatterns = [
    path('', views.developer_wrapper, name='developer-wrapper'),
    path('<int:pk_developer>/', views.developer_detail_wrapper, name='developer-detail-wrapper'),
]
