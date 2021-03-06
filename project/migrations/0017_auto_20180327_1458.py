# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_dbconfiguration_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationconfiguration',
            name='counterMemory',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='deploy_option',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Combo', 'Combo')], default='combo', max_length=16, verbose_name='NDB Deploy Option'),
        ),
    ]
