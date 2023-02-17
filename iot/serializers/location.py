from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    building = serializers.CharField()
    floor = serializers.CharField()
    room = serializers.CharField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.name:
            return obj.name

        return obj.building + obj.floor + obj.room

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
