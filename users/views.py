from django.contrib.auth.models import User
from users.models import Perfil 
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from menu.models import Plato


@login_required
def inicioAdministrador(request):
    perfiles = Perfil.objects.select_related('user').all()
    print('Total perfiles:', len(perfiles))
    platos = Plato.objects.all()
    return render(request, 'administrador/home-admin.html', {
        'perfiles': perfiles,
        'platos': platos,
    })

@login_required
def home_admin(request):
    perfiles = Perfil.objects.select_related('user').all()
    print('Total perfiles:', len(perfiles))  # <- Añade esta línea para debug
    return render(request, 'administrador/home-admin.html', {
        'perfiles': perfiles
    })

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('numero_documento', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        tipo_documento = request.POST.get('tipo_documento', '').strip()
        numero_documento = request.POST.get('numero_documento', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
        rol = request.POST.get('rol', '').strip()

        # Validaciones
        if request.user.username == request.POST.get('numero_documento'):
            messages.error(request, "No puedes modificar tu propio número de documento mientras estás autenticado.")
            return redirect('home_admin')      
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ya existe un usuario con ese número de documento.')
            return redirect('home_admin')
        
        if Perfil.objects.filter(numero_documento=numero_documento).exists():
            messages.error(request, 'Ya existe un usuario con ese número de documento.')
            return redirect('home_admin')
        
        if not numero_documento or not password or not first_name or not last_name:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('home_admin')

        # Validar contraseña con validadores de Django
        try:
            validate_password(password)
        except ValidationError as e:
            translated_errors = [_(msg) for msg in e.messages]
            messages.error(request, translated_errors[0])  # Usa messages
            return redirect('inicioAdministrador')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        Perfil.objects.create(
            user=user,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            fecha_nacimiento=fecha_nacimiento,
            rol=rol
        )

        messages.success(request, 'Usuario creado exitosamente.')
        return redirect('home_admin')  # Asegúrate de tener este nombre en tu urls.py


    return render(request, 'administrador/home-admin.html')


@login_required
def eliminar_usuario(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    perfil.user.delete()  # Esto elimina el perfil automáticamente por la relación OneToOne
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('home_admin')


@login_required
def actualizar_usuario(request):
    if request.method == 'POST':
        perfil_id = request.POST.get('perfil_id')
        perfil = get_object_or_404(Perfil, id=perfil_id)
        user = perfil.user
        # Verificar si el usuario que intenta actualizar es el mismo que está autenticado


        # Actualizar campos
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)
        if perfil.user != request.user:
            user.username = request.POST.get('numero_documento')
        user.save()

        perfil.tipo_documento = request.POST.get('tipo_documento')
        perfil.numero_documento = request.POST.get('numero_documento')
        perfil.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        perfil.rol = request.POST.get('rol')
        perfil.save()

        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('home_admin')