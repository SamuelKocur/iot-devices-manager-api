from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from iot.models.iot_device import Location, Sensor
from iot.serializers.mobile_app.sensor import LocationSensorSerializer
from iot.serializers.mobile_app.location import LocationSerializer
from iot.utils.permission_checks import get_available_location_ids, get_available_sensor_ids


class LocationListView(GenericAPIView):
    serializer_class = LocationSerializer

    def get(self, request):
        """Retrieve all locations"""
        available_locations = get_available_location_ids(request.user)
        locations = Location.objects.filter(id__in=available_locations)
        serializer = self.serializer_class(locations, many=True, context={'user': request.user})
        locations = {"locations": serializer.data}
        return Response(locations)


class LocationDetailView(GenericAPIView):
    serializer_class = LocationSensorSerializer

    def get(self, request, location_id):
        """Retrieve location by id"""
        # available_locations = get_available_location_ids(request.user)
        location = get_object_or_404(Location, pk=location_id)
        available_sensors = get_available_sensor_ids(request.user)
        sensors = Sensor.objects.filter(id__in=available_sensors, device__location=location)
        data = {
            'sensors': sensors,
            'location': location,
        }
        serializer = self.serializer_class(data, context={'user': request.user})
        return Response(serializer.data)
