from django.contrib import admin
from .models import Plato

from import_export  import resources
from import_export.admin import ImportExportModelAdmin

class PlatoResource(resources.ModelResource):
    class Meta:
        model = Plato
        fields = ('id', 'nombre', 'precio')
        export_order = ('id', 'nombre', 'precio')

@admin.register(Plato)
class PlatoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    resource_class = PlatoResource
