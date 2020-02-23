from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('info/<pk>/', views.info, name='info'),
    path('api/<pk>/', views.api, name='api'),
    path('api_list/<pk>/', views.api_list, name='api_list'),
    path('searches/', views.searches, name='searches'),
]
