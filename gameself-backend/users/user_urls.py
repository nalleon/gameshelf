from django.urls import path

from . import views

# app_name = 'collections'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('login/', views.auth, name='login'),
    path('register/', views.auth, name='register'),
    path('logout/', views.auth, name='logout'),
]
