# Generated by Django 4.0.6 on 2025-01-13 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Transportes', '0012_remove_venta_precio_remove_venta_ruta_venta_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.horario'),
        ),
    ]
