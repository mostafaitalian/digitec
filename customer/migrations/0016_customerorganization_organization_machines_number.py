# Generated by Django 2.2.15 on 2020-10-03 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_remove_customerbranch_branche_machines'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorganization',
            name='organization_machines_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
