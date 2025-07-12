from django.urls import path
from . import views

urlpatterns = [
    path('cajero/', views.crear_pedido, name='crear_pedido'),
    path('cajero/tabs/nuevo/', views.tab_nuevo_pedido, name='tab_nuevo_pedido'),
    path('cajero/tabs/detalle/', views.tab_detalle_pedido, name='tab_detalle_pedido'),
    path('cajero/tabs/estado/', views.tab_estado_pedidos, name='tab_estado_pedidos'),
    path('admin/editar-pedido/', views.editar_pedido_admin, name='editar_pedido_admin'),
]
