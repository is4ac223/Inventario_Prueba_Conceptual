#-*- coding: utf-8 -*-
from django.db import models

class UnidadVentaAgrupada(models.Model):
    class Meta:
        pass

    idUnidadVentaAgrupada = None
    nombre = models.CharField()
    cantidadContenida = models.CharField()
    unidadMedidaBase = models.CharField()

