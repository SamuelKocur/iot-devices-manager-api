from rest_framework import serializers
from django.shortcuts import get_object_or_404

from iot.models import Device, Sensor, SensorData


class SensorDataRequestSerializer(serializers.ModelSerializer):
    mac = serializers.CharField(required=False)
    order = serializers.IntegerField(required=False)
    data = serializers.FloatField()

    class Meta:
        model = SensorData
        fields = (
            'mac',
            'order',
            'data',
        )

    def create(self, validated_data):
        mac = validated_data['mac']
        order = validated_data['order']

        if not mac:
            raise serializers.ValidationError({'mac': 'This field is required'})

        if not order:
            raise serializers.ValidationError({'order': 'This field is required'})

        sensor = get_object_or_404(
            Sensor,
            device__mac__exact=mac,
            order=order,
        )

        if not sensor:
            raise serializers.ValidationError(detail='Sensor does not exists')

        if sensor.device.status != Device.Status.APPROVED:
            raise serializers.ValidationError(detail='Device status is not Approved, data can not be saved')

        sensor_data = SensorData.objects.create(sensor=sensor, data=validated_data['data'])
        return sensor_data

    def update(self, instance, validated_data):
        pass
