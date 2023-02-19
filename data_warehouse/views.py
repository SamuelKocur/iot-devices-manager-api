from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from data_warehouse.cron import add_data_to_warehouse


class FilterDataListView(GenericAPIView):
    def get(self, request):
        add_data_to_warehouse()
        return Response()


