# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calltype',
            name='mateUpdateSize',
            field=models.IntegerField(default=0),
        ),
    ]
