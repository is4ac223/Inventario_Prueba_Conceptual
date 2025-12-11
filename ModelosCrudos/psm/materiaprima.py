# -*- coding: utf-8 -*-

from django.db import models

from iteminventario import ItemInventario
from inventario import Inventario


class MateriaPrima(ItemInventario):
    class Meta:
        pass

    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    inventario = models.ForeignKey(
        Inventario, on_delete=models.CASCADE, related_name='materias_primas')
