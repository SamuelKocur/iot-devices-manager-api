from rest_framework import serializers

from ..models import Sensor
from ..utils.permission_checks import get_available_sensor_ids


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    building = serializers.CharField()
    floor = serializers.CharField()
    room = serializers.CharField()
    name = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    device_count = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.name:
            return obj.name

        return obj.building + obj.floor + obj.room

    def get_device_count(self, obj):
        user = self.context.get("user")
        available_sensors = get_available_sensor_ids(user)
        sensors = Sensor.objects.filter(id__in=available_sensors, device__location_id=obj.id)
        return sensors.count()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
