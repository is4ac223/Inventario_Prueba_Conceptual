#-*- coding: utf-8 -*-

from django.db import models

class ItemInventario(models.Model):
    class Meta:
        pass

    nombre = models.TextField()
    stock_minimo = models.IntegerField()
    stock_actual = models.PositiveIntegerField()


