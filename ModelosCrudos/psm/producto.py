#-*- coding: utf-8 -*-
from django.db import models

from ItemInventario import ItemInventario

class Producto(ItemInventario):
    class Meta:
        pass

    precioUnitario = models.CharField()

