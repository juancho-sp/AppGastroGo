from django.shortcuts import render

def crearUsuario (request):
    return render(request, 'administrador/home-admin.html')