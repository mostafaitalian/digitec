# Generated by Django 2.0.13 on 2020-08-03 23:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0008_auto_20200804_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 4, 7, 26, 19, 701689), help_text='the default value is 6 hours + assign_date'),
        ),
    ]