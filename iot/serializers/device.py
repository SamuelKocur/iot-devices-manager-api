from abc import ABC

from rest_framework import serializers

from iot.models import Device, Sensor, Location


class ModelListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data, **kwargs):
        model_mapping = {model.id: model for model in instance}

        invalid_id = -1
        data_mapping = {}
        for item in validated_data:
            if item.get('id'):
                data_mapping[item.get('id')] = item
            else:
                data_mapping[invalid_id] = item
                invalid_id -= 1

        # Perform creations and updates.
        ret = []
        for model_id, data in data_mapping.items():
            model = model_mapping.get(model_id, None)
            if model is None:
                ret.append(self.child.create(data, **kwargs))
            else:
                ret.append(self.child.update(model, data))

        # Perform deletions.
        for model_id, model in model_mapping.items():
            if model_id not in data_mapping:
                model.delete()

        return ret


class SensorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    order = serializers.CharField()
    name = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    date_updated = serializers.DateTimeField(required=False)
    date_created = serializers.DateTimeField(required=False)
    # is_favorite = serializers.SerializerMethodField()

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

    def get_is_favorite(self, obj):
        pass

    def create(self, validated_data, **kwargs):
        return Sensor.objects.create(device=kwargs.get('device'), **validated_data)


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    building = serializers.CharField()
    floor = serializers.IntegerField()
    room = serializers.CharField()


class DeviceSerializer(serializers.ModelSerializer):
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
