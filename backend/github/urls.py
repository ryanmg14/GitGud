from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('info/<pk>/', views.info, name='info'),
]
