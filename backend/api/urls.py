from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EncargadoInventarioViewSet, InventarioViewSet,
    MateriaPrimaViewSet, ProductoViewSet,
    MovimientoInventarioViewSet, RegistrarMovimientoView,
    LoginEncargadoView
)

router = DefaultRouter()
router.register(r'encargados', EncargadoInventarioViewSet,
                basename='encargado')
router.register(r'inventarios', InventarioViewSet, basename='inventario')
router.register(r'materias-primas', MateriaPrimaViewSet,
                basename='materia-prima')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'movimientos', MovimientoInventarioViewSet,
                basename='movimiento')

urlpatterns = [
    path('', include(router.urls)),
    path('registrar-movimiento/', RegistrarMovimientoView.as_view(),
         name='registrar-movimiento'),
    path('login/', LoginEncargadoView.as_view(), name='login'),
]
