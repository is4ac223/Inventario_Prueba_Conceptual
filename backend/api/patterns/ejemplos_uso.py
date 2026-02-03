# -*- coding: utf-8 -*-
"""
Ejemplos de uso de los patrones de diseño.
Este archivo NO debe ejecutarse directamente, es solo referencia.
"""

# ==============================================================================
# EJEMPLO 1: Usar Command Pattern para registrar movimientos
# ==============================================================================


def ejemplo_command_entrada():
    """Ejemplo de uso del patrón Command para entradas"""
    from api.models import MateriaPrima, EncargadoInventario
    from api.patterns import EntradaCommand, RegistroMovimientoService

    # Obtener objetos necesarios
    materia_prima = MateriaPrima.objects.get(nombre="Harina")
    encargado = EncargadoInventario.objects.first()

    # Crear comando de entrada
    comando_entrada = EntradaCommand(
        cantidad=50,
        item_inventario=materia_prima,
        encargado=encargado,
        motivo="Reposición mensual"
    )

    # Ejecutar comando a través del servicio
    servicio = RegistroMovimientoService()
    movimiento = servicio.procesar(comando_entrada)

    print(f"Movimiento registrado: {movimiento}")
    print(f"Nuevo stock: {materia_prima.stock_actual}")


def ejemplo_command_salida():
    """Ejemplo de uso del patrón Command para salidas"""
    from api.models import Producto, EncargadoInventario
    from api.patterns import SalidaCommand, RegistroMovimientoService

    # Obtener objetos necesarios
    producto = Producto.objects.get(nombre="Pan")
    encargado = EncargadoInventario.objects.first()

    # Crear comando de salida
    comando_salida = SalidaCommand(
        cantidad=20,
        item_inventario=producto,
        encargado=encargado,
        motivo="Venta al cliente"
    )

    # Ejecutar comando
    servicio = RegistroMovimientoService()
    try:
        movimiento = servicio.procesar(comando_salida)
        print(f"Salida registrada: {movimiento}")
    except ValueError as e:
        print(f"Error: {e}")  # Se captura si no hay stock suficiente


# ==============================================================================
# EJEMPLO 2: Usar Observer Pattern para notificaciones
# ==============================================================================

def ejemplo_observer_notificaciones():
    """Ejemplo de uso del patrón Observer para notificar eventos"""
    from api.models import MateriaPrima
    from api.patterns import InventarioPublisher, ServicioNotificaciones

    # Crear el publisher y el servicio de notificaciones
    publisher = InventarioPublisher()
    servicio_notificaciones = ServicioNotificaciones()

    # Suscribir el servicio de notificaciones
    publisher.suscribir(servicio_notificaciones)

    # Obtener un item con stock bajo
    materia_prima = MateriaPrima.objects.get(nombre="Azúcar")
    materia_prima.stock_actual = 5  # Simular stock bajo
    materia_prima.stock_minimo = 10
    materia_prima.save()

    # Notificar sobre stock bajo
    publisher.notificar_stock_bajo(materia_prima)

    # Ver notificaciones creadas
    from api.models import Notificacion
    notificaciones = Notificacion.objects.all()
    for notif in notificaciones:
        print(f"Notificación: {notif.mensaje}")


def ejemplo_observer_movimiento():
    """Ejemplo de notificación al registrar un movimiento"""
    from api.models import MovimientoInventario, EncargadoInventario
    from api.patterns import InventarioPublisher, ServicioNotificaciones

    # Configurar observer
    publisher = InventarioPublisher()
    servicio_notif = ServicioNotificaciones()
    publisher.suscribir(servicio_notif)

    # Crear un movimiento
    encargado = EncargadoInventario.objects.first()
    movimiento = MovimientoInventario.objects.create(
        cantidad=100,
        encargado=encargado,
        tipo_movimiento='ENTRADA',
        motivo="Prueba de notificación"
    )

    # Notificar el movimiento
    publisher.notificar_movimiento(movimiento)


# ==============================================================================
# EJEMPLO 3: Usar Memento Pattern para respaldos
# ==============================================================================

