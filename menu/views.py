from django.shortcuts import render, redirect
from .models import Plato
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from users.models import Perfil 


def gestion_platos(request):
    platos = Plato.objects.all()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        nombre = request.POST.get('nombre_plato', '').strip().upper()
        precio = request.POST.get('precio_plato')

        if not nombre:
            messages.error(request, 'Debe ingresar un nombre.')
            return redirect('gestion_platos')
        
        if not precio:
            messages.error(request, 'Debe ingresar un precio.')
            return redirect('gestion_platos')


        if accion == 'crear':
            if Plato.objects.filter(nombre__iexact=nombre).exists():
                messages.warning(request, 'Ya existe un plato con ese nombre.')
            else:
                Plato.objects.create(nombre=nombre, precio=precio)
                messages.success(request, 'Plato creado exitosamente.')

        elif accion == 'editar':
            try:
                plato = Plato.objects.get(nombre__iexact=nombre)
                plato.precio = precio
                plato.save()
                messages.success(request, 'Plato actualizado.')
            except Plato.DoesNotExist:
                messages.error(request, 'El plato no existe.')

        elif accion == 'eliminar':
            try:
                plato = Plato.objects.get(nombre__iexact=nombre)
                plato.delete()
                messages.success(request, 'Plato eliminado.')
            except Plato.DoesNotExist:
                messages.error(request, 'El plato no existe.')

        return redirect('gestion_platos')
    perfiles = Perfil.objects.select_related('user').all()
    return render(request, 'administrador/home-admin.html', {
            'platos': platos,
            'perfiles': perfiles
        })

@require_GET
def obtener_precio_plato(request):
    nombre = request.GET.get('nombre', '').strip().upper()
    try:
        plato = Plato.objects.get(nombre__iexact=nombre)
        return JsonResponse({'precio': str(plato.precio)})
    except Plato.DoesNotExist:
        return JsonResponse({'precio': ''})