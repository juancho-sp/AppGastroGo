from django.shortcuts import render

def nuevoPedido (request):
    return render(request, 'cajero/home-cajero.html')

def pedidosPendientes (request):
    return render(request, 'cocinero/home-cocinero.html')
