# Generated by Django 3.2 on 2023-03-19 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_delete_favoritesensor'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAppSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='app_setting', serialize=False, to='user_auth.user')),
                ('date_format', models.CharField(default='d MMM y H:mm', max_length=30)),
                ('get_data_for', models.CharField(default='Past Week', max_length=10)),
                ('graph_animate', models.BooleanField(default=True)),
                ('graph_include_points', models.BooleanField(default=False)),
                ('graph_show_avg', models.BooleanField(default=True)),
                ('graph_show_min', models.BooleanField(default=False)),
                ('graph_show_max', models.BooleanField(default=False)),
            ],
        ),
    ]
