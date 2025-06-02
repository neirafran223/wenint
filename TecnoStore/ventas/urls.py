from django.urls import path, include
from .views import home, galeria, base, listar_productos, registro, modificar_producto, eliminar_edicion, agregar_productos,ProductoViewSet, CarritoViewSet, BoletaViewSet, OrdenDespachoViewSet, ItemCarritoViewSet
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API TecnoStore",
      default_version='v1',
      description="Documentación interactiva de la API de Ventas y módulos integrados.",
      contact=openapi.Contact(email="contacto@tecnostore.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# Define the URL patterns for the ventas app    
# Configurar las rutas de los ViewSet (API REST)
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'boletas', BoletaViewSet)
router.register(r'ordenes-despacho', OrdenDespachoViewSet)
router.register(r'items-carrito', ItemCarritoViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('galeria/', galeria, name='galeria'),
    path('base/', base, name='base'),
    path('registro/', registro, name='registro'),
    path('agregar_productos/', agregar_productos, name='agregar_productos'),
    path('listar_productos/', listar_productos, name='listar_productos'),
    path('modificar_producto/<int:producto_id>/', modificar_producto, name='modificar_producto'),
    path('eliminar_edicion/<int:producto_id>/', eliminar_edicion, name='eliminar_edicion'),
    # Rutas de API REST
    path('api/', include(router.urls)),
    
]

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

