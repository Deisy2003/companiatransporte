# Generated by Django 4.0.6 on 2025-01-13 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Transportes', '0020_asiento_bus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asiento',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.bus'),
        ),
    ]
