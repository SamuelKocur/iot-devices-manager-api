import pytz
from django.utils.dateparse import parse_datetime

from data_warehouse.constants import MIN_NUMBER_OF_DATA
from data_warehouse.models import FactSensorData
from iot_devices_manager.settings import TIME_ZONE


def filter_data(request):
    sensor_id = request['sensor_id']
    date_from = parse_datetime(request['date_from'])
    date_to = parse_datetime(request['date_to'])
    # timezone = pytz.timezone(TIME_ZONE)
    # date_from = timezone.localize(date_from)
    # date_to = timezone.localize(date_to)
    tag = get_filtering_tag(date_from, date_to)
    filtered_data = FactSensorData.objects.filter(
        sensor_id=sensor_id,
        date__date__gte=date_from,
        date__date__lte=date_to,
        tag=tag,
    )
    return filtered_data


def get_filtering_tag(date_from, date_to):
    time_diff = date_to - date_from

    # Convert the time difference to hours, days, weeks, and months
    hours = int(time_diff.total_seconds() / 3600)
    days = time_diff.days
    weeks = int(days / 7)
    months = (date_to.year - date_from.year) * 12 + date_to.month - date_from.month

    if months >= MIN_NUMBER_OF_DATA:
        return FactSensorData.Tag.MONTH
    elif weeks >= MIN_NUMBER_OF_DATA:
        return FactSensorData.Tag.WEEK
    elif days >= MIN_NUMBER_OF_DATA:
        return FactSensorData.Tag.DAY
    else:
        return FactSensorData.Tag.HOUR
