# -*- coding: utf-8 -*-

from django.db import models
from encargadoinventario import EncargadoInventario
from TipoMovimiento import TipoMovimiento


class MovimientoInventario(models.Model):
    class Meta:
        pass

    fecha = models.DateField()
    cantidad = models.IntegerField()
    encargado = models.ForeignKey(
        EncargadoInventario, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(
        max_length=20, choices=[(tag.name, tag.value) for tag in TipoMovimiento])
