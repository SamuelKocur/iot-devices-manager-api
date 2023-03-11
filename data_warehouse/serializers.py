from rest_framework import serializers

from data_warehouse.models import FactSensorData


class FilterDataRequestSerializer(serializers.Serializer):
    sensor_id = serializers.IntegerField()
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class FilterDataResponseSerializer(serializers.ModelSerializer):
    sensor_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    avg_value = serializers.FloatField(required=False)
    min_value = serializers.FloatField(required=False)
    max_value = serializers.FloatField(required=False)
    total_value = serializers.FloatField(required=False)

    class Meta:
        model = FactSensorData
        fields = '__all__'
