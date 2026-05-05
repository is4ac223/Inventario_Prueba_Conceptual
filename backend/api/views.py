from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    EncargadoInventario, Inventario, MovimientoInventario,
    MateriaPrima, Producto, TipoMovimiento, Notificacion
)
from .serializers import (
    EncargadoInventarioSerializer, InventarioSerializer,
    MovimientoInventarioSerializer, MateriaPrimaSerializer,
    ProductoSerializer, RegistrarMovimientoSerializer, NotificacionSerializer
)

# Instancia global del historial de inventario para el patrón Memento
# En producción, esto debería manejarse con caché (Redis) o base de datos
_historial_inventario = None


def get_historial_inventario():
    """Obtiene o crea la instancia del historial de inventario"""
    global _historial_inventario
    if _historial_inventario is None:
        from api.patterns.memento import HistorialInventario
        _historial_inventario = HistorialInventario()
    return _historial_inventario


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
    Utiliza patrones de diseño: Command y Observer
    """

    def post(self, request):
        # Importar patrones de diseño
        from api.patterns import (
            EntradaCommand, SalidaCommand, RegistroMovimientoService,
            InventarioPublisher, ServicioNotificaciones
        )

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

        # Guardar stock anterior para la respuesta
        stock_anterior = item.stock_actual

        # ==================================================================
        # USAR PATRÓN COMMAND para ejecutar el movimiento
        # ==================================================================
        try:
            movimiento = None

            if tipo_movimiento == TipoMovimiento.ENTRADA:
                # Usar EntradaCommand
                comando = EntradaCommand(
                    cantidad=abs(cantidad),
                    item_inventario=item,
                    encargado=encargado,
                    motivo=motivo
                )
                servicio = RegistroMovimientoService()
                movimiento = servicio.procesar(comando)

            elif tipo_movimiento in [TipoMovimiento.SALIDA, TipoMovimiento.PERDIDA]:
                # Usar SalidaCommand
                comando = SalidaCommand(
                    cantidad=abs(cantidad),
                    item_inventario=item,
                    encargado=encargado,
                    motivo=motivo
                )
                servicio = RegistroMovimientoService()
                movimiento = servicio.procesar(comando)

            elif tipo_movimiento == TipoMovimiento.AJUSTE:
                # Para ajuste, crear movimiento manualmente
                if cantidad > 0:
                    item.stock_actual += cantidad
                else:
                    item.stock_actual += cantidad  # cantidad ya es negativa
                item.save()

                movimiento = MovimientoInventario.objects.create(
                    cantidad=cantidad,
                    motivo=motivo,
                    tipo_movimiento=tipo_movimiento,
                    encargado=encargado
                )
                movimiento.inventarios.add(item.inventario)

            # ==================================================================
            # USAR PATRÓN OBSERVER para generar notificaciones
            # ==================================================================
            publisher = InventarioPublisher()
            servicio_notificaciones = ServicioNotificaciones()
            publisher.suscribir(servicio_notificaciones)

            # Notificar el movimiento
            if movimiento:
                publisher.notificar_movimiento(movimiento)

            # Verificar si el stock está bajo el mínimo y notificar
            if item.stock_actual <= item.stock_minimo:
                publisher.notificar_stock_bajo(item)

            # ==================================================================
            # Actualizar totales del inventario
            # ==================================================================
            item.inventario.actualizar_totales()

        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'Error al procesar el movimiento: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serializar respuesta
        movimiento_serializer = MovimientoInventarioSerializer(movimiento)

        # Serializar el item actualizado
        if validated_data['item_tipo'] == 'materia_prima':
            item_serializer = MateriaPrimaSerializer(item)
        else:
            item_serializer = ProductoSerializer(item)

        return Response({
            'mensaje': 'Movimiento registrado exitosamente usando patrones de diseño',
            'motivo': motivo,
            'movimiento': movimiento_serializer.data,
            'item_actualizado': item_serializer.data,
            'stock_anterior': stock_anterior,
            'stock_actual': item.stock_actual,
            'alerta_stock_bajo': item.stock_actual <= item.stock_minimo,
            'patrones_usados': ['Command Pattern', 'Observer Pattern']
        }, status=status.HTTP_201_CREATED)


class LoginEncargadoView(APIView):
    """Vista de autenticación segura para encargados"""

    def post(self, request):
        from .serializers import EncargadoInventarioLoginSerializer

        serializer = EncargadoInventarioLoginSerializer(data=request.data)

        if serializer.is_valid():
            encargado = serializer.validated_data['encargado']
            encargado_serializer = EncargadoInventarioSerializer(encargado)
            return Response({
                'mensaje': 'Login exitoso',
                'encargado': encargado_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class NotificacionesViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar notificaciones"""
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        """Ordenar por fecha descendente"""
        return Notificacion.objects.all().order_by('-fecha_generacion')

    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """Obtener solo notificaciones no leídas"""
        notificaciones = self.queryset.filter(leida=False)
        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        """Marcar todas las notificaciones como leídas"""
        count = self.queryset.filter(leida=False).update(leida=True)
        return Response({
            'mensaje': f'{count} notificaciones marcadas como leídas'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """Marcar una notificación como leída"""
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        return Response({
            'mensaje': 'Notificación marcada como leída'
        }, status=status.HTTP_200_OK)


class EstadoInventarioView(APIView):
    """
    Vista para obtener el estado general del inventario.
    Muestra estadísticas y valoración total.
    """

    def get(self, request):
        """Obtener estado del inventario"""
        # Obtener el primer inventario (asumiendo que hay uno principal)
        inventario = Inventario.objects.first()

        if not inventario:
            return Response({
                'error': 'No hay inventario configurado'
            }, status=status.HTTP_404_NOT_FOUND)

        # Contar materias primas y productos
        materias_primas = MateriaPrima.objects.filter(inventario=inventario)
        productos = Producto.objects.filter(inventario=inventario)

        total_materias = materias_primas.count()
        total_productos = productos.count()

        # Calcular stock total
        stock_materias = sum(mp.stock_actual for mp in materias_primas)
        stock_productos = sum(p.stock_actual for p in productos)

        # Calcular valoración (asumiendo precio unitario promedio)
        # Nota: Agregar campo de precio si no existe
        valoracion_total = 0  # Placeholder

        data = {
            'inventario_id': inventario.id,
            'ubicacion': inventario.ubicacion_almacenamiento,
            'capacidad_maxima': inventario.capacidad_maxima,
            'fecha_ultima_revision': inventario.fecha_ultima_revision,
            'estadisticas': {
                'total_tipos_materias_primas': total_materias,
                'total_tipos_productos': total_productos,
                'stock_total_materias_primas': stock_materias,
                'stock_total_productos': stock_productos,
                'valoracion_total': valoracion_total,
            },
            'detalles_materias_primas': [
                {
                    'id': mp.id,
                    'nombre': mp.nombre,
                    'stock_actual': mp.stock_actual,
                    'stock_minimo': mp.stock_minimo
                } for mp in materias_primas[:5]  # Top 5
            ],
            'detalles_productos': [
                {
                    'id': p.id,
                    'nombre': p.nombre,
                    'stock_actual': p.stock_actual,
                    'stock_minimo': p.stock_minimo
                } for p in productos[:5]  # Top 5
            ]
        }

        return Response(data, status=status.HTTP_200_OK)


class GuardarEstadoInventarioView(APIView):
    """
    Vista para guardar un snapshot del inventario usando el patrón Memento.
    """

    def post(self, request):
        """Guardar estado actual del inventario"""
        inventario = Inventario.objects.first()

        if not inventario:
            return Response({
                'error': 'No hay inventario configurado'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            historial = get_historial_inventario()
            estado = historial.respaldar(inventario)

            return Response({
                'mensaje': 'Estado del inventario guardado exitosamente',
                'estado': estado.to_dict(),
                'patron_usado': 'Memento',
                'total_snapshots': len(historial.obtener_historial())
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': f'Error al guardar estado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RestaurarEstadoInventarioView(APIView):
    """
    Vista para restaurar el inventario a un estado anterior.
    Usa el patrón Memento para la restauración.
    """

    def post(self, request):
        """Restaurar inventario al último estado guardado"""
        inventario = Inventario.objects.first()

        if not inventario:
            return Response({
                'error': 'No hay inventario configurado'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            historial = get_historial_inventario()

            # Deshacer al último estado
            estado = historial.deshacer(inventario)

            if estado is None:
                return Response({
                    'error': 'No hay estados anteriores para restaurar'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'mensaje': 'Estado del inventario restaurado exitosamente',
                'estado_restaurado': estado.to_dict(),
                'patron_usado': 'Memento',
                'snapshots_restantes': len(historial.obtener_historial())
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'Error al restaurar estado: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
