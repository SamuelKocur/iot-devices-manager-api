from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user_auth.serializers.change_password import ChangePasswordSerializer
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

    def post(self, request):
        """
        Applies updates to user's profile
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
