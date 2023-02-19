from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from iot.models import Location, Sensor
from iot.serializers.sensor import LocationSensorSerializer
from iot.serializers.location import LocationSerializer
from iot.utils.permission_checks import get_available_location_ids, get_available_sensor_ids


class LocationListView(GenericAPIView):
    serializer_class = LocationSerializer

    def get(self, request):
        """Retrieve all locations"""
        # available_locations = get_available_location_ids(request.user)
        locations = Location.objects.all()
        serializer = self.serializer_class(locations, many=True, context={'user_id': request.user.id})
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
        serializer = self.serializer_class(data, context={'user_id': request.user.id})
        return Response(serializer.data)
