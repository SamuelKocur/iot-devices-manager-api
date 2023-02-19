from iot.models import SensorGroup


def get_available_sensor_ids(user):
    return SensorGroup.objects.filter(users=user).values_list('available_sensors__id')


def get_available_location_ids(user):
    return SensorGroup.objects.filter(users=user).values_list('available_sensors__device__location_id')