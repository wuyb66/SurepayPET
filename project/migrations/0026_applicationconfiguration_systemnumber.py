# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-18 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_calculatedresult_systemnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationconfiguration',
            name='systemNumber',
            field=models.FloatField(default=0),
        ),
    ]
