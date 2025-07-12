from django.db import models
from django.contrib.auth.models import User
from menu.models import Plato

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    turno = models.IntegerField(unique=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=15, decimal_places=0, default=0.00)
    nota_cancelacion = models.TextField(blank=True, null=True)
    fecha_actualizacion_estado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - Turno {self.turno}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre}"
