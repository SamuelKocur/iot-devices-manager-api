from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from iot_devices_manager.utils.admin_actions import ExportCsvMixin
from iot.models.iot_device import Device, Sensor


class SensorInlineAdmin(admin.TabularInline):
    model = Sensor
    extra = 0
    max_num = 10


@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = Device
    ordering = ('-date_created',)
    inlines = (SensorInlineAdmin, )
    list_display = ('id', 'mac', 'name', 'status', 'location', 'date_created')
    list_filter = (('date_created', DateRangeFilter), 'status', 'location')
    search_fields = ('mac', 'name', 'location',)
    readonly_fields = ('date_created', 'date_updated')
    actions = ('export_as_csv',)
