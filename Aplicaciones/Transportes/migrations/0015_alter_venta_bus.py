# Generated by Django 4.0.6 on 2025-01-13 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Transportes', '0014_venta_bus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.bus'),
        ),
    ]
