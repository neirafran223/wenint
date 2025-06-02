# ventas/models.py

from django.db import models
from django.contrib.auth.models import User

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

class Carrito(models.Model): # This model represents an individual item in a user's cart
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} for {self.usuario.username}"

# Choices for Boleta estado
ESTADOS_BOLETA = [
    ('pendiente', 'Pendiente'),
    ('pagado', 'Pagado'),
    ('anulado', 'Anulado'),
]

class Boleta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Kept, as views use it
    total = models.DecimalField(max_digits=10, decimal_places=2) # Kept, as views use it
    fecha = models.DateTimeField(auto_now_add=True) # Kept, likely useful
    estado = models.CharField(max_length=10, choices=ESTADOS_BOLETA, default='pendiente') # Added from migration 0004

    def __str__(self):
        return f"Boleta {self.id} ({self.usuario.username}) - {self.get_estado_display()}"

# Choices for OrdenDespacho estado
ESTADOS_DESPACHO = [
    ('pendiente', 'Pendiente'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
]

class OrdenDespacho(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE) # Kept
    direccion = models.CharField(max_length=255) # Kept
    # entregado = models.BooleanField(default=False) # This field might be redundant if 'estado' covers it
    estado = models.CharField(max_length=10, choices=ESTADOS_DESPACHO, default='pendiente') # Added from migration 0004

    def __str__(self):
        return f"Orden {self.id} for Boleta {self.boleta.id} - {self.get_estado_display()}"


# ItemCarrito: Review its necessity.
# If 'Carrito' model above IS the item in the cart (User + Product + Qty),
# then 'ItemCarrito' linking to 'Carrito' and also having Product and Qty might be redundant.
# For now, I'm leaving it as it is in your files, but it's something to clarify for your project structure.
class ItemCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (related to Carrito entry {self.carrito.id})"