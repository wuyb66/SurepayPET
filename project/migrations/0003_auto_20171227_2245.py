# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_calculatedresult_dimensioningresult_dimensioningresultpersystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='trafficinformation',
            name='aprocCPUCost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='trafficinformation',
            name='asCPUCost',
            field=models.FloatField(default=0),
        ),
    ]