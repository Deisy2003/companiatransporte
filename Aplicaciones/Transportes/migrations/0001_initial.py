# Generated by Django 4.0.6 on 2025-01-12 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, unique=True, verbose_name='Cédula')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección')),
            ],
        ),
        migrations.CreateModel(
            name='Conductor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('licencia', models.CharField(max_length=50, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('telefono', models.CharField(blank=True, max_length=15)),
                ('direccion', models.CharField(blank=True, max_length=255)),
                ('fecha_ingreso', models.DateField()),
                ('estado', models.CharField(choices=[('Activo', 'Activo'), ('Suspendido', 'Suspendido'), ('Retirado', 'Retirado')], default='Activo', max_length=20)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='conductores/')),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=100)),
                ('destino', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asiento', models.CharField(max_length=5)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_compra', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.cliente')),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.ruta')),
            ],
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Vendedor', 'Vendedor'), ('Usuario', 'Usuario')], default='Usuario', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=10)),
                ('hora_salida', models.TimeField()),
                ('hora_llegada', models.TimeField()),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transportes.ruta')),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_placa', models.CharField(max_length=15, unique=True)),
                ('capacidad', models.PositiveIntegerField()),
                ('conductor', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bus', to='Transportes.conductor')),
            ],
        ),
    ]
