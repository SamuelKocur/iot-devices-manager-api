from django.urls import path

from data_warehouse.views import FilterDataListView

urlpatterns = [
    path('filter/', FilterDataListView.as_view(), name="filtered_sensor_data"),
]
