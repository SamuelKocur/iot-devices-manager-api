from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from django.utils.safestring import mark_safe
from rangefilter.filters import DateRangeFilter

from .models import UserGroup, User, UserSensorGroup, UserAppSettings


admin.site.unregister(Group)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    model = UserGroup


class UserSensorGroupInLineAdmin(admin.TabularInline):
    model = UserSensorGroup
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (UserSensorGroupInLineAdmin, )
    ordering = ('-date_created',)
    list_display = (
        'id',
        'email',
        'verified',
        'current_sensor_groups',
        'is_staff',
        'is_superuser',
        'date_created',
    )
    list_filter = (
        'groups',
        'verified',
        'is_staff',
        'is_superuser',
        ('date_created', DateRangeFilter),
    )
    search_fields = ('email',)
    readonly_fields = ('date_created', 'date_updated')
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': (
                'verified', 'is_active', 'is_staff', 'is_superuser',
            )
        }),
        ('Important dates', {
            'fields': ('date_created', 'date_updated',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': (
                'verified', 'is_active', 'is_staff', 'is_superuser',
            )
        }),
    )

    def current_sensor_groups(self, obj):
        # return mark_safe("""<b title="aaa">a</b>, <b title="aaa">a</b>, <b title="aaa">a</b>, """)
        return mark_safe(",  ".join([f'<span title="{group.group_name}">{group.id}</span>' for group in obj.sensor_groups.all()]))


@admin.register(UserAppSettings)
class UserAppSettingsAdmin(admin.ModelAdmin):
    model = UserAppSettings
    list_display = (
        'user',
        'date_format',
        'get_data_for',
        'graph_animate',
        'graph_include_points',
        'graph_show_avg',
        'graph_show_min',
        'graph_show_max',
    )
    list_filter = (
        'date_format',
        'get_data_for',
        'graph_animate',
        'graph_include_points',
        'graph_show_avg',
        'graph_show_min',
        'graph_show_max',
    )
    readonly_fields = (
        'date_format',
        'get_data_for',
        'graph_animate',
        'graph_include_points',
        'graph_show_avg',
        'graph_show_min',
        'graph_show_max',
    )

    def has_add_permission(self, request, obj=None):
        return False
