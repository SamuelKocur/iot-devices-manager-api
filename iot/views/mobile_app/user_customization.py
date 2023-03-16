from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from iot_devices_manager.utils.serializers import EmptySerializer
from iot.models.user_customization import UserLocationName, UserSensorName


class UserSensorNameView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, sensor_id):
        """
        Add user own name to sensor.
        """
        user_id = request.user.id
        name = request.query_params.get("name")

        try:
            user_sensor_name = UserSensorName.objects.get(user_id=user_id, sensor_id=sensor_id)

            if name == "":
                user_sensor_name.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            user_sensor_name.name = name
            user_sensor_name.save()
            return Response(status=status.HTTP_200_OK)
        except UserSensorName.DoesNotExist:
            if name == "":
                return Response(status=status.HTTP_204_NO_CONTENT)

            UserSensorName.objects.create(user_id=user_id, sensor_id=sensor_id, name=name)
            return Response(status=status.HTTP_201_CREATED)


class UserLocationNameView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, location_id):
        """
        Add user own name to location.
        """
        user_id = request.user.id
        name = request.query_params.get("name")

        try:
            user_location_name = UserLocationName.objects.get(user_id=user_id, location_id=location_id)

            if name == "":
                user_location_name.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            user_location_name.name = name
            user_location_name.save()
            return Response(status=status.HTTP_200_OK)
        except UserLocationName.DoesNotExist:
            if name == "":
                return Response(status=status.HTTP_204_NO_CONTENT)

            UserLocationName.objects.create(user_id=user_id, location_id=location_id, name=name)
            return Response(status=status.HTTP_201_CREATED)
