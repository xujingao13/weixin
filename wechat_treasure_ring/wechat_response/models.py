from django.db import models


class RingUser(models.Model):
    user_id = models.CharField(max_length=30, primary_key=True)
    sex = models.CharField(max_length=30)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    target = models.IntegerField()
    last_record = models.IntegerField()


class Record(models.Model):
    user_name = models.CharField(max_length=30)
    startTime = models.IntegerField()
    endTime = models.IntegerField()
    type = models.IntegerField()
    distance = models.IntegerField()
    #speed = models.FloatField()
    calories = models.IntegerField()
    steps = models.IntegerField()
    subType = models.IntegerField()
    actTime = models.IntegerField()
    nonActTime = models.IntegerField()
    dsNum = models.IntegerField()
    lsNum = models.IntegerField()
    wakeNum = models.IntegerField()
    wakeTimes = models.IntegerField()
    score = models.FloatField()


