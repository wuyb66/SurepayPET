# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-09 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0004_auto_20180420_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardwaremodel',
            name='defaultIOCPUNumber',
            field=models.IntegerField(default=16),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='defaultIOMemory',
            field=models.IntegerField(default=32),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='defaultPilotCPUNumber',
            field=models.IntegerField(default=8),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='defaultPilotMemory',
            field=models.IntegerField(default=32),
        ),
    ]
