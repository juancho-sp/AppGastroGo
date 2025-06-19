from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth.views import LogoutView
from ingreso.views import logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ingreso.urls')), # el '' vacio es la raiz del proyecto, y se redirige a ingreso.urls
    path('administrador/', include('users.urls')),  # Redirige a las URLs de la aplicación users
    path('operativo/', include('orders.urls')),  # Redirige a las URLs de la aplicación cajero
    path('logout/', logout_view, name='logout'),
]
