# -*- coding: utf-8 -*-

from django.db import models

from iteminventario import ItemInventario
from inventario import Inventario
from unidadventaagrupada import UnidadVentaAgrupada


class Producto(ItemInventario):
    class Meta:
        pass

    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    inventario = models.ForeignKey(
        Inventario, on_delete=models.CASCADE, related_name='productos')
    unidades_venta = models.ManyToManyField(
        UnidadVentaAgrupada, related_name='productos')
