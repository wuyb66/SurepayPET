# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-04 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20171230_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='callcost',
            name='aprocCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='callcost',
            name='aprocRoutingCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='callcost',
            name='asdCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='callcost',
            name='asdMateCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='callcost',
            name='cpuCostForRoutingClient',
            field=models.FloatField(default=0.15),
        ),
        migrations.AddField(
            model_name='callcost',
            name='cpuCostForServer',
            field=models.FloatField(default=0.15),
        ),
        migrations.AddField(
            model_name='callcost',
            name='diamCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='callcost',
            name='ss7Cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='callcost',
            name='tcpCost',
            field=models.FloatField(default=0),
        ),
    ]
