# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-11 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_applicationinformation_countermemoryimpact'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='counterMemoryImpact',
            field=models.FloatField(default=0),
        ),
    ]
