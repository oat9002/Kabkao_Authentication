from django.db import models

class Hello(models.Model):
    hi = models.FloatField(default=0.0)
    lo = models.FloatField(default=0.0)