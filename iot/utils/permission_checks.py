from iot.models.iot_device import SensorGroup, Device, Sensor, Location


def get_available_sensor_ids(user):
    if user.is_staff:
        return Sensor.objects.all().values_list('id', flat=True)

    return SensorGroup.objects.filter(users=user, available_sensors__device__status=Device.Status.APPROVED).values_list('available_sensors__id', flat=True)


def get_available_location_ids(user):
    if user.is_staff:
        return Location.objects.all().values_list('id', flat=True)

    return SensorGroup.objects.filter(users=user, available_sensors__device__status=Device.Status.APPROVED).values_list('available_sensors__device__location_id', flat=True)
