import rest_framework.serializers as serializers


class PublishApiSerializer(serializers.Serializer):
    topic = serializers.CharField()
    message = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
