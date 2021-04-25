from djongo import models

# Create your models here.

class voice(models.Model):
    data = models.JSONField()
