# Generated by Django 2.2.15 on 2020-08-28 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20200828_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='begin_at',
            field=models.TimeField(default=datetime.datetime(2020, 8, 28, 16, 26, 32, 627211)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='finish_at',
            field=models.TimeField(default=datetime.datetime(2020, 8, 29, 0, 26, 32, 627211)),
        ),
    ]
