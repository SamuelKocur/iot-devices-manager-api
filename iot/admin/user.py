from django.contrib import admin

from iot.models.user_customization import FavoriteSensor, UserLocationName, UserSensorName


@admin.register(FavoriteSensor)
class FavoriteSensorAdmin(admin.ModelAdmin):
    model = FavoriteSensor
    list_display = ('id', 'user', 'sensor')
    search_fields = ('user',)
    readonly_fields = ('date_created',)


@admin.register(UserLocationName)
class UserLocationNameAdmin(admin.ModelAdmin):
    model = UserLocationName
    list_display = ('id', 'user', 'location', 'name')
    search_fields = ('user',)
    readonly_fields = ('date_created',)


@admin.register(UserSensorName)
class UserSensorNameAdmin(admin.ModelAdmin):
    model = UserSensorName
    list_display = ('id', 'user', 'sensor', 'name')
    search_fields = ('user',)
    readonly_fields = ('date_created',)


