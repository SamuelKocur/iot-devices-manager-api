from django.db import models


class DateInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
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
        date_info = DateInfo.get_date_info(self.date)
        super(DateInfo, date_info).save(*args, **kwargs)

    @staticmethod
    def get_date_info(date):
        return DateInfo(
            id=date,
            date=date,
            hour=date.hour,
            day=date.day,
            week=date.isocalendar()[1],
            month=date.month,
            quarter=(date.month - 1) // 3 + 1,
            year=date.year,
            is_leap_year=date.year % 4 == 0 and (date.year % 100 != 0 or date.year % 400 == 0),
            is_week_day=date.weekday() < 5
        )

    def __str__(self):
        return str(self.date)


class FactSensorData(models.Model):
    sensor = models.ForeignKey('iot.Sensor', on_delete=models.CASCADE, related_name='fact_data')
    date = models.ForeignKey('DateInfo', on_delete=models.CASCADE, related_name='fact_data')
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    avg_value = models.FloatField(blank=True, null=True)
    total_value = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Sensor data (warehouse)'
