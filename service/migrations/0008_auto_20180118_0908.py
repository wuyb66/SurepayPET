# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-18 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_auto_20180104_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationinformation',
            old_name='asCost',
            new_name='aprocRoutingCost',
        ),
        migrations.AddField(
            model_name='applicationinformation',
            name='asdCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationinformation',
            name='asdMateCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationinformation',
            name='cpuCostForRoutingClient',
            field=models.FloatField(default=0),
        ),
    ]