# Generated by Django 2.2.17 on 2020-11-04 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0022_auto_20201104_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
