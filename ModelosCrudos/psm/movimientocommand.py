#-*- coding: utf-8 -*-
from django.db import models

class MovimientoCommand(models.Model):
    class Meta:
        abstract = True

    def ejecutar(self, ):
        pass

