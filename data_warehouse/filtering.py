from django.utils.dateparse import parse_datetime

from data_warehouse.constants import MIN_NUMBER_OF_DATA
from data_warehouse.models import FactSensorData


def filter_data(request):
    sensor_id = request['sensor_id']
    date_from = parse_datetime(request['date_from'])
    date_to = parse_datetime(request['date_to'])

    tag = get_filtering_tag(date_from, date_to)
    date_format = get_date_format(tag)
    filtered_data = FactSensorData.objects.filter(
        sensor_id=sensor_id,
        date__date__gte=date_from,
        date__date__lte=date_to,
        tag=tag,
    ).order_by('date')

    return filtered_data, date_format


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


def get_date_format(tag):
    if tag == FactSensorData.Tag.HOUR:
        return 'MMM d, HH:mm'
    elif tag == FactSensorData.Tag.MONTH:
        return 'MMM y'

    return 'MMM d'
