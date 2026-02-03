#-*- coding: utf-8 -*-
from django.db import models

class MovimientoInventario(models.Model):
    class Meta:
        pass

    idMovimiento = None
    fechaLlegada = models.CharField()
    cantidad = models.CharField()
    responsableEjecuta = None
    motivo = models.CharField()
    fechaRegistro = models.CharField()
    itemMovido = models.CharField()

