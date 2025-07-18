from django.db import models

class Plato(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        # Muestra nombre y precio en el desplegable de selección de platos
        return f'{self.nombre} - ${self.precio}'