# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-11 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20180118_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationinformation',
            name='counterMemoryImpact',
            field=models.FloatField(default=0),
        ),
    ]
