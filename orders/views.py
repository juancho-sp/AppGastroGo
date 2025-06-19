from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def nuevoPedido (request):
    return render(request, 'cajero/home-cajero.html')

@login_required
def pedidosPendientes (request):
    return render(request, 'cocinero/home-cocinero.html')
