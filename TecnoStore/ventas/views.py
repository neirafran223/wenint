# Import necessary modules
from django.shortcuts import redirect, render, get_object_or_404
from .models import Producto, Carrito, Boleta, OrdenDespacho, ItemCarrito
from .forms import ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .serializers import ProductoSerializer, CarritoSerializer, BoletaSerializer, OrdenDespachoSerializer, ItemCarritoSerializer
from rest_framework import viewsets
import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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
    return redirect(to="listar_productos")

# Consumo de APIs externas
def consumir_apis(request):
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    data = response.json() if response.status_code == 200 else []
    return render(request, 'api_result.html', {'data': data})

def seguridad(request):
    return render(request, 'seguridad.html')

def stock(request):
    return render(request, 'stock.html')

def productos(request):
    return render(request, 'productos.html')

# API REST Framework ViewSets
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @action(detail=False, methods=['post'])
    def cerrar_compra(self, request):
        carrito = Carrito.objects.filter(usuario=request.user)
        if not carrito:
            return Response({'mensaje': 'Carrito vacío'}, status=status.HTTP_400_BAD_REQUEST)
        total = 0
        for item in carrito:
            if item.producto.stock >= item.cantidad:
                item.producto.stock -= item.cantidad
                item.producto.save()
                total += item.producto.precio * item.cantidad
            else:
                return Response({'mensaje': f'Stock insuficiente para {item.producto.nombre}'}, status=status.HTTP_400_BAD_REQUEST)
        boleta = Boleta.objects.create(usuario=request.user, total=total)
        carrito.delete()
        return Response({'mensaje': 'Compra realizada', 'boleta_id': boleta.id}, status=status.HTTP_201_CREATED)


class BoletaViewSet(viewsets.ModelViewSet):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer
# Filtro por usuario en APIs
def get_queryset(self):
    return Carrito.objects.filter(usuario=self.request.user)

class BoletaViewSet(viewsets.ModelViewSet):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer

    def perform_create(self, serializer):
        carrito = Carrito.objects.filter(usuario=self.request.user)
        total = 0
        for item in carrito:
            if item.producto.stock >= item.cantidad:
                item.producto.stock -= item.cantidad
                item.producto.save()
                total += item.producto.precio * item.cantidad
            else:
                raise serializers.ValidationError(f"Stock insuficiente para {item.producto.nombre}")
        boleta = serializer.save(usuario=self.request.user, total=total)
        carrito.delete()
   
class ItemCarritoViewSet(viewsets.ModelViewSet):
    queryset = ItemCarrito.objects.all()
    serializer_class = ItemCarritoSerializer
class OrdenDespachoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDespacho.objects.all()
    serializer_class = OrdenDespachoSerializer