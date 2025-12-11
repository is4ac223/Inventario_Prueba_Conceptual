from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    EncargadoInventario, Inventario, MovimientoInventario,
    MateriaPrima, Producto, TipoMovimiento
)
from .serializers import (
    EncargadoInventarioSerializer, InventarioSerializer,
    MovimientoInventarioSerializer, MateriaPrimaSerializer,
    ProductoSerializer, RegistrarMovimientoSerializer
)


class EncargadoInventarioViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar encargados de inventario"""
    queryset = EncargadoInventario.objects.all()
    serializer_class = EncargadoInventarioSerializer


class InventarioViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar inventarios"""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class MateriaPrimaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar materias primas"""
    queryset = MateriaPrima.objects.all()
    serializer_class = MateriaPrimaSerializer

    @action(detail=False, methods=['get'])
    def con_stock(self, request):
        """Obtener solo items con stock"""
        items = self.queryset.filter(stock_actual__gt=0)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar productos"""
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def con_stock(self, request):
        """Obtener solo items con stock"""
        items = self.queryset.filter(stock_actual__gt=0)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)


class MovimientoInventarioViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para consultar movimientos de inventario"""
    queryset = MovimientoInventario.objects.all().order_by('-fecha', '-id')
    serializer_class = MovimientoInventarioSerializer


class RegistrarMovimientoView(APIView):
    """
    Vista para registrar movimientos de inventario.
    Implementa el caso de uso "Registrar movimiento de inventario"
    """

    def post(self, request):
        serializer = RegistrarMovimientoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        item = validated_data['item']
        encargado = validated_data['encargado']
        tipo_movimiento = validated_data['tipo_movimiento']
        cantidad = validated_data['cantidad']
        motivo = validated_data['motivo']

        # Verificar advertencia de stock negativo
        advertencia = validated_data.get('advertencia')
        confirmar = request.data.get('confirmar', False)

        if advertencia and not confirmar:
            return Response({
                'advertencia': advertencia,
                'requiere_confirmacion': True
            }, status=status.HTTP_200_OK)

        # Actualizar stock según el tipo de movimiento
        if tipo_movimiento == TipoMovimiento.ENTRADA:
            item.stock_actual += abs(cantidad)
        elif tipo_movimiento in [TipoMovimiento.SALIDA, TipoMovimiento.PERDIDA]:
            item.stock_actual -= abs(cantidad)
        elif tipo_movimiento == TipoMovimiento.AJUSTE:
            # Para ajuste, cantidad positiva suma, negativa resta
            item.stock_actual += cantidad

        item.save()

        # Crear el movimiento
        movimiento = MovimientoInventario.objects.create(
            fecha=timezone.now().date(),
            cantidad=cantidad,
            tipo_movimiento=tipo_movimiento,
            encargado=encargado
        )

        # Asociar con el inventario del item
        movimiento.inventarios.add(item.inventario)

        # Serializar respuesta
        movimiento_serializer = MovimientoInventarioSerializer(movimiento)

        # Serializar el item actualizado
        if validated_data['item_tipo'] == 'materia_prima':
            item_serializer = MateriaPrimaSerializer(item)
        else:
            item_serializer = ProductoSerializer(item)

        return Response({
            'mensaje': 'Movimiento registrado exitosamente',
            'motivo': motivo,
            'movimiento': movimiento_serializer.data,
            'item_actualizado': item_serializer.data,
            'stock_anterior': item.stock_actual - cantidad if tipo_movimiento == TipoMovimiento.ENTRADA else item.stock_actual + abs(cantidad),
            'stock_actual': item.stock_actual
        }, status=status.HTTP_201_CREATED)


class LoginEncargadoView(APIView):
    """Vista simple de autenticación para encargados"""

    def post(self, request):
        nombre = request.data.get('nombre_completo', '').strip()

        if not nombre:
            return Response({
                'error': 'Debe ingresar el nombre completo'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            encargado = EncargadoInventario.objects.get(
                nombre_completo__iexact=nombre)
            serializer = EncargadoInventarioSerializer(encargado)
            return Response({
                'mensaje': 'Login exitoso',
                'encargado': serializer.data
            }, status=status.HTTP_200_OK)
        except EncargadoInventario.DoesNotExist:
            return Response({
                'error': 'Encargado no encontrado. Verifique el nombre.'
            }, status=status.HTTP_404_NOT_FOUND)
