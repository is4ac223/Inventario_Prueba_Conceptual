from django.contrib import admin
from .models import (
    EncargadoInventario, Inventario, MovimientoInventario,
    MateriaPrima, Producto, OrdenCompra, DetalleOrden,
    UnidadVentaAgrupada, Notificacion
)


@admin.register(EncargadoInventario)
class EncargadoInventarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'tipo_documento', 'fecha_contrato']
    search_fields = ['nombre_completo']


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['ubicacion_almacenamiento',
                    'capacidad_maxima', 'fecha_ultima_revision']


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['tipo_movimiento', 'cantidad',
                    'fecha', 'encargado', 'motivo']
    list_filter = ['tipo_movimiento', 'fecha']
    search_fields = ['motivo']


@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'stock_actual', 'stock_minimo', 'costo_unitario']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'stock_actual',
                    'stock_minimo', 'precio_unitario']
    search_fields = ['nombre']


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_solicitud', 'estado', 'responsable_autoriza']
    list_filter = ['estado', 'fecha_solicitud']


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ['orden_compra', 'materia_prima',
                    'cantidad', 'precio_negociado']


@admin.register(UnidadVentaAgrupada)
class UnidadVentaAgrupadaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad_contenida', 'unidad_medida_base']


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['mensaje_corto', 'fecha_generacion', 'leida']
    list_filter = ['leida', 'fecha_generacion']
    search_fields = ['mensaje']
    date_hierarchy = 'fecha_generacion'

    def mensaje_corto(self, obj):
        return obj.mensaje[:50] + '...' if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje'
