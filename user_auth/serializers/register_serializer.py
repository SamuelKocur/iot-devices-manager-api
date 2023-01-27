from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=True,
        validators=[
            validators.UniqueValidator(queryset=User.objects.all(), message='A user with given email already exists', )]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        # extra_kwargs = {
        #     'first_name': {'required': False},
        #     'last_name': {'required': False}
        # }

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
        )
        user.set_password(validated_data.get('password'))
        user.save()

        return user
