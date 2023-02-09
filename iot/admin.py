from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter

from iot_devices_manager.utils.admin_actions import ExportCsvMixin
from iot.models import Device, Sensor, SensorGroup, SensorData, Location
from user_auth.models import User


class DeviceInLineAdmin(admin.TabularInline):
    model = Device
    extra = 0
    max_num = 10


class SensorInlineAdmin(admin.TabularInline):
    model = Sensor
    extra = 0
    max_num = 10


class SensorDataInlineAdmin(admin.TabularInline):
    model = SensorData
    ordering = ('-timestamp',)
    readonly_fields = ('sensor', 'data', 'timestamp')
    list_filter = (('timestamp', DateRangeFilter),)
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = Device
    ordering = ('-date_created',)
    inlines = (SensorInlineAdmin, )
    list_display = ('mac', 'name', 'status', 'location', 'date_created')
    list_filter = (('date_created', DateRangeFilter), 'status', 'location')
    search_fields = ('mac', 'name', 'location',)
    readonly_fields = ('date_created', 'date_updated')
    actions = ('export_as_csv',)


@admin.register(Sensor)
class SensorAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = Sensor
    inlines = (SensorDataInlineAdmin,)
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


class UserInlineAdmin(admin.TabularInline):
    model = User.sensor_groups.through
    extra = 1
    max_num = 10


@admin.register(SensorGroup)
class SensorGroupAdmin(admin.ModelAdmin):
    model = SensorGroup
    inlines = (UserInlineAdmin,)
    list_display = ('id', 'group_name', 'sensors', 'assigned_users', 'date_created', 'date_updated')
    list_filter = (('date_created', DateRangeFilter), ('date_updated', DateRangeFilter))
    search_fields = ('group_name',)
    readonly_fields = ('date_created', 'date_updated')
    fieldsets = (
        (None, {
            'fields': ('group_name', 'available_sensors')
        }),
        ('Important dates', {
            'fields': ('date_created', 'date_updated')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('group_name', 'available_sensors')
        }),
    )
    actions = ('export_as_csv',)

    def sensors(self, obj):
        # return ", ".join([str(sensor.id) for sensor in obj.available_sensors.all()])  # displays all sensor IDs
        return len(obj.available_sensors.all())

    def assigned_users(self, obj):
        # return ", ".join([str(user.email) for user in obj.users.all()]) # displays all emails
        return len(obj.users.all())

    def users(self, obj):
        return obj.users.all()


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, admin.ModelAdmin, ExportCsvMixin):
    model = Location
    inlines = (DeviceInLineAdmin,)
    list_display = ('id', 'building', 'floor', 'room')
    list_filter = ('building', 'floor', 'room')
    readonly_fields = ('date_created', 'date_updated')
    actions = ('export_as_csv',)
