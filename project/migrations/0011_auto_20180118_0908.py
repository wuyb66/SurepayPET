# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-18 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_applicationconfiguration_ndbcpulimitation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationconfiguration',
            old_name='asCPUCost',
            new_name='aprocRoutingCost',
        ),
        migrations.RenameField(
            model_name='trafficinformation',
            old_name='asCPUCost',
            new_name='aprocRoutingCost',
        ),
        migrations.AddField(
            model_name='applicationconfiguration',
            name='asdCPUCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationconfiguration',
            name='asdMateCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationconfiguration',
            name='cpuCostForRoutingClient',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='trafficinformation',
            name='asdCPUCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='trafficinformation',
            name='asdMateCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='trafficinformation',
            name='cpuCostForRoutingClient',
            field=models.FloatField(default=0),
        ),
    ]
