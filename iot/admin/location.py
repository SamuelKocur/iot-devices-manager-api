from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from iot_devices_manager.utils.admin_actions import ExportCsvMixin
from iot.models import Device, Location


class DeviceInLineAdmin(admin.TabularInline):
    model = Device
    extra = 0
    max_num = 10


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = Location
    inlines = (DeviceInLineAdmin,)
    list_display = ('id', 'building', 'floor', 'room', 'name')
    list_filter = ('building', 'floor', 'room')
    readonly_fields = ('date_created', 'date_updated')
    fieldsets = (
        (None, {
            'fields': ('building', 'floor', 'room', 'date_created', 'date_updated')
        }),
        ('Mobile app', {
            'fields': ('name', 'image')
        }),
    )
    actions = ('export_as_csv',)
