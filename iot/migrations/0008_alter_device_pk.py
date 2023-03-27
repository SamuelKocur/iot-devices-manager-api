# Generated by Django 3.2 on 2023-03-27 10:08

from django.db import migrations, models


def set_new_primary_key(apps, schema_editor):
    model = apps.get_model('iot', 'Device')
    i = 1
    for obj in model.objects.all():
        obj.id = i
        obj.save()
        i += 1


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0007_alter_device_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='mac',
            field=models.CharField(max_length=17, unique=True),
        ),
        migrations.RunPython(set_new_primary_key),
    ]
