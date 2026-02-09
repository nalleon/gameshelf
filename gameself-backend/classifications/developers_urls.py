from django.urls import path

from . import views

app_name = 'classifications'

urlpatterns = [
    path('', views.developer_list, name='developer-list'),
    path('add/', views.add_developer, name='add-developer'),
    path('<int:pk_developer>/', views.developer_detail, name='developer-detail'),
    path('<int:pk_developer>/delete/', views.delete_developer, name='delete-developer'),
    path('<int:pk_developer>/edit/', views.edit_developer, name='edit-developer'),
]
