from rest_framework import serializers

from iot.models.iot_device import Sensor
from iot.models.user_customization import UserLocationName
from iot.utils.permission_checks import get_available_sensor_ids


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    building = serializers.CharField()
    floor = serializers.CharField()
    room = serializers.CharField()
    name = serializers.SerializerMethodField()
    custom_name = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    number_of_devices = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.name:
            return obj.name

        return obj.building + obj.floor + obj.room

    def get_custom_name(self, obj):
        user = self.context.get("user")
        custom_names = UserLocationName.objects.filter(user=user, location_id=obj.id)
        if len(custom_names) == 0:
            return self.get_name(obj)

        return custom_names.first().name

    def get_number_of_devices(self, obj):
        user = self.context.get("user")
        print(user)
        available_sensors = get_available_sensor_ids(user)
        sensors = Sensor.objects.filter(id__in=available_sensors, device__location_id=obj.id)
        return sensors.count()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
