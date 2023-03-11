from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from data_warehouse.cron.recalculations import recalculate_collected_date
from iot_devices_manager.utils.permissions import LocalhostOnlyPermission
from iot_devices_manager.utils.serializers import EmptySerializer


class HourlyRecalculationView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [LocalhostOnlyPermission]

    def get(self, request):
        """
        Used with cron to recalculated collected data
        """
        status = recalculate_collected_date()
        return Response(status=status)
