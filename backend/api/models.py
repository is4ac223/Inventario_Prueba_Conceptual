from django.db import models


# Enumeraciones
class EstadoOrden(models.TextChoices):
    SOLICITADA = 'SOLICITADA', 'Solicitada'
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    APROBADA = 'APROBADA', 'Aprobada'
    RECHAZADA = 'RECHAZADA', 'Rechazada'


class TipoDocumento(models.TextChoices):
    CEDULA = 'CEDULA', 'Cédula'
    DNI = 'DNI', 'DNI'
    PASAPORTE = 'PASAPORTE', 'Pasaporte'
    OTRO = 'OTRO', 'Otro'


class TipoMovimiento(models.TextChoices):
    ENTRADA = 'ENTRADA', 'Entrada'
    SALIDA = 'SALIDA', 'Salida'
    AJUSTE = 'AJUSTE', 'Ajuste'
    PERDIDA = 'PERDIDA', 'Pérdida'


# Modelos base
class ItemInventario(models.Model):
    """Clase base abstracta para productos y materias primas"""
    nombre = models.TextField()
    stock_minimo = models.IntegerField()
    stock_actual = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre


class UnidadVentaAgrupada(models.Model):
    """Unidades de venta agrupadas para productos"""
    nombre = models.CharField(max_length=100)
    cantidad_contenida = models.IntegerField()
    unidad_medida_base = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Unidad de Venta Agrupada'
        verbose_name_plural = 'Unidades de Venta Agrupadas'

    def __str__(self):
        return f"{self.nombre} ({self.cantidad_contenida} {self.unidad_medida_base})"


class EncargadoInventario(models.Model):
    """Encargados del inventario"""
    nombre_completo = models.TextField()
    fecha_contrato = models.DateField()
    tipo_documento = models.CharField(
        max_length=20,
        choices=TipoDocumento.choices
    )

    class Meta:
        verbose_name = 'Encargado de Inventario'
        verbose_name_plural = 'Encargados de Inventario'

    def __str__(self):
        return self.nombre_completo


class Inventario(models.Model):
    """Inventario general"""
    ubicacion_almacenamiento = models.CharField(max_length=255)
    capacidad_maxima = models.IntegerField()
    fecha_ultima_revision = models.DateField()

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f"Inventario - {self.ubicacion_almacenamiento}"


class MovimientoInventario(models.Model):
    """Movimientos del inventario"""
    fecha = models.DateField()
    cantidad = models.IntegerField()
    encargado = models.ForeignKey(
        EncargadoInventario,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TipoMovimiento.choices
    )
    inventarios = models.ManyToManyField(
        Inventario,
        related_name='movimientos'
    )

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} - {self.fecha}"


class MateriaPrima(ItemInventario):
    """Materias primas del inventario"""
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,
        related_name='materias_primas'
    )

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materias Primas'

    def __str__(self):
        return f"{self.nombre} - ${self.costo_unitario}"


class Producto(ItemInventario):
    """Productos del inventario"""
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    unidades_venta = models.ManyToManyField(
        UnidadVentaAgrupada,
        related_name='productos'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre} - ${self.precio_unitario}"


class OrdenCompra(models.Model):
    """Órdenes de compra"""
    fecha_solicitud = models.DateField()
    responsable_autoriza = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=EstadoOrden.choices,
        default=EstadoOrden.SOLICITADA
    )

    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Orden #{self.id} - {self.get_estado_display()}"


class DetalleOrden(models.Model):
    """Detalles de las órdenes de compra"""
    cantidad = models.IntegerField()
    precio_negociado = models.DecimalField(max_digits=10, decimal_places=2)
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    materia_prima = models.ForeignKey(
        MateriaPrima,
        on_delete=models.CASCADE,
        related_name='detalles_orden'
    )

    class Meta:
        verbose_name = 'Detalle de Orden'
        verbose_name_plural = 'Detalles de Órdenes'

    def __str__(self):
        return f"{self.materia_prima.nombre} x {self.cantidad}"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_negociado
