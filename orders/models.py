from django.db import models
from django.contrib.auth.models import User
from menu.models import Plato

class Pedido(models.Model):
    mesa = models.IntegerField()
    cajero = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=20, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.mesa}'

class PedidoPlato(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='platos')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    nota = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.plato.nombre} x {self.cantidad}'
