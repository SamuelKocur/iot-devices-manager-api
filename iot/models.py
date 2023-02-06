from django.db import models


class Location(models.Model):
    building = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    room = models.CharField(max_length=20)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('building', 'floor', 'room')

    def __str__(self):
        return f"B-{self.building} F-{self.floor} R-{self.room} [{self.id}]"


class Device(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'

    mac = models.CharField(max_length=17, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, default=None, related_name='devices')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.mac}"


class Sensor(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='sensors')
    order = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20)
    unit = models.CharField(max_length=10, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('device', 'order')

    def __str__(self):
        return f"{self.device} - {self.order} [{self.type}]"


class SensorData(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='data')
    data = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.id}"


class SensorGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    available_sensors = models.ManyToManyField('Sensor', related_name='sensor_groups')

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.group_name} [{self.id}]"
