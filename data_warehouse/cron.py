from datetime import timedelta
from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import TruncHour
from django.utils import timezone

from iot.models import SensorData
from data_warehouse.models import DateInfo, FactSensorData


def add_data_to_warehouse():
    now = timezone.now()
    start_of_previous_day = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_previous_day = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)

    # with transaction.atomic():  # ensure that all the database queries are executed in a single transaction, which can help to improve performance and reduce the number of times the database is accessed.
    last_day_data = SensorData.objects \
        .filter(timestamp__gte=start_of_previous_day, timestamp__lte=end_of_previous_day) \
        .annotate(hour=TruncHour('timestamp')) \
        .values('sensor', 'hour') \
        .annotate(
            avg_value=Avg('data'),
            max_value=Max('data'),
            min_value=Min('data'),
            total_value=Sum('data'),
        )

    # Create list of date_info objects and insert them to DB using bulk_create()
    list_date_info = [
        DateInfo.get_date_info(row['hour']) for row in last_day_data
    ]
    DateInfo.objects.bulk_create(list_date_info, ignore_conflicts=True)

    # Create list of fact_sensor_data objects and insert them to DB using bulk_create()
    list_fact_sensor_data = [
        FactSensorData(
            sensor_id=row['sensor'],
            date_id=row['hour'],
            min_value=row['min_value'],
            max_value=row['max_value'],
            avg_value=row['avg_value'],
            total_value=row['total_value'],
        ) for row in last_day_data
    ]
    FactSensorData.objects.bulk_create(list_fact_sensor_data)
