# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_auto_20180327_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinformation',
            name='deploy_option',
            field=models.CharField(choices=[('Combo', 'Combo'), ('Individual', 'Individual')], default='Combo', max_length=16, verbose_name='NDB Deploy Option'),
        ),
    ]
