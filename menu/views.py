from django.shortcuts import render, redirect
from .models import Ingrediente, Plato
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def gestion_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    platos = Plato.objects.all()  # <-- IMPORTANTE para que no se rompa el home-admin.html

    if request.method == 'POST':
        accion = request.POST.get('accion')
        nombre = request.POST.get('nombre', '').strip().upper()
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
        'ingredientes': ingredientes,
        'platos': platos,  # <-- IMPORTANTE para que no se rompa el home-admin.html 
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

    return render(request, 'administrador/home-admin.html', {'platos': platos})

@require_GET
def obtener_precio_plato(request):
    nombre = request.GET.get('nombre', '').strip().upper()
    try:
        plato = Plato.objects.get(nombre__iexact=nombre)
        return JsonResponse({'precio': str(plato.precio)})
    except Plato.DoesNotExist:
        return JsonResponse({'precio': ''})