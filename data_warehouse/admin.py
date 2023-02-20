from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from data_warehouse.models import DateInfo, FactSensorData
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
    ordering = ('-date',)
    list_display = ('id', 'sensor', 'date', 'avg_value', 'min_value', 'max_value')
    list_filter = (('date', DateRangeFilter), 'sensor')
    search_fields = ('sensor',)
    actions = ('export_as_csv',)

