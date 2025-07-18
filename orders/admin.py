from django.contrib import admin
from .models import Pedido, DetallePedido

from import_export  import resources
from import_export.admin import ImportExportModelAdmin

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['plato', 'cantidad', 'nota']
    can_delete = False

class PedidoResource(resources.ModelResource):
    class Meta:
        model = Pedido
        fields = ('id', 'turno', 'usuario', 'estado', 'fecha_creacion', 'total')
        export_order = ('id', 'turno', 'usuario', 'estado', 'fecha_creacion', 'total')

class DetallePedidoResource(resources.ModelResource):
    class Meta:
        model = DetallePedido
        fields = ('id', 'pedido', 'plato', 'cantidad', 'nota')
        export_order = ('id', 'pedido', 'plato', 'cantidad', 'nota')

@admin.register(Pedido)
class PedidoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'turno', 'usuario', 'estado', 'fecha_creacion', 'total']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['usuario__username', 'turno']
    inlines = [DetallePedidoInline]
    readonly_fields = ['usuario', 'fecha_creacion']
    resourse_class = PedidoResource

@admin.register(DetallePedido)
class DetallePedidoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'pedido', 'plato', 'cantidad', 'nota']
    search_fields = ['pedido__id', 'plato__nombre']
    readonly_fields = ['pedido', 'plato', 'cantidad', 'nota']
    resourse_class = PedidoResource