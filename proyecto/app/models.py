from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class transfer(models.Model):
    patente = models.CharField(max_length=20, primary_key=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)
    empresa = models.ForeignKey('EmpresaTransfer', on_delete=models.CASCADE)
    conductor = models.ForeignKey('chofer', on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='static/img/', null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"
    

class EmpresaTransfer(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_agre = models.DateTimeField(default=timezone.now)
    transfers = models.IntegerField(default=0, editable=False) 

    def __str__(self):
        return self.nombre
    

class Chofer(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    usuario = models.CharField(max_length=150, unique=True)
    contrasenna = models.CharField(max_length=128)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=254)
    horario_entrada = models.TimeField()
    horario_salida = models.TimeField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"
    
class Cliente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    transfer_utilizado = models.ForeignKey(transfer, on_delete=models.CASCADE, null=True, blank=True)
    cliente_rut = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha_realizacion = models.DateField()
    hora_realizacion = models.TimeField()
    destino = models.CharField(max_length=200)
    cantidad_asientos = models.IntegerField()

    def __str__(self):
        if self.cliente_rut:
            return f"Reserva #{self.id_reserva} - Cliente: {self.cliente_rut.nombre}, Destino: {self.destino}"
        else:
            return f"Reserva #{self.id_reserva} - Sin cliente, Destino: {self.destino}"
    
class Usuarios(models.Model):
    ROL_CHOICES = (
        ('admin_aeropuerto', 'Admin Aeropuerto'),
        ('admin_empresa_transfer', 'Admin Empresa Transfer'),
        ('superuser', 'Superuser'),
    )

    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    horario_entrada = models.TimeField()
    horario_salida = models.TimeField()
    rol = models.CharField(max_length=50, choices=ROL_CHOICES, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"