# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-21 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_featureadditionalimpact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurecalltypeconfiguration',
            name='featureApplicable',
            field=models.FloatField(default=0),
        ),
    ]
