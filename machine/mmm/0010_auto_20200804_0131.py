# Generated by Django 2.0.13 on 2020-08-03 23:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0009_auto_20200804_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 4, 7, 31, 45, 508609), help_text='the default value is 6 hours + assign_date'),
        ),
    ]