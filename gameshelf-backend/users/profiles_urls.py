from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/', views.user_login, name='profile-details'),
    path('<str:username>/edit/', views.user_register, name='edit-profile'),
    # path('<str:username>/delete', views.user_login, name='logout'),
]