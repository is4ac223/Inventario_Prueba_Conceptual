#-*- coding: utf-8 -*-
from django.db import models

class EncargadoInventario(models.Model):
    class Meta:
        pass

    idEmpleado = None
    nombreCompleto = models.CharField()
    fechaContrato = models.CharField()

