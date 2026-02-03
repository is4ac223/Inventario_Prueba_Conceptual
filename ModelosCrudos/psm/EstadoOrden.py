#-*- coding: utf-8 -*-
from enum import Enum

class EstadoOrden(Enum):
    SOLICITADA = 1
    PENDIENTE = 2
    APROBADA = 3
    RECHAZADA = 4
