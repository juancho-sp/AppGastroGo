from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from users.models import Perfil

def inicio (request):
    return render(request, 'index.html')

@never_cache
def loginView(request):
    # Si ya está autenticado, redirigir según el rol
    if request.user.is_authenticated:
        try:
            if request.user.is_superuser:
                return redirect('home_admin')
            perfil = request.user.perfil
            if perfil.rol == 'admin':
                return redirect('home_admin')
            elif perfil.rol == 'cocinero':
                return redirect('home_cocinero')
            elif perfil.rol == 'cajero':
                return redirect('home_cajero')
            else:
                return render(request, 'index.html', {'message': 'Rol no reconocido'})
        except:
            return render(request, 'index.html', {'message': 'No se pudo determinar el rol del usuario'})

    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home_admin')
            try:
                perfil = user.perfil
                if perfil.rol == 'admin':
                    return redirect('home_admin')
                elif perfil.rol == 'cocinero':
                    return redirect('home_cocinero')
                elif perfil.rol == 'cajero':
                    return redirect('home_cajero')
                else:
                    message = 'Rol no reconocido.'
            except:
                message = 'El usuario no tiene un perfil asociado.'
        else:
            message = 'Usuario o contraseña incorrectos'

    return render(request, 'index.html', {'message': message})

@login_required
def home_admin(request):
    return render(request, 'administrador/home-admin.html')

@login_required
def home_cajero(request):
    return render(request, 'cajero/home-cajero.html')

@login_required
def home_cocinero(request):
    return render(request, 'cocinero/home-cocinero.html')

# Cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cambiar_rol(request):
    perfil = Perfil.objects.get(user=request.user)
    rol_actual = perfil.rol

    # Secuencia de cambio de rol
    siguiente_rol = {
        'admin': 'cajero',
        'cajero': 'cocinero',
        'cocinero': 'admin'
    }

    nuevo_rol = siguiente_rol.get(rol_actual, 'admin')  # por si acaso

    perfil.rol = nuevo_rol
    perfil.save()

    # Redirigir al home del nuevo rol
    if nuevo_rol == 'admin':
        return redirect('home_admin')
    elif nuevo_rol == 'cajero':
        return redirect('home_cajero')
    elif nuevo_rol == 'cocinero':
        return redirect('home_cocinero')

    # Fallback
    return redirect('home')