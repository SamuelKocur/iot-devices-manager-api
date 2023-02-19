from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from iot.models import SensorGroup
from user_auth.models import User


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
