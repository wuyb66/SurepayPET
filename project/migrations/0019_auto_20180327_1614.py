# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 08:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_auto_20180327_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinformation',
            name='cpuNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='APP_CPU_Number', to='hardware.CPUList', verbose_name='CPU Number'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='dbCPUNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DB_CPU_Number', to='hardware.CPUList', verbose_name='DB CPU Number'),
        ),
    ]
