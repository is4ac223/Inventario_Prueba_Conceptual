#-*- coding: utf-8 -*-
from django.db import models

class Subscriber(models.Model):
    class Meta:
        abstract = True

    def actualizar(self, i):
        pass

