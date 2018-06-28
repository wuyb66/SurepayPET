# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-26 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_dimensioningresult_calculated_app_node_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimensioningresult',
            name='bound_type',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AddField(
            model_name='dimensioningresult',
            name='calculated_db_node_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dimensioningresult',
            name='calculated_io_node_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dimensioningresult',
            name='calculated_system_number',
            field=models.IntegerField(default=0),
        ),
    ]
