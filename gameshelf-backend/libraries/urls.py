from django.urls import path

from . import views

# app_name = 'libraries'

urlpatterns = [
    path('', views.library_wrapper, name='library-wrapper'),
    path('<int:pk_item>/', views.library_detail_wrapper, name='library-detail-wrapper'),
    path('users/<int:pk_user>/', views.get_library, name='library-user'),
]
