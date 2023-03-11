import logging

from datetime import timedelta

from django.db import transaction
from django.db.models import Avg, Max, Min, Sum
from rest_framework import status

from iot.models import SensorData
from data_warehouse.models import DateInfo, FactSensorData

logger = logging.getLogger(__name__)


# Recalculates collected data from all sensors on hourly basis
def recalculate_collected_data_hourly(datetime):
    start_of_previous_hour = datetime.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    start_of_next_hour = start_of_previous_hour + timedelta(hours=1)
    end_of_previous_hour = start_of_next_hour - timedelta(seconds=1)

    if FactSensorData.objects.filter(
        date__date__gte=start_of_previous_hour,
        date__date__lte=end_of_previous_hour,
        tag=FactSensorData.Tag.HOUR,
    ):
        logger.warning('Data for ' + str(start_of_previous_hour) + ' - ' + str(end_of_previous_hour) + ' hour are already saved')
        return status.HTTP_400_BAD_REQUEST

    with transaction.atomic():
        logger.info('Getting all the data for last hour')
        last_hour_data = SensorData.objects.filter(
            timestamp__gte=start_of_previous_hour,
            timestamp__lte=end_of_previous_hour,
        ).values(
            'sensor'
        ).annotate(
            avg_value=Avg('data'),
            max_value=Max('data'),
            min_value=Min('data'),
            total_value=Sum('data'),
        )

        logger.info('Creating date info model instance')
        date_info = DateInfo.objects.create(date=start_of_previous_hour)

        logger.info('Creating fact sensor data model instances')
        create_fact_sensor_data(
            data=last_hour_data,
            date_info=date_info,
            tag=FactSensorData.Tag.HOUR,
        )

        return recalculate_daily_data(datetime)


def recalculate_daily_data(datetime):
    last_day_hourly_data = FactSensorData.objects.filter(
        tag=FactSensorData.Tag.HOUR,
        date__day=datetime.day,
        date__month=datetime.month,
        date__year=datetime.year,
    ).values(
        'sensor'
    ).annotate(
        avg_value=Avg('avg_value'),
        max_value=Max('max_value'),
        min_value=Min('min_value'),
        total_value=Sum('total_value'),
    )

    date_info, _ = DateInfo.objects.get_or_create(date=datetime.replace(hour=0, minute=0, second=0, microsecond=0))

    logger.info('Creating fact sensor data model instance for daily data')
    FactSensorData.objects.filter(
        date__day=datetime.day,
        date__month=datetime.month,
        date__year=datetime.year,
        tag=FactSensorData.Tag.DAY,
    ).delete()

    create_fact_sensor_data(
        data=last_day_hourly_data,
        date_info=date_info,
        tag=FactSensorData.Tag.DAY,
    )

    return recalculate_weekly_data(datetime)


def recalculate_weekly_data(datetime):
    last_week_daily_data = FactSensorData.objects.filter(
        tag=FactSensorData.Tag.DAY,
        date__week=datetime.isocalendar()[1],
        date__month=datetime.month,
        date__year=datetime.year,
    ).values(
        'sensor'
    ).annotate(
        avg_value=Avg('avg_value'),
        max_value=Max('max_value'),
        min_value=Min('min_value'),
        total_value=Sum('total_value'),
    )

    start_of_week = datetime.date() - timedelta(days=datetime.date().weekday())
    date_info, _ = DateInfo.objects.get_or_create(date=datetime.replace(day=start_of_week.day, hour=0, minute=0, second=0, microsecond=0))

    logger.info('Creating fact sensor data model instance for weekly data')
    FactSensorData.objects.filter(
        date__week=datetime.isocalendar()[1],
        date__month=datetime.month,
        date__year=datetime.year,
        tag=FactSensorData.Tag.WEEK,
    ).delete()

    create_fact_sensor_data(
        data=last_week_daily_data,
        date_info=date_info,
        tag=FactSensorData.Tag.WEEK,
    )

    return recalculate_monthly_data(datetime)


def recalculate_monthly_data(datetime):
    last_month_daily_data = FactSensorData.objects.filter(
        tag=FactSensorData.Tag.DAY,
        date__month=datetime.month,
        date__year=datetime.year,
    ).values(
        'sensor'
    ).annotate(
        avg_value=Avg('avg_value'),
        max_value=Max('max_value'),
        min_value=Min('min_value'),
        total_value=Sum('total_value'),
    )

    date_info, _ = DateInfo.objects.get_or_create(date=datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0))

    logger.info('Creating fact sensor data model instance for monthly data')
    FactSensorData.objects.filter(
        date__month=datetime.month,
        date__year=datetime.year,
        tag=FactSensorData.Tag.MONTH,
    ).delete()

    create_fact_sensor_data(
        data=last_month_daily_data,
        date_info=date_info,
        tag=FactSensorData.Tag.MONTH,
    )

    return status.HTTP_200_OK


def create_fact_sensor_data(data, date_info, tag):
    list_fact_sensor_data = [
        FactSensorData(
            sensor_id=row['sensor'],
            date_id=date_info.id,
            min_value=row['min_value'],
            max_value=row['max_value'],
            avg_value=row['avg_value'],
            total_value=row['total_value'],
            tag=tag,
        ) for row in data
    ]
    FactSensorData.objects.bulk_create(list_fact_sensor_data)
