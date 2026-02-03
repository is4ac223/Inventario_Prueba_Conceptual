# -*- coding: utf-8 -*-
"""
Patrones de diseño para el sistema de inventario.
Estos patrones no se persisten en la base de datos.
"""

# Command Pattern
from .command import (
    MovimientoCommand,
    EntradaCommand,
    SalidaCommand,
    RegistroMovimientoService
)

# Observer Pattern
from .observer import (
    Subscriber,
    ServicioNotificaciones,
    InventarioPublisher
)

# Memento Pattern
from .memento import (
    EstadoInventario,
    HistorialInventario
)

__all__ = [
    # Command
    'MovimientoCommand',
    'EntradaCommand',
    'SalidaCommand',
    'RegistroMovimientoService',
    # Observer
    'Subscriber',
    'ServicioNotificaciones',
    'InventarioPublisher',
    # Memento
    'EstadoInventario',
    'HistorialInventario',
]
