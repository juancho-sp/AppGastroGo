from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PlatoTextoForm
from .models import Pedido, DetallePedido
from menu.models import Plato
from django.utils.dateparse import parse_date
from datetime import datetime, time, timezone as dt_timezone
from django.utils.timezone import make_aware, get_current_timezone
from django.urls import reverse
from users.models import Perfil
from django.db.models import Sum

@login_required
def crear_pedido(request):
    return render(request, 'cajero/home-cajero.html')


@login_required
def tab_nuevo_pedido(request):
    PlatoFormSet = formset_factory(PlatoTextoForm, extra=1)
    platos = Plato.objects.all()

    if request.method == 'POST':
        formset = PlatoFormSet(request.POST)
        turno = request.POST.get('turno')

        if not turno or not turno.isdigit():
            messages.warning(request, "Debes ingresar un número de turno válido.")
            return redirect('crear_pedido')

        turno = int(turno)

        if Pedido.objects.filter(turno=turno, estado='pendiente').exists():
            messages.warning(request, f"Ya existe un pedido pendiente con el turno {turno}.")
            return redirect('crear_pedido')

        if formset.is_valid():
            # Validar que todos los platos existan ANTES de crear el pedido
            nombres_invalidos = []
            for form in formset:
                nombre = form.cleaned_data.get('nombre_plato')
                if nombre and not Plato.objects.filter(nombre=nombre).exists():
                    nombres_invalidos.append(nombre)

            if nombres_invalidos:
                for nombre in nombres_invalidos:
                    messages.warning(request, f"El plato '{nombre}' no existe.")
                return redirect('crear_pedido')  # No crear pedido si hay errores

            # Crear el pedido porque todos los nombres son válidos
            pedido = Pedido.objects.create(
                turno=turno,
                usuario=request.user,
                estado='pendiente',
                total=0
            )

            total_pedido = 0

            for form in formset:
                nombre = form.cleaned_data.get('nombre_plato')
                cantidad = form.cleaned_data.get('cantidad')
                nota = form.cleaned_data.get('nota_plato')

                plato = Plato.objects.get(nombre=nombre)
                subtotal = plato.precio * cantidad
                total_pedido += subtotal

                DetallePedido.objects.create(
                    pedido=pedido,
                    plato=plato,
                    cantidad=cantidad,
                    nota=nota
                )

            pedido.total = total_pedido
            pedido.save()

            messages.success(request, f"Pedido #{pedido.id} creado exitosamente.")
            return redirect('crear_pedido')

        else:
            messages.warning(request, "Hay errores en el formulario.")
            return redirect('crear_pedido')

    else:
        formset = PlatoFormSet()

    turnos_pendientes = Pedido.objects.filter(estado='pendiente').order_by('turno').values_list('turno', flat=True)

    return render(request, 'cajero/tabs/nuevo_pedido.html', {
        'formset': formset,
        'platos': platos,
        'platos_json': {p.nombre: float(p.precio) for p in platos},
        'turnos_pendientes': turnos_pendientes,
    })

@login_required
def tab_detalle_pedido(request):
    if not request.GET.get('fecha'):
        today = timezone.localdate()
        return redirect(f"{reverse('tab_detalle_pedido')}?fecha={today}")

    fecha_str = request.GET.get('fecha')
    hora_inicio_str = request.GET.get('hora_inicio')
    hora_fin_str = request.GET.get('hora_fin')

    pedidos = []

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        if hora_inicio_str and hora_fin_str:
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()

            dt_inicio_naive = datetime.combine(fecha, hora_inicio)
            dt_fin_naive = datetime.combine(fecha, hora_fin)

            tz = timezone.get_current_timezone()
            datetime_inicio = timezone.make_aware(dt_inicio_naive, timezone=tz)
            datetime_fin = timezone.make_aware(dt_fin_naive, timezone=tz)

            print("Inicio UTC:", datetime_inicio)
            print("Fin UTC:", datetime_fin)

            pedidos = Pedido.objects.filter(
                fecha_creacion__range=(datetime_inicio, datetime_fin)
            ).order_by('-fecha_creacion')

            for p in pedidos:
                print("Pedido:", p.id, timezone.localtime(p.fecha_creacion))
        else:
            print("⏱ No se especificó rango de hora. No se filtrarán pedidos.")
    except Exception as e:
        print("❌ Error al filtrar pedidos:", e)
        pedidos = []

    # ➕ Total de ventas
    total_ventas = sum(p.total for p in pedidos)

    context = {
        'pedidos': pedidos,
        'fecha': fecha_str,
        'hora_inicio': hora_inicio_str,
        'hora_fin': hora_fin_str,
        'ahora': timezone.localtime(),
        'total_ventas': total_ventas,  #  se pasa al template
    }

    return render(request, 'cajero/tabs/detalle_pedido.html', context)

@login_required
def tab_estado_pedidos(request):
    return render(request, 'cajero/tabs/estado_pedidos.html')


def es_admin(user):
    return hasattr(user, 'perfil') and user.perfil.rol == 'admin'

@login_required
@user_passes_test(es_admin)
def editar_pedido_admin(request):
    pedido = None
    detalles = []

    if request.method == 'GET':
        pedido_id = request.GET.get('pedido_id')

        if pedido_id:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                detalles = pedido.detalles.all()  
            except Pedido.DoesNotExist:
                pedido = None
                detalles = []
                

    context = {
        'pedido': pedido,
        'detalles': detalles,
        'platos': Plato.objects.all(),
        'perfiles': Perfil.objects.all(), 
    }
    return render(request, 'administrador/home-admin.html', context)
