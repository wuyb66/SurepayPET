# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-22 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20180118_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationconfiguration',
            name='trafficBHTA',
            field=models.FloatField(default=0),
        ),
    ]
