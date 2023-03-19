from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from user_auth.models import UserAppSettings
from user_auth.serializers.change_password import ChangePasswordSerializer
from user_auth.serializers.user_app_settings import UserSettingsRequestSerializer
from user_auth.serializers.user_profile_update import UpdateUserProfileSerializer


class ChangePasswordApiView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        """
        Change user's password.
        Required fields: old password, password1, password2
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data.get("new_password"))
        user.save()

        return Response(
            {
                'status': 'success',
                'message': 'Password updated successfully',
            }
        )


class UpdateUserProfileApiView(GenericAPIView):
    serializer_class = UpdateUserProfileSerializer

    def put(self, request):
        """
        Apply updates to user's profile
        """
        instance = request.user
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'status': 'success',
                'message': 'Profile updated successfully',
            }
        )


class UserAppSettingsView(GenericAPIView):
    serializer_class = UserSettingsRequestSerializer

    def get(self, request):
        """
        Get user's app settings
        """
        user_id = request.user
        app_settings = get_object_or_404(UserAppSettings, user_id=user_id)
        serializer = self.serializer_class(app_settings)
        return Response(serializer.data)

    def post(self, request):
        """
        Save app settings for given user.
        """
        user_id = request.user.id
        serializer = UserSettingsRequestSerializer(data=request.data, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data
        )
