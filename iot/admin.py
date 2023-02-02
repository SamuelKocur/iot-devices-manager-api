from django.contrib import admin
from iot.models import Device, Sensor, SensorGroup, SensorData, Location

from user_auth.models import User


class DeviceInLineAdmin(admin.TabularInline):
    model = Device
    extra = 0


class SensorInlineAdmin(admin.TabularInline):
    model = Sensor
    extra = 0


class SensorDataInlineAdmin(admin.TabularInline):
    model = SensorData
    extra = 1
    readonly_fields = ('sensor', 'data', 'timestamp')


class DeviceAdmin(admin.ModelAdmin):
    model = Device
    inlines = (SensorInlineAdmin, )
    list_display = ('id', 'mac', 'name', 'status', 'location', 'date_updated')
    list_filter = ('location', 'status')
    search_fields = ('mac', 'name', 'location',)
    readonly_fields = ('date_created', 'date_updated')


class SensorAdmin(admin.ModelAdmin):
    model = Sensor
    inlines = (SensorDataInlineAdmin,)
    list_display = ('id', 'device', 'name', 'type')
    list_filter = ('id', 'device', 'type', 'unit')
    search_fields = ('name',)
    readonly_fields = ('date_created', 'date_updated')


class SensorDataAdmin(admin.ModelAdmin):
    model = SensorData
    list_display = ('id', 'sensor', 'data', 'timestamp')
    list_filter = ('id', 'sensor')
    readonly_fields = ('id', 'sensor', 'data', 'timestamp')

    def has_add_permission(self, request, obj=None):
        return False


class UserInlineAdmin(admin.TabularInline):
    model = User.sensor_groups.through
    extra = 1


class SensorGroupAdmin(admin.ModelAdmin):
    model = SensorGroup
    inlines = (UserInlineAdmin,)
    list_display = ('id', 'group_name', 'sensors', 'assigned_users')
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

    def sensors(self, obj):
        # return ", ".join([str(sensor.id) for sensor in obj.available_sensors.all()])  # displays all sensor IDs
        return len(obj.available_sensors.all())

    def assigned_users(self, obj):
        # return ", ".join([str(user.email) for user in obj.users.all()]) # displays all emails
        return len(obj.users.all())

    def users(self, obj):
        return obj.users.all()


class LocationAdmin(admin.ModelAdmin):
    model = Location
    inlines = (DeviceInLineAdmin,)
    list_display = ('id', 'building', 'floor', 'room')
    list_filter = ('building', 'floor', 'room')
    readonly_fields = ('date_created', 'date_updated')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorGroup, SensorGroupAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(SensorData, SensorDataAdmin)
