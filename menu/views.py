from django.shortcuts import render, redirect
from .models import Ingrediente
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def gestion_ingredientes(request):
    ingredientes = Ingrediente.objects.all()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        nombre = request.POST.get('nombre', '').strip().upper()  # siempre mayúsculas
        precio = request.POST.get('precio', '').strip()

        if not nombre:
            messages.error(request, 'Debe ingresar un nombre.')
            return redirect('gestion_ingredientes')

        if accion == 'crear':
            if Ingrediente.objects.filter(nombre__iexact=nombre).exists():
                messages.warning(request, 'Ya existe un ingrediente con ese nombre.')
            else:
                Ingrediente.objects.create(nombre=nombre, precio=precio)
                messages.success(request, 'Ingrediente creado exitosamente.')

        elif accion == 'editar':
            ingrediente = Ingrediente.objects.filter(nombre__iexact=nombre).first()
            if ingrediente:
                ingrediente.precio = precio
                ingrediente.save()
                messages.success(request, 'Ingrediente actualizado correctamente.')
            else:
                messages.error(request, 'El ingrediente no existe para ser editado.')

        elif accion == 'eliminar':
            ingrediente = Ingrediente.objects.filter(nombre__iexact=nombre).first()
            if ingrediente:
                ingrediente.delete()
                messages.success(request, 'Ingrediente eliminado correctamente.')
            else:
                messages.error(request, 'El ingrediente no existe para ser eliminado.')

        return redirect('gestion_ingredientes')

    return render(request, 'administrador/home-admin.html', {
        'ingredientes': ingredientes
    })


# API para obtener precio desde el JS
@require_GET
def obtener_precio_ingrediente(request):
    nombre = request.GET.get('nombre', '').strip().upper()
    try:
        ingrediente = Ingrediente.objects.get(nombre__iexact=nombre)
        return JsonResponse({'precio': str(ingrediente.precio)})
    except Ingrediente.DoesNotExist:
        return JsonResponse({'precio': ''})