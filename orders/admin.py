from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['plato', 'cantidad', 'nota']
    can_delete = False

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'turno', 'usuario', 'estado', 'fecha_creacion', 'total']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['usuario__username', 'turno']
    inlines = [DetallePedidoInline]
    readonly_fields = ['usuario', 'fecha_creacion']

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'plato', 'cantidad', 'nota']
    search_fields = ['pedido__id', 'plato__nombre']
    readonly_fields = ['pedido', 'plato', 'cantidad', 'nota']
