from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db import models

from user_auth.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    verified = models.BooleanField(default=False)
    sensor_groups = models.ManyToManyField('iot.SensorGroup', through='UserSensorGroup', related_name='users')

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"


class UserGroup(Group):
    pass


class UserSensorGroup(models.Model):
    sensor_group = models.ForeignKey('iot.SensorGroup', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sensor_group', 'user',)
        db_table = 'user_sensor_groups'
        verbose_name = 'User sensor group'
        verbose_name_plural = 'User sensor groups'


class UserAppSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='app_setting', primary_key=True)
    date_format = models.CharField(max_length=30, default='d MMM y H:mm')
    get_data_for = models.CharField(max_length=10, default='Past Week')
    graph_animate = models.BooleanField(default=True)
    graph_include_points = models.BooleanField(default=False)
    graph_show_avg = models.BooleanField(default=True)
    graph_show_min = models.BooleanField(default=False)
    graph_show_max = models.BooleanField(default=False)
