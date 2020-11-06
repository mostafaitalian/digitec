# Generated by Django 2.2.17 on 2020-11-03 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0044_auto_20201104_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='machines_dep', to='customer.Department'),
        ),
        migrations.AlterUniqueTogether(
            name='machine',
            unique_together={('serial', 'machine_model')},
        ),
        migrations.CreateModel(
            name='MachineContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('mobile', models.IntegerField()),
                ('telephone', models.PositiveIntegerField(blank=True, null=True)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine_contacts', to='machine.Machine')),
            ],
        ),
    ]
