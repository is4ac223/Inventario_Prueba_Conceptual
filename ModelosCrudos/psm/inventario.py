# -*- coding: utf-8 -*-

from django.db import models
from movimientoinventario import MovimientoInventario


class Inventario(models.Model):
    class Meta:
        pass

    ubicacion_almacenamiento = models.CharField(max_length=255)
    capacidad_maxina = models.IntegerField()
    fecha_ultima_revision = models.DateField()
    movimientos = models.ManyToManyField(
        MovimientoInventario, related_name='inventarios')
