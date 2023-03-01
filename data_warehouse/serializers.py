from rest_framework import serializers

from data_warehouse.models import FactSensorData
from iot.models import SensorData


class FilterDataRequestSerializer(serializers.ModelSerializer):
    sensor_id = serializers.IntegerField()
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()

    class Meta:
        model = SensorData
        fields = '__all__'


class FilterDataResponseSerializer(serializers.ModelSerializer):
    sensor_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    avg_value = serializers.FloatField(required=False)
    min_value = serializers.FloatField(required=False)
    max_value = serializers.FloatField(required=False)
    total_value = serializers.FloatField(required=False)

    class Meta:
        model = SensorData
        fields = '__all__'
