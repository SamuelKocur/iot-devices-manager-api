from iot.models import SensorGroup, Device


def get_available_sensor_ids(user):
    return SensorGroup.objects.filter(users=user, available_sensors__device__status=Device.Status.APPROVED).values_list('available_sensors__id', flat=True)


def get_available_location_ids(user):
    return SensorGroup.objects.filter(users=user, available_sensors__device__status=Device.Status.APPROVED).values_list('available_sensors__device__location_id', flat=True)
