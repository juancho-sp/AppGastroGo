from django.urls import path
from . import views

urlpatterns = [
    path('', views.crear_pedido, name='crear_pedido'),
    path('cajero/tabs/nuevo/', views.tab_nuevo_pedido, name='tab_nuevo_pedido'),
    path('cajero/tabs/detalle/', views.tab_detalle_pedido, name='tab_detalle_pedido'),
    path('cajero/tabs/estado/', views.tab_estado_pedidos, name='tab_estado_pedidos'),
    path('admin/editar-pedido/', views.editar_pedido_admin, name='editar_pedido_admin'),
    path('estado/', views.tab_estado_pedidos, name='tab_estado_pedidos'),
    path('cambiar-estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('estado/', views.estado_pedidos, name='estado_pedidos'),
    path('cocina/preparar/', views.marcar_preparado, name='marcar_preparado'),
    path('cocinero/', views.home_cocinero, name='home_cocinero'),
]
