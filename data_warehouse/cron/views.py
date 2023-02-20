from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from data_warehouse.cron.recalculations import recalculate_collected_data_daily
from iot_devices_manager.utils.permissions import LocalhostOnlyPermission
from iot_devices_manager.utils.serializers import EmptySerializer


class DailyRecalculationView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [LocalhostOnlyPermission]

    def get(self, request):
        """
        Used with cron to recalculated collected data
        """
        recalculate_collected_data_daily()
        return Response(status=status.HTTP_200_OK)
