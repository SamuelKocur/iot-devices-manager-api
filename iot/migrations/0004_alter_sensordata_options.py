# Generated by Django 3.2 on 2023-02-19 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0003_location_add_image_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensordata',
            options={'verbose_name_plural': 'Sensor data'},
        ),
    ]
