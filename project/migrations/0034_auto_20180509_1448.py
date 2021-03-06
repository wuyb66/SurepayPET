# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-09 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0033_auto_20180509_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinformation',
            name='sigtranLinkNumber',
            field=models.IntegerField(default=1, verbose_name='SIGTRAN Link Number'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='sigtranLinkSpeed',
            field=models.IntegerField(default=10000, verbose_name='SIGTRAN Link Speed (Mb/s)'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='sigtranPortUtil',
            field=models.FloatField(default=0.3, verbose_name='SIGTRAN Port Utility'),
        ),
    ]
