# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-20 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0003_hardwaretype_issingleserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardwaremodel',
            name='maxAppNodeNumber',
            field=models.IntegerField(default=26),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='maxDBNodeNumber',
            field=models.IntegerField(default=8),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='maxIONodeNumber',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='maxPilotNodeNumber',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='minAppNodeNumber',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='minDBNodeNumber',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='minIONodeNumber',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='hardwaremodel',
            name='minPilotNodeNumber',
            field=models.IntegerField(default=2),
        ),
    ]