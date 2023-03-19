from django.utils import timezone
from rest_framework import serializers

from iot.models.iot_device import Device, Sensor, SensorData
from iot.serializers.location import LocationSerializer
from iot_devices_manager.utils.serializers import ModelListSerializer
from iot.models.user_customization import FavoriteSensor


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
    name = serializers.SerializerMethodField()
    custom_name = serializers.SerializerMethodField()
    unit = serializers.CharField(required=False)
    date_updated = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)
    is_favorite = serializers.SerializerMethodField()
    device = DeviceSerializer()
    latest_value = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = ModelListSerializer
        model = Sensor
        fields = (
            'id',
            'order',
            'name',
            'custom_name',
            'type',
            'unit',
            'date_created',
            'date_updated',
            'is_favorite',
            'latest_value',
            'device',
        )

    def get_is_favorite(self, obj):
        user = self.context.get("user")
        if user:
            try:
                FavoriteSensor.objects.get(user=user, sensor_id=obj.id)
            except FavoriteSensor.DoesNotExist:
                return False

            return True
        return False

    def get_name(self, obj):
        if obj.name:
            return obj.name

        return obj.type

    def get_custom_name(self, obj):
        user = self.context.get("user")
        custom_names = obj.user_names.filter(user=user)
        if len(custom_names) == 0:
            return self.get_name(obj)

        return custom_names.first().name

    def get_latest_value(self, obj):
        try:
            sensor_data = SensorData.objects.filter(sensor_id=obj.id).latest('timestamp')
            return {
                'value': sensor_data.data,
                'timestamp': timezone.localtime(sensor_data.timestamp),
            }
        except SensorData.DoesNotExist:
            return


class LocationSensorSerializer(serializers.Serializer):
    location = LocationSerializer()
    sensors = SensorDetailSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
