from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from iot.models import Location, SensorGroup
from iot.serializers.location import LocationSerializer


class LocationListView(GenericAPIView):
    serializer_class = LocationSerializer

    def get(self, request):
        """Retrieve all locations"""
        available_locations = SensorGroup.objects.filter(users=request.user).values_list('available_sensors__device__location_id')
        locations = Location.objects.filter(id__in=available_locations)
        serializer = self.serializer_class(locations, many=True)
        sensors = {"locations": serializer.data}
        return Response(sensors)
