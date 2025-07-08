from django.contrib import admin
from .models import Pedido, PedidoPlato

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'mesa', 'cajero', 'estado', 'total', 'fecha_creacion']
    search_fields = ['id', 'cajero__username', 'mesa']

@admin.register(PedidoPlato)
class PedidoPlatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'plato', 'cantidad', 'subtotal']
    search_fields = ['plato__nombre', 'pedido__id']
