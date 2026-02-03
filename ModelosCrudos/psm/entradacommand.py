#-*- coding: utf-8 -*-
from django.db import models

from MovimientoCommand import MovimientoCommand

class EntradaCommand(MovimientoCommand):
    class Meta:
        pass

    cantidad = models.CharField()

