# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 08:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_auto_20180327_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinformation',
            name='dbMemory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DB_Memory', to='hardware.MemoryList', verbose_name='DB Memory'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='memory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='APP_Memory', to='hardware.MemoryList', verbose_name='Memory'),
        ),
    ]
