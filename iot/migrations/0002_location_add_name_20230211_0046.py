# Generated by Django 3.2 on 2023-02-11 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddIndex(
            model_name='sensordata',
            index=models.Index(fields=['timestamp', 'sensor_id'], name='iot_sensord_timesta_356fb0_idx'),
        ),
    ]
