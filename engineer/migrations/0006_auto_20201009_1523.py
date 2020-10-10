# Generated by Django 2.2.15 on 2020-10-09 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineer', '0005_engineer_no_of_calls_dispatched'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineer',
            name='begin_at',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AddField(
            model_name='engineer',
            name='finish_at',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='engineer',
            name='first_week_dayoff',
            field=models.IntegerField(choices=[(0, 'Saturday'), (1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'NoDayoff')], default=0),
        ),
        migrations.AddField(
            model_name='engineer',
            name='second_week_dayoff',
            field=models.IntegerField(choices=[(0, 'Saturday'), (1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'NoDayoff')], default=6),
        ),
    ]
