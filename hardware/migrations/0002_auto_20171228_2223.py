# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-28 14:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cputuning',
            old_name='hardware_type',
            new_name='hardwareType',
        ),
        migrations.RenameField(
            model_name='hardwaremodel',
            old_name='hardware_type',
            new_name='hardwareType',
        ),
    ]
