# Generated by Django 2.2.15 on 2020-08-23 22:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='assigned_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 24, 0, 36, 47, 973428)),
        ),
        migrations.AlterField(
            model_name='call',
            name='completed_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 24, 6, 36, 47, 973428), help_text='the default value is 6 hours + assign_date'),
        ),
        migrations.AlterField(
            model_name='call',
            name='response_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 24, 0, 36, 47, 973428), null=True),
        ),
    ]