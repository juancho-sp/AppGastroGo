# Generated by Django 5.2.3 on 2025-07-12 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_pedido_nota_cancelacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='fecha_actualizacion_estado',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
