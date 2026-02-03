#-*- coding: utf-8 -*-
from django.db import models

class OrdenCompra(models.Model):
    class Meta:
        pass

    idOrden = None
    fechaSolcitud = models.CharField()
    estado = None
    responsableAutoriza = models.CharField()

