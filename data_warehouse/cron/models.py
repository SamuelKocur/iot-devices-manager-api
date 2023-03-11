from django.db import models
from django.utils import timezone


class CronJobLastRun(models.Model):
    last_run = models.DateTimeField(default=timezone.now)
