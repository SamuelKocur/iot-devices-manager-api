from rest_framework import serializers

from user_auth.models import UserAppSettings


class UserSettingsRequestSerializer(serializers.ModelSerializer):
    date_format = serializers.CharField()
    get_data_for = serializers.CharField()
    graph_animate = serializers.BooleanField()
    graph_include_points = serializers.BooleanField()
    graph_show_avg = serializers.BooleanField()
    graph_show_min = serializers.BooleanField()
    graph_show_max = serializers.BooleanField()

    class Meta:
        model = UserAppSettings
        fields = (
            'date_format',
            'get_data_for',
            'graph_animate',
            'graph_include_points',
            'graph_show_avg',
            'graph_show_min',
            'graph_show_max',
        )

    def create(self, validated_data):
        user_id = self.context.get("user_id")

        app_setting, _ = UserAppSettings.objects.get_or_create(
            user_id=user_id,
        )

        print(validated_data)

        app_setting.date_format = validated_data['date_format']
        app_setting.get_data_for = validated_data['get_data_for']
        app_setting.graph_animate = validated_data['graph_animate']
        app_setting.graph_include_points = validated_data['graph_include_points']
        app_setting.graph_show_avg = validated_data['graph_show_avg']
        app_setting.graph_show_min = validated_data['graph_show_min']
        app_setting.graph_show_max = validated_data['graph_show_max']

        app_setting.save()

        return app_setting
