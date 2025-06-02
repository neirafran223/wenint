from django.db import models
from collections import UserList
from django.contrib.auth.models import User
# Create your models here.c
class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Boleta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

class OrdenDespacho(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    entregado = models.BooleanField(default=False)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
    
ESTADOS_BOLETA = [
    ('pendiente', 'Pendiente'),
    ('pagado', 'Pagado'),
    ('anulado', 'Anulado'),
]

class Boleta(models.Model):
    ...
    estado = models.CharField(max_length=10, choices=ESTADOS_BOLETA, default='pendiente')

ESTADOS_DESPACHO = [
    ('pendiente', 'Pendiente'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
]

class OrdenDespacho(models.Model):
    ...
    estado = models.CharField(max_length=10, choices=ESTADOS_DESPACHO, default='pendiente')
