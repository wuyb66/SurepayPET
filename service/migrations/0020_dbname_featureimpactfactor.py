# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-10 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0019_release_trafficrequirededicatemate'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbname',
            name='featureImpactFactor',
            field=models.FloatField(default=0, verbose_name='Feature Impact Factor'),
        ),
    ]
