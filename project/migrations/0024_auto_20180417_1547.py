# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-17 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20180403_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationconfiguration',
            name='boundType',
            field=models.CharField(choices=[('CPU Bound', 'CPU Bound'), ('Memory Bound', 'Memory Bound'), ('-', '-')], default='CPU Bound', max_length=20, verbose_name='Bound Type'),
        ),
        migrations.AlterField(
            model_name='calculatedresult',
            name='boundType',
            field=models.CharField(choices=[('CPU Bound', 'CPU Bound'), ('Memory Bound', 'Memory Bound'), ('-', '-')], default='-', max_length=20, verbose_name='Bound Type'),
        ),
        migrations.AlterField(
            model_name='calculatedresult',
            name='calCPUAppNumber',
            field=models.FloatField(default=0, verbose_name='Calculated App Node Number (CPU Based)'),
        ),
        migrations.AlterField(
            model_name='calculatedresult',
            name='calMemAppNumber',
            field=models.FloatField(default=0, verbose_name='Calculated App Node Number (Memory Based)'),
        ),
    ]