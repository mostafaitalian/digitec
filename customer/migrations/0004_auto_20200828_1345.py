# Generated by Django 2.2.15 on 2020-08-28 11:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20200824_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='begin_at',
            field=models.TimeField(default=datetime.datetime(2020, 8, 28, 13, 44, 49, 104643)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='finish_at',
            field=models.TimeField(default=datetime.datetime(2020, 8, 28, 21, 44, 49, 104643)),
        ),
    ]