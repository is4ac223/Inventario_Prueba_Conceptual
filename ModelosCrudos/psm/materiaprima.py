#-*- coding: utf-8 -*-
from django.db import models

from ItemInventario import ItemInventario

class MateriaPrima(ItemInventario):
    class Meta:
        pass

    costoUnitario = models.CharField()

