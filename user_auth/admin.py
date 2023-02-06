from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from rangefilter.filters import DateRangeFilter

from .models import FavoriteSensor, UserGroup, User, UserSensorGroup
from django.utils.safestring import mark_safe


class UserGroupAdmin(admin.ModelAdmin):
    model = UserGroup


class UserSensorGroupInLineAdmin(admin.TabularInline):
    model = UserSensorGroup
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (UserSensorGroupInLineAdmin, )
    ordering = ('id', 'email',)
    list_display = ('id', 'email', 'verified', 'current_sensor_groups', 'is_staff', 'is_superuser', 'date_created')
    list_filter = ('groups', 'verified', 'is_staff', 'is_superuser', ('date_created', DateRangeFilter),)
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


class FavoriteSensorAdmin(admin.ModelAdmin):
    model = FavoriteSensor
    list_display = ('id', 'user', 'sensor')
    search_fields = ('user',)
    readonly_fields = ('date_created',)


admin.site.unregister(Group)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(FavoriteSensor, FavoriteSensorAdmin)
