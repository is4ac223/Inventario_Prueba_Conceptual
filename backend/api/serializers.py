from rest_framework import serializers
from .models import (
    EncargadoInventario, Inventario, MovimientoInventario,
    MateriaPrima, Producto, TipoMovimiento, Notificacion
)


class EncargadoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncargadoInventario
        fields = ['id', 'nombre_completo', 'fecha_contrato', 'tipo_documento']


class EncargadoInventarioLoginSerializer(serializers.Serializer):
    """Serializer para el login de encargados"""
    nombre_completo = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)

    def validate(self, data):
        """Valida las credenciales del usuario"""
        nombre = data.get('nombre_completo', '').strip()
        password = data.get('password', '').strip()

        if not nombre or not password:
            raise serializers.ValidationError(
                'Nombre de usuario y contraseña son requeridos')

        try:
            encargado = EncargadoInventario.objects.get(
                nombre_completo__iexact=nombre)
            if not encargado.check_password(password):
                raise serializers.ValidationError('Contraseña incorrecta')
            data['encargado'] = encargado
        except EncargadoInventario.DoesNotExist:
            raise serializers.ValidationError('Encargado no encontrado')

        return data


class InventarioSerializer(serializers.ModelSerializer):
    materias_primas_count = serializers.SerializerMethodField()
    productos_count = serializers.SerializerMethodField()

    class Meta:
        model = Inventario
        fields = ['id', 'ubicacion_almacenamiento', 'capacidad_maxima',
                  'fecha_ultima_revision', 'materias_primas_count', 'productos_count']

    def get_materias_primas_count(self, obj):
        return obj.materias_primas.count()

    def get_productos_count(self, obj):
        return obj.productos.count()


class MateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriaPrima
        fields = ['id', 'nombre', 'descripcion', 'stock_minimo', 'stock_actual',
                  'costo_unitario', 'inventario']
        extra_kwargs = {
            'inventario': {'required': False}
        }

    def create(self, validated_data):
        # Si no se proporciona inventario, usar el primero disponible o crear uno
        if 'inventario' not in validated_data:
            inventario = Inventario.objects.first()
            if not inventario:
                from datetime import date
                inventario = Inventario.objects.create(
                    ubicacion_almacenamiento='Principal',
                    capacidad_maxima=10000,
                    fecha_ultima_revision=date.today()
                )
            validated_data['inventario'] = inventario
        return super().create(validated_data)


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'stock_minimo', 'stock_actual',
                  'precio_unitario', 'inventario']
        extra_kwargs = {
            'inventario': {'required': False}
        }

    def create(self, validated_data):
        # Si no se proporciona inventario, usar el primero disponible o crear uno
        if 'inventario' not in validated_data:
            inventario = Inventario.objects.first()
            if not inventario:
                from datetime import date
                inventario = Inventario.objects.create(
                    ubicacion_almacenamiento='Principal',
                    capacidad_maxima=10000,
                    fecha_ultima_revision=date.today()
                )
            validated_data['inventario'] = inventario
        return super().create(validated_data)


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    encargado_nombre = serializers.CharField(
        source='encargado.nombre_completo', read_only=True)
    tipo_movimiento_display = serializers.CharField(
        source='get_tipo_movimiento_display', read_only=True)

    class Meta:
        model = MovimientoInventario
        fields = ['id', 'fecha', 'cantidad', 'tipo_movimiento',
                  'tipo_movimiento_display', 'encargado', 'encargado_nombre', 'inventarios']
        read_only_fields = ['fecha']


class RegistrarMovimientoSerializer(serializers.Serializer):
    """Serializer para registrar movimientos de inventario"""
    item_id = serializers.IntegerField(required=True)
    item_tipo = serializers.ChoiceField(
        choices=['materia_prima', 'producto'], required=True)
    tipo_movimiento = serializers.ChoiceField(
        choices=TipoMovimiento.choices, required=True)
    cantidad = serializers.IntegerField(required=True)
    motivo = serializers.CharField(required=True, max_length=500)
    encargado_id = serializers.IntegerField(required=True)

    def validate_cantidad(self, value):
        if value == 0:
            raise serializers.ValidationError("La cantidad no puede ser cero.")
        return value

    def validate(self, data):
        # Validar que el item existe
        item_tipo = data['item_tipo']
        item_id = data['item_id']

        try:
            if item_tipo == 'materia_prima':
                item = MateriaPrima.objects.get(id=item_id)
            else:
                item = Producto.objects.get(id=item_id)
        except (MateriaPrima.DoesNotExist, Producto.DoesNotExist):
            raise serializers.ValidationError({
                'item_id': 'Ítem no encontrado. Verifique el código.'
            })

        # Validar que el encargado existe
        try:
            encargado = EncargadoInventario.objects.get(
                id=data['encargado_id'])
        except EncargadoInventario.DoesNotExist:
            raise serializers.ValidationError({
                'encargado_id': 'Encargado no encontrado.'
            })

        # Validar stock negativo para SALIDA, AJUSTE, PERDIDA
        tipo_movimiento = data['tipo_movimiento']
        cantidad = data['cantidad']

        if tipo_movimiento in [TipoMovimiento.SALIDA, TipoMovimiento.AJUSTE, TipoMovimiento.PERDIDA]:
            stock_resultante = item.stock_actual - abs(cantidad)
            if stock_resultante < 0:
                data['advertencia'] = f"La pérdida/salida excede el stock actual ({item.stock_actual}). El stock resultante será {stock_resultante}."

        data['item'] = item
        data['encargado'] = encargado

        return data


class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""

    class Meta:
        model = Notificacion
        fields = ['id', 'mensaje', 'fecha_generacion', 'leida']
        read_only_fields = ['id', 'fecha_generacion']
