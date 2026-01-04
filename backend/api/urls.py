from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EncargadoInventarioViewSet, InventarioViewSet,
    MovimientoInventarioViewSet, RegistrarMovimientoView,
    LoginEncargadoView,
    MateriaPrimaListCreateView, MateriaPrimaDetailView,
    ProductoListCreateView, ProductoDetailView
)

router = DefaultRouter()
router.register(r'encargados', EncargadoInventarioViewSet,
                basename='encargado')
router.register(r'inventarios', InventarioViewSet, basename='inventario')
router.register(r'movimientos', MovimientoInventarioViewSet,
                basename='movimiento')

urlpatterns = [
    path('', include(router.urls)),
    path('materias-primas/', MateriaPrimaListCreateView.as_view(),
         name='materias-primas-list'),
    path('materias-primas/<int:pk>/', MateriaPrimaDetailView.as_view(),
         name='materias-primas-detail'),
    path('productos/', ProductoListCreateView.as_view(),
         name='productos-list'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(),
         name='productos-detail'),
    path('registrar-movimiento/', RegistrarMovimientoView.as_view(),
         name='registrar-movimiento'),
    path('login/', LoginEncargadoView.as_view(), name='login'),
]
