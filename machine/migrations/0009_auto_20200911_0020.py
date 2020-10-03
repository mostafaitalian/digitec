# Generated by Django 2.2.15 on 2020-09-10 22:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0008_auto_20200828_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='assigned_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 11, 0, 20, 26, 632029)),
        ),
        migrations.AlterField(
            model_name='call',
            name='completed_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 11, 6, 20, 26, 632029), help_text='the default value is 6 hours + assign_date'),
        ),
        migrations.AlterField(
            model_name='call',
            name='response_time_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 11, 0, 20, 26, 632029), null=True),
        ),
    ]
