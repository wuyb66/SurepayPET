# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-26 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_auto_20180426_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimensioningresultpersystem',
            name='mateNodeNumber',
            field=models.IntegerField(default=0),
        ),
    ]