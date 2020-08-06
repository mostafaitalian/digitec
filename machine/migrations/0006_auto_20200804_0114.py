# Generated by Django 2.0.13 on 2020-08-03 23:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0005_auto_20200803_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 4, 7, 14, 16, 418953), help_text='the default value is 6 hours + assign_date'),
        ),
        migrations.AlterField(
            model_name='call',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='machine.Machine'),
        ),
    ]
