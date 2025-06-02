# Import necessary modules
from django.shortcuts import redirect, render, get_object_or_404
from .models import Producto, Carrito, Boleta, OrdenDespacho, ItemCarrito
from .forms import ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q # Importar Q para consultas complejas
from .serializers import ProductoSerializer, CarritoSerializer, BoletaSerializer, OrdenDespachoSerializer, ItemCarritoSerializer # Asegúrate de que esto esté presente

# Función para mostrar vistas
def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos,
    }
    return render(request, 'ventas/home.html', data)

def base(request):
    return render(request, 'ventas/base.html')

def galeria(request):
    return render(request, 'ventas/galeria.html')

# Productos
def agregar_productos(request):
    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Registrado")
        else:
            data["form"] = formulario

    return render(request, 'ventas/producto/agregar.html', data)

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data['username'],
                password=formulario.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, "Usuario Registrado")
            return redirect(to='home')
        else:
            data["form"] = formulario

    return render(request, 'registration/registro.html', data)

# Listar
def listar_productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'ventas/producto/listar.html', data)

def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    data = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_productos")
        else:
            data["form"] = formulario
    
    return render(request, 'ventas/producto/modificar.html', data)

def eliminar_edicion(request, producto_id):   
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect(to="listar_productos")

# Consumo de APIs externas
def consumir_apis(request):
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    data = response.json() if response.status_code == 200 else []
    return render(request, 'Apis/Api_result.html', {'data': data})

def seguridad(request):
    return render(request, 'Apis/Api_seguridad.html')

def stock(request):
    return render(request, 'stock/stock.html')

def productos(request):
    return render(request, 'productos/productos.html')

def carrito(request):
    # Lógica para mostrar el carrito de compras del usuario
    items_en_carrito = []
    total_carrito = 0

    if request.user.is_authenticated:
        # Obtener los items del carrito para el usuario actual
        # Asumiendo que Carrito.objects.filter(usuario=request.user) devuelve instancias de Carrito
        # y que ItemCarrito está relacionado con Carrito
        try:
            # Obtener los items del carrito directamente si tu modelo ItemCarrito tiene una relación directa con el usuario
            # O si el modelo Carrito es más bien una "sesión" de carrito y ItemCarrito son los productos dentro de esa sesión
            # Si Carrito es un "header" y ItemCarrito son los "detalles", necesitas un Carrito por usuario.
            # Según tu models.py, Carrito tiene usuario y producto, lo que es un poco ambiguo.
            # Vamos a asumir que Carrito es el item individual en el carrito:
            items_en_carrito = Carrito.objects.filter(usuario=request.user)
            for item in items_en_carrito:
                total_carrito += item.producto.precio * item.cantidad
        except Exception as e:
            messages.error(request, f"Error al cargar el carrito: {e}")
            items_en_carrito = []
            total_carrito = 0
    else:
        messages.info(request, "Inicia sesión para ver tu carrito.")
        # Lógica para carrito de sesión si no hay usuario autenticado (más complejo, no se implementará aquí)

    context = {
        'items_en_carrito': items_en_carrito,
        'total_carrito': total_carrito,
    }
    return render(request, 'ventas/carrito.html', context)

# Nueva función de vista para el detalle del producto
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'ventas/detalle_producto.html', {'producto': producto})

# Nueva función de vista para agregar al carrito
def agregar_al_carrito(request, producto_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para añadir productos al carrito.")
        return redirect('login') # O a la página de detalle del producto

    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser al menos 1.")
        return redirect('detalle_producto', producto_id=producto.id)

    if producto.stock < cantidad:
        messages.error(request, f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")
        return redirect('detalle_producto', producto_id=producto.id)

    # Buscar si el producto ya está en el carrito del usuario
    item_carrito, created = Carrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': cantidad}
    )

    if not created:
        # Si el item ya existe, actualiza la cantidad
        item_carrito.cantidad += cantidad
        item_carrito.save()
        messages.success(request, f"Se agregaron {cantidad} unidades más de '{producto.nombre}' a tu carrito.")
    else:
        messages.success(request, f"'{producto.nombre}' se añadió a tu carrito.")

    return redirect('carrito') # Redirige a la página del carrito

# API REST Framework ViewSets (sin cambios significativos, solo un pequeño ajuste en la lógica de stock para claridad)
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @action(detail=False, methods=['post'])
    def cerrar_compra(self, request):
        if not request.user.is_authenticated:
            return Response({'mensaje': 'Debe iniciar sesión para realizar una compra'}, status=status.HTTP_401_UNAUTHORIZED)
            
        carrito_items = Carrito.objects.filter(usuario=request.user)
        if not carrito_items.exists():
            return Response({'mensaje': 'Carrito vacío'}, status=status.HTTP_400_BAD_REQUEST)
        
        total = 0
        productos_a_actualizar = []
        for item in carrito_items:
            if item.producto.stock < item.cantidad:
                return Response({'mensaje': f'Stock insuficiente para {item.producto.nombre}'}, status=status.HTTP_400_BAD_REQUEST)
            item.producto.stock -= item.cantidad
            productos_a_actualizar.append(item.producto)
            total += item.producto.precio * item.cantidad
        
        # Guardar cambios de stock de una vez
        Producto.objects.bulk_update(productos_a_actualizar, ['stock'])

        boleta = Boleta.objects.create(usuario=request.user, total=total)
        carrito_items.delete() # Vaciar el carrito
        
        return Response({'mensaje': 'Compra realizada', 'boleta_id': boleta.id}, status=status.HTTP_201_CREATED)


class BoletaViewSet(viewsets.ModelViewSet):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer
    
    def get_queryset(self): # Esto es un método de clase, no una función independiente
        return Boleta.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("Debe iniciar sesión para crear una boleta.")

        carrito_items = Carrito.objects.filter(usuario=self.request.user)
        if not carrito_items.exists():
            raise serializers.ValidationError("El carrito está vacío.")
            
        total = 0
        productos_a_actualizar = []
        for item in carrito_items:
            if item.producto.stock < item.cantidad:
                # Se necesita importar serializers para usar ValidationError
                from rest_framework import serializers 
                raise serializers.ValidationError(f"Stock insuficiente para {item.producto.nombre}")
            item.producto.stock -= item.cantidad
            productos_a_actualizar.append(item.producto)
            total += item.producto.precio * item.cantidad
        
        Producto.objects.bulk_update(productos_a_actualizar, ['stock'])
        boleta = serializer.save(usuario=self.request.user, total=total)
        carrito_items.delete()
   
class ItemCarritoViewSet(viewsets.ModelViewSet):
    queryset = ItemCarrito.objects.all()
    serializer_class = ItemCarritoSerializer

class OrdenDespachoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDespacho.objects.all()
    serializer_class = OrdenDespachoSerializer