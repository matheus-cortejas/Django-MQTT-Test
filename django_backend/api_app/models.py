# models.py
from django.db import models

class SensorData(models.Model):
    sensor_id = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
