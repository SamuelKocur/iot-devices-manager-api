from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from data_warehouse.models import DateInfo, FactSensorData
from data_warehouse.cron.models import CronJobLastRun
from iot_devices_manager.utils.admin_actions import ExportCsvMixin


class FactSensorDataInlineAdmin(admin.TabularInline):
    model = FactSensorData
    ordering = ('-date',)
    readonly_fields = (
        'sensor',
        'date',
        'min_value',
        'max_value',
        'avg_value',
        'total_value',
    )
    list_filter = (('timestamp', DateRangeFilter),)
    extra = 1


@admin.register(DateInfo)
class DateInfoAdmin(admin.ModelAdmin):
    model = DateInfo
    inlines = (FactSensorDataInlineAdmin,)
    list_display = ('date', 'hour', 'day', 'month', 'year')
    list_filter = (('date', DateRangeFilter),)
    search_fields = ('date',)
    readonly_fields = (
        'hour',
        'day',
        'week',
        'month',
        'quarter',
        'year',
        'is_leap_year',
        'is_week_day',
    )
    ordering = ('-date',)


@admin.register(FactSensorData)
class FactSensorDataAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = FactSensorData
    ordering = ('-date__date',)
    list_display = ('id', 'sensor', 'date', 'tag', 'avg_value', 'min_value', 'max_value', 'total_value')
    list_filter = (('date', DateRangeFilter), 'tag', 'sensor')
    search_fields = ('sensor',)
    actions = ('export_as_csv',)


@admin.register(CronJobLastRun)
class CronJobLastRunAdmin(admin.ModelAdmin):
    model = CronJobLastRun
    list_display = ('last_run',)
    list_filter = (('last_run', DateRangeFilter),)
    # readonly_fields = ('last_run',)
    ordering = ('-last_run',)
