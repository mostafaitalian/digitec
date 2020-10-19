# Generated by Django 2.2.15 on 2020-10-13 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0017_auto_20201009_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_week_dayoff',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'), (7, 'NoDayoff')], default=7),
        ),
        migrations.AlterField(
            model_name='customer',
            name='second_week_dayoff',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'), (7, 'NoDayoff')], default=7),
        ),
    ]