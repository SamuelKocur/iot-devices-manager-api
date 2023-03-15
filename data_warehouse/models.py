from django.db import models
from django.utils import timezone


class DateInfo(models.Model):
    date = models.DateTimeField(unique=True)
    hour = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    quarter = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    is_leap_year = models.BooleanField(blank=True, default=False)
    is_week_day = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name_plural = 'Date info'

    def save(self, *args, **kwargs):
        date = self.date
        self.hour = date.hour
        self.day = date.day
        self.week = date.isocalendar()[1]
        self.month = date.month
        self.quarter = (date.month - 1) // 3 + 1
        self.year = date.year
        self.is_leap_year = date.year % 4 == 0 and (date.year % 100 != 0 or date.year % 400 == 0)
        self.is_week_day = date.weekday() < 5
        super(DateInfo, self).save(*args, **kwargs)

    def __str__(self):
        return str(timezone.localtime(self.date))


class FactSensorData(models.Model):
    class Tag(models.TextChoices):
        HOUR = 'hour'
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'

    sensor = models.ForeignKey('iot.Sensor', on_delete=models.CASCADE, related_name='fact_data')
    date = models.ForeignKey('DateInfo', on_delete=models.CASCADE, related_name='fact_data')

    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    avg_value = models.FloatField(blank=True, null=True)
    total_value = models.FloatField(blank=True, null=True)

    tag = models.CharField(max_length=10, choices=Tag.choices, default=Tag.HOUR)

    class Meta:
        verbose_name_plural = 'Sensor data (warehouse)'
