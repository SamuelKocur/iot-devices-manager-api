# Generated by Django 3.2 on 2023-03-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0006_favoritesensor_userlocationname_usersensorname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('pending', 'Pending'), ('approved', 'Approved')], default='pending', max_length=10),
        ),
    ]
