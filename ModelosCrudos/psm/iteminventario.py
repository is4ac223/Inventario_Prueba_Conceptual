#-*- coding: utf-8 -*-
from django.db import models

class ItemInventario(models.Model):
    class Meta:
        pass

    nombre = models.CharField()
    stockActual = models.CharField()
    stockMinimo = models.CharField()
    descripcion = models.CharField()

    def subscribir(self, s):
        pass

    def desuscribir(self, s):
        pass

    def notificar(self, ):
        pass

