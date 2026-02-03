#-*- coding: utf-8 -*-
from django.db import models

class TransaccionInventario(models.Model):
    class Meta:
        pass

    fechaTransformacionInventario = models.CharField()
    descripcion = models.CharField()

