# Generated by Django 4.0.6 on 2025-01-12 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transportes', '0004_bus_nombre_bus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
