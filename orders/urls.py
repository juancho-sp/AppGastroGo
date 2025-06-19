from django.urls import path
from . import views

urlpatterns = [
    path('caja', views.nuevoPedido, name='nuevoPedido'),
    path('cocina', views.pedidosPendientes, name='pedidosPendientes'),
]