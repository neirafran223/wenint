from rest_framework import serializers
from .models import Producto, Carrito, Boleta, OrdenDespacho, ItemCarrito

class ItemCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrito
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Producto
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = '__all__'

class OrdenDespachoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDespacho
        fields = '__all__'
