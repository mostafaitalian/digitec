# Generated by Django 2.0.13 on 2020-08-03 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0004_auto_20200803_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 3, 20, 2, 52, 443311), help_text='the default value is 6 hours + assign_date'),
        ),
    ]