# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-30 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20171228_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationconfiguration',
            name='dbCPUCost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='applicationconfiguration',
            name='inactiveSubscriber',
            field=models.IntegerField(default=0, verbose_name='Inactive Subscriber'),
        ),
    ]
