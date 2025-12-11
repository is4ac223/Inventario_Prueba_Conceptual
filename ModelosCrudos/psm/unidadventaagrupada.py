#-*- coding: utf-8 -*-

from django.db import models

class UnidadVentaAgrupada(models.Model):
    class Meta:
        pass

    nombre = models.StringField()
    cantidad_contenida = models.IntegerField()
    unidad_medida_base = models.StringField()


