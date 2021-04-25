from djongo import models

class Pose(models.Model):
    data = models.JSONField()
