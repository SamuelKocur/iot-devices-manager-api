from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from data_warehouse.cron import add_data_to_warehouse
from iot_devices_manager.utils.serializers import EmptySerializer


class FilterDataListView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        add_data_to_warehouse()
        return Response()
