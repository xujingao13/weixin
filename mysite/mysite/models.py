from django.db import models


class Record(models.Model):
    user = models.CharField(max_length=30)
    time = models.DateField()
    step = models.IntegerField(max_length=60)
