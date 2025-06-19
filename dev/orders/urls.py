from django.urls import path
from . import views

urlpatterns = [
    path('cajero', views.nuevoPedido, name='nuevoPedido'),
    path('cocina', views.pedidosPendientes, name='pedidosPendientes'),
]