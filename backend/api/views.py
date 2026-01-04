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


class MateriaPrimaListCreateView(APIView):
    """Vista para listar y crear materias primas"""

    def get(self, request):
        """Obtener todas las materias primas"""
        materias_primas = MateriaPrima.objects.all()
        serializer = MateriaPrimaSerializer(materias_primas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Crear una nueva materia prima"""
        serializer = MateriaPrimaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MateriaPrimaDetailView(APIView):
    """Vista para obtener, actualizar y eliminar una materia prima"""

    def get_object(self, pk):
        try:
            return MateriaPrima.objects.get(pk=pk)
        except MateriaPrima.DoesNotExist:
            return None

    def get(self, request, pk):
        """Obtener una materia prima específica"""
        materia_prima = self.get_object(pk)
        if not materia_prima:
            return Response(
                {'error': 'Materia prima no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MateriaPrimaSerializer(materia_prima)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Actualizar una materia prima"""
        materia_prima = self.get_object(pk)
        if not materia_prima:
            return Response(
                {'error': 'Materia prima no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MateriaPrimaSerializer(materia_prima, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Eliminar una materia prima"""
        materia_prima = self.get_object(pk)
        if not materia_prima:
            return Response(
                {'error': 'Materia prima no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        materia_prima.delete()
        return Response(
            {'mensaje': 'Materia prima eliminada exitosamente'},
            status=status.HTTP_204_NO_CONTENT
        )


class ProductoListCreateView(APIView):
    """Vista para listar y crear productos"""

    def get(self, request):
        """Obtener todos los productos"""
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Crear un nuevo producto"""
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetailView(APIView):
    """Vista para obtener, actualizar y eliminar un producto"""

    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None

    def get(self, request, pk):
        """Obtener un producto específico"""
        producto = self.get_object(pk)
        if not producto:
            return Response(
                {'error': 'Producto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Actualizar un producto"""
        producto = self.get_object(pk)
        if not producto:
            return Response(
                {'error': 'Producto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Eliminar un producto"""
        producto = self.get_object(pk)
        if not producto:
            return Response(
                {'error': 'Producto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        producto.delete()
        return Response(
            {'mensaje': 'Producto eliminado exitosamente'},
            status=status.HTTP_204_NO_CONTENT
        )


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
            motivo=motivo,
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
        print(
            f"Todos los que existen son: {EncargadoInventario.objects.all()}")

        if not nombre:
            return Response({
                'error': 'Debe ingresar el nombre completo'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(
                f"Todos los que existen son: {EncargadoInventario.objects.all()}")
            encargado = EncargadoInventario.objects.get(
                nombre_completo__iexact=nombre)
            serializer = EncargadoInventarioSerializer(encargado)
            return Response({
                'mensaje': 'Login exitoso',
                'encargado': serializer.data
            }, status=status.HTTP_200_OK)
        except EncargadoInventario.DoesNotExist:
            print(
                f"Todos los que existen son: {EncargadoInventario.objects.all()}")
            return Response({
                'error': 'Encargado no encontrado. Verifique el nombre.'
            }, status=status.HTTP_404_NOT_FOUND)
        print("no existes pendejo")
