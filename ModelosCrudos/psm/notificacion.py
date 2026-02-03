#-*- coding: utf-8 -*-
from django.db import models

class Notificacion(models.Model):
    class Meta:
        pass

    Mensaje = models.CharField()
    FechaGeneracion = models.CharField()

