# Generated by Django 3.2.3 on 2021-05-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210529_0258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stationlocation',
            old_name='location_name',
            new_name='city_name',
        ),
        migrations.AddField(
            model_name='stationlocation',
            name='street_name',
            field=models.CharField(blank=True, default='zielona 8', max_length=30),
        ),
    ]