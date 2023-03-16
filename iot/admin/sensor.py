from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from iot_devices_manager.utils.admin_actions import ExportCsvMixin
from iot.models.iot_device import Sensor, SensorData


class SensorDataInlineAdmin(admin.TabularInline):
    model = SensorData
    ordering = ('-timestamp',)
    readonly_fields = ('sensor', 'data', 'timestamp')
    list_filter = (('timestamp', DateRangeFilter),)
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Sensor)
class SensorAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = Sensor
    # inlines = (SensorDataInlineAdmin,)
    list_display = ('id', 'device', 'order', 'name', 'type', 'unit', 'date_created')
    list_filter = (('date_created', DateRangeFilter), 'type', 'unit')
    search_fields = ('id', 'name',)
    readonly_fields = ('date_created', 'date_updated')
    ordering = ('-date_created',)
    actions = ('export_as_csv',)


@admin.register(SensorData)
class SensorDataAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = SensorData
    ordering = ('-timestamp',)
    list_display = ('id', 'sensor', 'data', 'timestamp')
    list_filter = (('timestamp', DateRangeFilter), 'sensor')
    search_fields = ('sensor',)
    readonly_fields = ('id', 'sensor', 'data', 'timestamp')
    actions = ('export_as_csv',)

    def has_add_permission(self, request, obj=None):
        return False

