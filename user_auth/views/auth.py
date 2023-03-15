from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from knox.auth import AuthToken

from iot_devices_manager.utils.serializers import EmptySerializer
from user_auth.serializers.auth_token import AuthTokenSerializer
from user_auth.serializers.register import RegisterSerializer


class LoginApiView(GenericAPIView):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Login user by email and password
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        instance, token = AuthToken.objects.create(user)
        expiry_date = instance.expiry

        return Response(
            {
                'user_info': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'token': token,
                'expiry_date': expiry_date,
            }
        )


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register user by email, password, first name and last name
        For passwords are required fields: password1, password2
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        instance, token = AuthToken.objects.create(user)
        expiry_date = instance.expiry

        return Response(
            {
                'user_info': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'token': token,
                'expiry_date': expiry_date,
            }
        )


class DeleteUserApiView(GenericAPIView):
    serializer_class = EmptySerializer

    def delete(self, request):
        """
        Soft delete user account
        """
        user = request.user
        user.is_active = False
        user.save()

        return Response(
            {
                'status': 'success',
                'message': 'Profile deleted successfully',
            }
        )


class CheckTokenView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        """
        Check if token is valid
        """
        return Response({'valid': True})
