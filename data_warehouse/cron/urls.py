from django.urls import path

import data_warehouse.cron.views as views

urlpatterns = [
    path('recalculate-collected-data/', views.DailyRecalculationView.as_view(), name="cron_process_data"),
]
