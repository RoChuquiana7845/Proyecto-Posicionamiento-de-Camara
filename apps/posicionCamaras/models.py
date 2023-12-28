# posicionCamaras/models.py
from django.db import models

class Posicion(models.Model):
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f'Posición ({self.x}, {self.y})'
