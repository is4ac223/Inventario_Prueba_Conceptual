#-*- coding: utf-8 -*-
from django.db import models

class EstadoInventario(models.Model):
    class Meta:
        pass

    ubicacionAlmacenamiento = models.CharField()
    capacidadMaxina = models.CharField()
    fechaUltimaRevision = models.CharField()
    totalMateriaPrima = models.CharField()
    totalProducto = models.CharField()

