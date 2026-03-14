from django.urls import path

from . import views

# app_name = 'publishers'

urlpatterns = [
    path('', views.publisher_list, name='publisher-list'),
    path('add/', views.add_publisher, name='add-publisher'),
    path('<int:pk_publisher>/', views.publisher_detail, name='publisher-detail'),
    path('<int:pk_publisher>/delete/', views.delete_publisher, name='delete-publisher'),
    path('<int:pk_publisher>/edit/', views.edit_publisher, name='edit-publisher'),
]
