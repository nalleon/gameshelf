from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile_wrapper, name='profile-wrapper'),
    path('me/', views.profile_me, name='profile-me'),
    path('search/', views.search_by_name, name='profile-search'),
    path('<int:pk_profile>/', views.profile_detail_wrapper, name='profile-details'),
]