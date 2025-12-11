# -*- coding: utf-8 -*-

from django.db import models
from TipoDocumento import TipoDocumento


class EncargadoInventario(models.Model):
    class Meta:
        pass

    nombre_completo = models.TextField()
    fecha_contrato = models.DateField()
    tipo_documento = models.CharField(
        max_length=20, choices=[(tag.name, tag.value) for tag in TipoDocumento])
