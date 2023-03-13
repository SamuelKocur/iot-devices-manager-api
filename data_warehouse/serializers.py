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
    date = serializers.SerializerMethodField()
    avg_value = serializers.DecimalField(required=False, max_digits=7, decimal_places=2)
    min_value = serializers.DecimalField(required=False, max_digits=7, decimal_places=2)
    max_value = serializers.DecimalField(required=False, max_digits=7, decimal_places=2)
    total_value = serializers.DecimalField(required=False, max_digits=28, decimal_places=2)

    class Meta:
        model = FactSensorData
        fields = (
            'sensor_id',
            'date',
            'avg_value',
            'min_value',
            'max_value',
            'total_value',
        )

    def get_date(self, obj):
        return obj.date.date
