# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-11 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_applicationconfiguration_trafficbhta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinformation',
            name='clientNumber',
            field=models.IntegerField(default=0, verbose_name='Client Number'),
        ),
    ]