def ejemplo_memento_respaldo():
    """Ejemplo de uso del patrón Memento para respaldos"""
    from api.models import Inventario
    from api.patterns import HistorialInventario

    # Obtener inventario
    inventario = Inventario.objects.first()

    # Crear caretaker para manejar historial
    historial = HistorialInventario()

    # Guardar estado actual
    estado_inicial = historial.respaldar(inventario)
    print(f"Estado respaldado: {estado_inicial.ubicacion_almacenamiento}")

    # Hacer cambios al inventario
    inventario.ubicacion_almacenamiento = "Bodega B - Zona Norte"
    inventario.capacidad_maxima = 5000
    inventario.save()
    print(f"Inventario modificado: {inventario.ubicacion_almacenamiento}")

    # Guardar otro estado
    estado_modificado = historial.respaldar(inventario)

    # Hacer más cambios
    inventario.ubicacion_almacenamiento = "Bodega C - Zona Este"
    inventario.save()

    # Deshacer último cambio (restaurar estado_modificado)
    estado_restaurado = historial.deshacer(inventario)
    print(f"Estado restaurado: {inventario.ubicacion_almacenamiento}")

    # Deshacer otro cambio (restaurar estado_inicial)
    estado_restaurado = historial.deshacer(inventario)
    print(
        f"Estado restaurado al inicial: {inventario.ubicacion_almacenamiento}")


def ejemplo_memento_con_modelo():
    """Ejemplo usando el método integrado en el modelo"""
    from api.models import Inventario

    # Obtener inventario
    inventario = Inventario.objects.first()

    # Usar método del modelo para guardar estado
    estado = inventario.guardar_estado()
    print(f"Estado guardado: {estado.to_dict()}")

    # Hacer cambios
    inventario.ubicacion_almacenamiento = "Nueva ubicación"
    inventario.save()

    # Restaurar estado anterior
    inventario.restaurar_estado(estado)
    print(f"Estado restaurado: {inventario.ubicacion_almacenamiento}")


# ==============================================================================
# EJEMPLO 4: Integración completa - Workflow real
# ==============================================================================

def ejemplo_workflow_completo():
    """Ejemplo de un workflow completo usando todos los patrones"""
    from api.models import MateriaPrima, EncargadoInventario, Inventario
    from api.patterns import (
        EntradaCommand, RegistroMovimientoService,
        InventarioPublisher, ServicioNotificaciones,
        HistorialInventario
    )

    # 1. Configurar observer para notificaciones
    publisher = InventarioPublisher()
    servicio_notif = ServicioNotificaciones()
    publisher.suscribir(servicio_notif)

    # 2. Obtener datos necesarios
    materia_prima = MateriaPrima.objects.get(nombre="Levadura")
    encargado = EncargadoInventario.objects.first()
    inventario = materia_prima.inventario

    # 3. Guardar estado del inventario (Memento)
    historial = HistorialInventario()
    estado_antes = historial.respaldar(inventario)

    # 4. Registrar entrada usando Command
    comando = EntradaCommand(
        cantidad=100,
        item_inventario=materia_prima,
        encargado=encargado,
        motivo="Pedido semanal"
    )

    servicio = RegistroMovimientoService()
    movimiento = servicio.procesar(comando)

    # 5. Notificar movimiento (Observer)
    publisher.notificar_movimiento(movimiento)

    # 6. Verificar si hay stock bajo
    if materia_prima.stock_actual <= materia_prima.stock_minimo:
        publisher.notificar_stock_bajo(materia_prima)

    # 7. Actualizar totales del inventario
    inventario.actualizar_totales()

    print("Workflow completado exitosamente")
    print(f"- Movimiento: {movimiento}")
    print(f"- Stock actual: {materia_prima.stock_actual}")
    print(f"- Notificaciones generadas: {servicio_notif.notificaciones}")


# ==============================================================================
# NOTAS DE USO
# ==============================================================================

"""
IMPORTANTE:
- Los patrones NO se deben usar directamente en los templates o serializadores
- Deben usarse en:
  * Vistas (views.py)
  * Servicios personalizados (si creas una capa de servicios)
  * Signals de Django (para automatizar acciones)
  * Tareas asíncronas (Celery)

MEJORES PRÁCTICAS:
1. Command: Usar para operaciones que modifican el inventario
2. Observer: Usar para notificaciones y logs de auditoría
3. Memento: Usar para respaldos antes de operaciones críticas

EVITAR:
- No usar los patrones en los modelos directamente (solo métodos auxiliares)
- No intentar persistir las clases de patrones como modelos
- No mezclar responsabilidades (cada patrón tiene su propósito)
"""
