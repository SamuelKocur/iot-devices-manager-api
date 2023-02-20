from django.urls import path, include

import data_warehouse.views as view

urlpatterns = [
    path('filter/', view.FilterDataListView.as_view(), name="filtered_sensor_data"),

    path('', include('data_warehouse.cron.urls'))
]
