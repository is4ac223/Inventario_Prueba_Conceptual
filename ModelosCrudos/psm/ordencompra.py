# -*- coding: utf-8 -*-

from django.db import models
from EstadoOrden import EstadoOrden


class OrdenCompra(models.Model):
    class Meta:
        pass

    fecha_solcitud = models.DateField()
    responsable_autoriza = models.TextField()
    estado = models.CharField(max_length=20, choices=[
                              (tag.name, tag.value) for tag in EstadoOrden])
