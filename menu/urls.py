from django.urls import path
from . import views

urlpatterns = [
    path('ingredientes/', views.gestion_ingredientes, name='gestion_ingredientes'),
    path('ingredientes/precio/', views.obtener_precio_ingrediente, name='obtener_precio_ingrediente'),
]