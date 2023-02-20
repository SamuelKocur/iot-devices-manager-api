from rest_framework.generics import GenericAPIView

from iot_devices_manager.utils.serializers import EmptySerializer


class FilterDataListView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        pass
