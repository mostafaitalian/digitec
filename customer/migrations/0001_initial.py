# Generated by Django 2.0.13 on 2020-08-21 18:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, help_text='donot fill this it will be filled automatically', unique=True)),
                ('location', models.CharField(max_length=255, verbose_name='Address location')),
                ('address', models.URLField(verbose_name='address site')),
                ('telephone', models.PositiveIntegerField(blank=True, null=True, verbose_name='telephone')),
                ('begin_at', models.TimeField(default=datetime.datetime(2020, 8, 21, 20, 18, 59, 499195))),
                ('finish_at', models.TimeField(default=datetime.datetime(2020, 8, 22, 4, 18, 59, 499195))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(blank=True, choices=[('HR section', 'HR'), ('Service section', 'Service'), ('Finance section', 'Finance'), ('Collection section', 'Collection'), ('Sales section', 'Sales'), ('Production section', 'Production'), ('others', 'others')], max_length=200)),
                ('no_of_machine', models.PositiveIntegerField(default=0, verbose_name='machines number')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='customer.Customer')),
            ],
        ),
    ]