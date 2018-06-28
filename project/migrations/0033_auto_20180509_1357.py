# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-09 05:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0032_auto_20180426_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbconfiguration',
            name='placeholderRatio',
            field=models.FloatField(default=0, verbose_name='Placeholder Ratio'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='ioCPUNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='IO_CPU_Number', to='hardware.CPUList', verbose_name='IO CPU Number'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='ioMemory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='IO_Memory', to='hardware.MemoryList', verbose_name='IO Memory'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='pilotCPUNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Pilot_CPU_Number', to='hardware.CPUList', verbose_name='Pilot CPU Number'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='pilotMemory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Pilot_Memory', to='hardware.MemoryList', verbose_name='Pilot Memory'),
        ),
    ]
