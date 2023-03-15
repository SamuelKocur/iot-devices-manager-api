from rest_framework import serializers

from user_auth.models import User


class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_first_name(self, value):
        if value is not None and len(value) < 2:
            raise serializers.ValidationError({"first_name": "First name must have at least 2 characters."})
        return value

    def validate_last_name(self, value):
        if value is not None and len(value) < 2:
            raise serializers.ValidationError({"last_name": "Last name must have at least 2 characters."})
        return value

    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        if first_name is not None:
            instance.first_name = first_name
        if last_name is not None:
            instance.last_name = last_name

        instance.save()
        return instance
