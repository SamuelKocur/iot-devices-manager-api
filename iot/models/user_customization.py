from django.db import models
from django.conf import settings


class FavoriteSensor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_sensors')
    sensor = models.ForeignKey('iot.Sensor', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('user', 'sensor',)
        ordering = ['-date_created']


class UserSensorName(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sensor_names')
    sensor = models.ForeignKey('iot.Sensor', on_delete=models.CASCADE, related_name='user_names')
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('user', 'sensor',)
        ordering = ['-date_created']


class UserLocationName(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location_names')
    location = models.ForeignKey('iot.Location', on_delete=models.CASCADE, related_name='user_names')
    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('user', 'location',)
        ordering = ['-date_created']
