from django.db import models
from datetime import date
from decimal import Decimal


# models.py
from django.contrib.auth.models import User

# Modelo PerfilUsuario
class PerfilUsuario(models.Model):
    # Relación uno a uno con el modelo User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    # Campos adicionales
    
    # Campos para roles
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Vendedor', 'Vendedor'),
        ('Usuario', 'Usuario'),
    ]
    rol = models.CharField(max_length=50, choices=ROL_CHOICES, default='Usuario')
    def __str__(self):
        return self.user.username

class Bus(models.Model):
    nombre_bus = models.CharField(max_length=15, default="Cotopaxi")
    numero_placa = models.CharField(max_length=15, unique=True)
    capacidad = models.PositiveIntegerField()
    numero_bus = models.PositiveIntegerField(unique=True)   # Capacidad máxima de pasajeros
    conductor = models.OneToOneField('Conductor', on_delete=models.SET_NULL, null=True, related_name='bus')
    
    def __str__(self):
        return f"Bus {self.numero_placa}"



class Conductor(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Suspendido', 'Suspendido'),
        ('Retirado', 'Retirado'),
    ]
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activo')
    foto = models.ImageField(upload_to='conductores/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    
class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ruta {self.origen} - {self.destino}"

class Horario(models.Model):
    id=models.AutoField(primary_key=True)

    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    hora_salida = models.TimeField()
    hora_llegada = models.TimeField()
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.ruta.origen} - {self.ruta.destino}"


class Cliente(models.Model):
    cedula = models.CharField(max_length=10, unique=True, verbose_name="Cédula")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cedula})"


class Asiento(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    ocupado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Asiento {self.numero} en {self.bus}"



class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE,null=True, blank=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    asiento = models.CharField(max_length=200) 
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_asientos = models.IntegerField()
    asientos = models.ManyToManyField(Asiento)

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre} - {self.ruta.origen} a {self.ruta.destino}"
    





