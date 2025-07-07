from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from .forms import PedidoForm, PedidoPlatoForm
from .models import Pedido, PedidoPlato

@login_required
def nuevoPedido(request):
    PedidoPlatoFormSet = modelformset_factory(
        PedidoPlato,
        form=PedidoPlatoForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST' and 'buscar' not in request.POST:
        pedido_form = PedidoForm(request.POST)
        formset = PedidoPlatoFormSet(request.POST, queryset=PedidoPlato.objects.none())

        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.cajero = request.user
            pedido.estado = 'pendiente'
            pedido.save()

            total = 0
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    plato = form.cleaned_data['plato']
                    cantidad = form.cleaned_data['cantidad']
                    nota = form.cleaned_data.get('nota', '')
                    subtotal = plato.precio * cantidad

                    PedidoPlato.objects.create(
                        pedido=pedido,
                        plato=plato,
                        cantidad=cantidad,
                        nota=nota,
                        subtotal=subtotal
                    )

                    total += subtotal

            pedido.total = total
            pedido.save()

            messages.success(request, '✅ Pedido registrado correctamente.')
            return redirect('nuevoPedido')
    else:
        pedido_form = PedidoForm()
        formset = PedidoPlatoFormSet(queryset=PedidoPlato.objects.none())

    pedidos = Pedido.objects.filter(cajero=request.user).order_by('-fecha_creacion')[:10]

    fecha_filtrar = request.GET.get('fecha')
    if fecha_filtrar:
        fecha_inicio = datetime.strptime(fecha_filtrar, '%Y-%m-%d')
        fecha_fin = fecha_inicio.replace(hour=23, minute=59, second=59)
        pedidos = Pedido.objects.filter(
            cajero=request.user,
            fecha_creacion__range=(fecha_inicio, fecha_fin)
        ).order_by('-fecha_creacion')

    return render(request, 'cajero/home-cajero.html', {
        'pedido_form': pedido_form,
        'formset': formset,
        'pedidos': pedidos
    })

@login_required
def pedidosPendientes(request):
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-fecha_creacion')
    return render(request, 'cocinero/home-cocinero.html', {'pedidos': pedidos})