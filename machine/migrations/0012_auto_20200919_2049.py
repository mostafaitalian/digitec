# Generated by Django 2.2.15 on 2020-09-19 18:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineer', '0004_auto_20200919_2049'),
        ('machine', '0011_auto_20200913_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='assigned_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 19, 20, 49, 22, 675511)),
        ),
        migrations.AlterField(
            model_name='call',
            name='completed_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 20, 2, 49, 22, 675511), help_text='the default value is 6 hours + assign_date'),
        ),
        migrations.AlterField(
            model_name='call',
            name='response_time_end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 19, 20, 49, 22, 675511), null=True),
        ),
        migrations.CreateModel(
            name='EngineerReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(blank='True', null=True)),
                ('state', models.CharField(choices=[('pending', 'pending'), ('published', 'published'), ('rejected', 'rejected')], max_length=50)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engineer.Engineer')),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='machine.Machine')),
            ],
            options={
                'permissions': (('can_approve_or_reject_review', 'can approve or reject review'),),
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(blank=True, choices=[('FSMA', 'FSMA'), ('Time', 'Time'), ('LIS', 'LIS'), ('FM', 'FM'), ('XPPS', 'XPPS')], max_length=50, null=True)),
                ('machine', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='machine.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engineer.Engineer')),
                ('engineer_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machine.EngineerReview')),
            ],
        ),
    ]
