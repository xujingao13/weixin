from django.db import models

class Record(models.Model):
    user = models.CharField(max_length=30)
    step = models.IntegerField(max_length=60)
    time = models.DateField(auto_now_add = True)
