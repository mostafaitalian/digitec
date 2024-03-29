# Generated by Django 2.1 on 2019-03-22 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('engineer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('location', models.CharField(max_length=255, verbose_name='Address location')),
                ('address', models.URLField(verbose_name='address site')),
                ('telephone', models.PositiveIntegerField(blank=True, null=True, verbose_name='telephone')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='engineer.Area', to_field='slug')),
                ('engineers', models.ManyToManyField(blank=True, related_name='customers', to='engineer.Engineer')),
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
