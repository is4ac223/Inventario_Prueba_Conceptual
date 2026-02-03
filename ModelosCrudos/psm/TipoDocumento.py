#-*- coding: utf-8 -*-
from enum import Enum

class TipoDocumento(Enum):
    CEDULA = 1
    DNI = 2
    PASAPORTE = 3
    OTRO = 4
