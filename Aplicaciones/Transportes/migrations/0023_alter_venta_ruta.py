# Generated by Django 4.0.6 on 2025-01-13 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Transportes', '0022_venta_ruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='ruta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.ruta'),
        ),
    ]
