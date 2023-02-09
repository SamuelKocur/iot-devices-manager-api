from rest_framework import serializers

from iot.models import Device, Sensor, Location
from iot_devices_manager.utils.model_list_serializer import ModelListSerializer

from iot.serializers.location import LocationSerializer


class SensorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    order = serializers.CharField()
    name = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    date_updated = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)

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
        )

    def create(self, validated_data, **kwargs):
        return Sensor.objects.create(device=kwargs.get('device'), **validated_data)


class DeviceDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    sensors = SensorSerializer(many=True)
    location = LocationSerializer(many=False)
    status = serializers.CharField(required=False)
    date_updated = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)

    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        sensor_data = validated_data.pop('sensors')
        location_data = validated_data.pop('location')

        location, created = Location.objects.get_or_create(
            **location_data
        )
        device = Device.objects.create(location=location, **validated_data)

        for sensor in sensor_data:
            Sensor.objects.create(device=device, **sensor)

        return device
