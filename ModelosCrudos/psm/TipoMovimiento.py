#!/usr/bin/python
#-*- coding: utf-8 -*-

from enum import Enum

class TipoMovimiento(Enum):
    ENTRADA = 1
    SALIDA = 2
    AJUSTE = 3
    PERDIDA = 4
