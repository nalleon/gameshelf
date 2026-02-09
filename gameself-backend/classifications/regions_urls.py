from django.urls import path

from . import views

app_name = 'classifications'

urlpatterns = [
    path('', views.region_list, name='region-list'),
    path('add/', views.add_region, name='add-region'),
    path('<int:pk_region>/', views.region_detail, name='region-detail'),
    path('<int:pk_region>/delete/', views.delete_region, name='delete-region'),
    path('<int:pk_region>/edit/', views.edit_region, name='edit-region'),
]
