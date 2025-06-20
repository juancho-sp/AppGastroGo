from django.urls import path
from . import views
from .views import loginView,cambiar_rol

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', loginView, name='loginView'),
    path('', views.home_admin, name='home_admin'),
    path('cajero/', views.home_cajero, name='home_cajero'),
    path('cocinero/', views.home_cocinero, name='home_cocinero'),
    path('cambiar_rol/', cambiar_rol, name='cambiar_rol'),
]