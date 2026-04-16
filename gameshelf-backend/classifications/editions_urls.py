from django.urls import path

from . import views

# app_name = 'editions'

urlpatterns = [
    path('', views.edition_wrapper, name='edition-wrapper'),
    path('<int:pk_edition>/', views.edition_detail_wrapper, name='edition-detail-wrapper'),
]
