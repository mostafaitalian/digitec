# Generated by Django 2.2.17 on 2020-11-05 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0024_auto_20201104_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='customerbranch',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
