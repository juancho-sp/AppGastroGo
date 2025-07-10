from django.urls import path
from . import views
from .views import gestion_platos, obtener_precio_plato

urlpatterns = [
    path('gestion_platos/', gestion_platos, name='gestion_platos'),
    path('obtener_precio_plato/', obtener_precio_plato, name='obtener_precio_plato'),
    path('platos/precio/', obtener_precio_plato, name='obtener_precio_plato'),
]