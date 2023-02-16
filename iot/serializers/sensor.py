from rest_framework import serializers

from iot.models import Device, Sensor, Location
from iot_devices_manager.utils.serializers import ModelListSerializer
from user_auth.models import FavoriteSensor

from iot.serializers.location import LocationSerializer


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = LocationSerializer(many=False)
    status = serializers.CharField(required=False)
    date_updated = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)

    class Meta:
        model = Device
        fields = '__all__'


class SensorDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    order = serializers.CharField()
    name = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    date_updated = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)
    is_favorite = serializers.SerializerMethodField()
    device = DeviceSerializer()

    class Meta:
        list_serializer_class = ModelListSerializer
        model = Sensor
        fields = (
            'id',
            'order',
            'name',
            'type',
            'unit',
            'date_created',
            'date_updated',
            'is_favorite',
            'device',
        )

    def get_is_favorite(self, obj):
        user_id = self.context.get("user_id")
        if user_id:
            try:
                FavoriteSensor.objects.get(user_id=user_id, sensor_id=obj.id)
            except FavoriteSensor.DoesNotExist:
                return False

            return True
        return False

    def create(self, validated_data, **kwargs):
        return Sensor.objects.create(device=kwargs.get('device'), **validated_data)
