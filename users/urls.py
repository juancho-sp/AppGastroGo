from django.urls import path
from . import views
from .views import actualizar_usuario, crear_usuario, eliminar_usuario, home_admin

urlpatterns = [
    path('', views.inicioAdministrador, name='inicioAdministrador'),
    path('', home_admin, name='home_admin'),  # esta sí carga 'perfiles'
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('eliminar_usuario/<int:perfil_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('actualizar_usuario/', actualizar_usuario, name='actualizar_usuario'),
]