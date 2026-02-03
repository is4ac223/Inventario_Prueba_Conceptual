# -*- coding: utf-8 -*-
"""
Patrón Observer para notificaciones de inventario.
Permite notificar a suscriptores cuando ocurren eventos en el inventario.
"""
from abc import ABC, abstractmethod
from typing import List


class Subscriber(ABC):
    """
    Interfaz para suscriptores del patrón Observer.
    No se persiste en la base de datos.
    """

    @abstractmethod
    def actualizar(self, mensaje):
        """
        Método llamado cuando ocurre un evento.

        Args:
            mensaje: Información sobre el evento
        """
        pass


class ServicioNotificaciones(Subscriber):
    """
    Servicio concreto de notificaciones.
    Implementa el patrón Observer como suscriptor.
    """

    def __init__(self):
        self.notificaciones = []

    def actualizar(self, mensaje):
        """
        Recibe y almacena notificaciones.

        Args:
            mensaje: Mensaje de notificación
        """
        from api.models import Notificacion
        from datetime import datetime

        # Crear notificación en la base de datos
        notificacion = Notificacion.objects.create(
            mensaje=mensaje,
            fecha_generacion=datetime.now()
        )

        self.notificaciones.append(notificacion)
        return notificacion


class InventarioPublisher:
    """
    Publisher/Subject del patrón Observer.
    Gestiona suscriptores y envía notificaciones.
    """

    def __init__(self):
        self._subscribers: List[Subscriber] = []

    def suscribir(self, subscriber: Subscriber):
        """Agrega un suscriptor"""
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def desuscribir(self, subscriber: Subscriber):
        """Elimina un suscriptor"""
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notificar(self, mensaje):
        """Notifica a todos los suscriptores"""
        for subscriber in self._subscribers:
            subscriber.actualizar(mensaje)

    def notificar_stock_bajo(self, item_inventario):
        """Notifica cuando el stock está bajo el mínimo"""
        if item_inventario.stock_actual <= item_inventario.stock_minimo:
            mensaje = (
                f"ALERTA: Stock bajo para {item_inventario.nombre}. "
                f"Stock actual: {item_inventario.stock_actual}, "
                f"Stock mínimo: {item_inventario.stock_minimo}"
            )
            self.notificar(mensaje)

    def notificar_movimiento(self, movimiento):
        """Notifica cuando se registra un movimiento"""
        mensaje = (
            f"Movimiento registrado: {movimiento.get_tipo_movimiento_display()} "
            f"de {movimiento.cantidad} unidades. "
            f"Fecha: {movimiento.fecha}"
        )
        self.notificar(mensaje)
