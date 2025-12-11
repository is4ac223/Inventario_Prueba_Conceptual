# -*- coding: utf-8 -*-

from django.db import models
from ordencompra import OrdenCompra
from materiaprima import MateriaPrima


class DetalleOrden(models.Model):
    class Meta:
        pass

    cantidad = models.IntegerField()
    precio_negociado = models.DecimalField(max_digits=10, decimal_places=2)
    orden_compra = models.ForeignKey(
        OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    materia_prima = models.ForeignKey(
        MateriaPrima, on_delete=models.CASCADE, related_name='detalles_orden')
