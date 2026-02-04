# -*- coding: utf-8 -*-
"""
Patrón Command para movimientos de inventario.
Define comandos para ejecutar operaciones de entrada y salida.
"""
from abc import ABC, abstractmethod


class MovimientoCommand(ABC):
    """
    Clase abstracta base para comandos de movimiento.
    Patrón Command - no se persiste en la base de datos.
    """

    @abstractmethod
    def ejecutar(self):
        """Ejecuta el comando de movimiento"""
        pass


class EntradaCommand(MovimientoCommand):
    """
    Comando para registrar entradas de inventario.
    """

    def __init__(self, cantidad, item_inventario, encargado, motivo=""):
        self.cantidad = cantidad
        self.item_inventario = item_inventario
        self.encargado = encargado
        self.motivo = motivo

    def ejecutar(self):
        """Ejecuta el comando de entrada"""
        from api.models import MovimientoInventario, TipoMovimiento

        # Actualizar stock
        self.item_inventario.stock_actual += self.cantidad
        self.item_inventario.save()

        # Registrar movimiento (fecha y fecha_registro se asignan automáticamente)
        movimiento = MovimientoInventario.objects.create(
            cantidad=self.cantidad,
            item_movido=self.item_inventario.nombre,
            motivo=self.motivo,
            encargado=self.encargado,
            tipo_movimiento=TipoMovimiento.ENTRADA
        )

        return movimiento


class SalidaCommand(MovimientoCommand):
    """
    Comando para registrar salidas de inventario.
    """

    def __init__(self, cantidad, item_inventario, encargado, motivo=""):
        self.cantidad = cantidad
        self.item_inventario = item_inventario
        self.encargado = encargado
        self.motivo = motivo

    def ejecutar(self):
        """Ejecuta el comando de salida"""
        from api.models import MovimientoInventario, TipoMovimiento

        # Verificar stock disponible
        if self.item_inventario.stock_actual < self.cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {self.item_inventario.stock_actual}")

        # Actualizar stock
        self.item_inventario.stock_actual -= self.cantidad
        self.item_inventario.save()

        # Registrar movimiento (fecha y fecha_registro se asignan automáticamente)
        movimiento = MovimientoInventario.objects.create(
            cantidad=self.cantidad,
            item_movido=self.item_inventario.nombre,
            motivo=self.motivo,
            encargado=self.encargado,
            tipo_movimiento=TipoMovimiento.SALIDA
        )

        return movimiento


class RegistroMovimientoService:
    """
    Servicio para procesar comandos de movimiento.
    Invoker del patrón Command.
    """

    def procesar(self, comando):
        """
        Procesa un comando de movimiento.

        Args:
            comando: Instancia de MovimientoCommand

        Returns:
            El resultado de ejecutar el comando
        """
        if not isinstance(comando, MovimientoCommand):
            raise TypeError(
                "El comando debe ser una instancia de MovimientoCommand")

        return comando.ejecutar()
