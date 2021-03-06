# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-26 02:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('hardware', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callRecordSize', models.IntegerField(default=0)),
                ('textSize', models.IntegerField(default=0)),
                ('initialDataSize', models.IntegerField(default=0)),
                ('ldapCIPSize', models.IntegerField(default=0)),
                ('sessionCIPSize', models.IntegerField(default=0)),
                ('otherCIPSize', models.IntegerField(default=0)),
                ('callCost', models.FloatField(default=0)),
                ('cpuCostForServer', models.FloatField(default=0.15)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CallCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callCost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CallType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Call Type')),
                ('ss7InSize', models.IntegerField(default=0)),
                ('ss7OutSize', models.IntegerField(default=0)),
                ('ss7Number', models.IntegerField(default=0)),
                ('tcpipSize', models.IntegerField(default=0)),
                ('tcpipNumber', models.IntegerField(default=0)),
                ('diameterSize', models.IntegerField(default=0)),
                ('diameterNumber', models.IntegerField(default=0)),
                ('mateUpdateNumber', models.IntegerField(default=0)),
                ('ndbCPUUsageLimitation', models.FloatField(default=0.6)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CounterCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counterNumberPerRecord', models.IntegerField(default=6)),
                ('costDBReadUpdatePerRecord', models.FloatField(default=0)),
                ('costPerAppliedBucket', models.FloatField(default=0)),
                ('costPerAppliedUBD', models.FloatField(default=0)),
                ('costPerUnappliedBucket', models.FloatField(default=0)),
                ('costPerUnappliedUBD', models.FloatField(default=0)),
                ('costPerUnappliedCounterWithBasicCriteria', models.FloatField(default=0)),
                ('costTurnOnbucket', models.FloatField(default=0)),
                ('costTurnOnUBD', models.FloatField(default=0)),
                ('costTurnOnUnappliedCounter', models.FloatField(default=0)),
                ('costCounterNumberImpact', models.FloatField(default=0)),
                ('percentageCounterNumberImpact', models.FloatField(default=0)),
                ('costGroupDBReadUpdatePerRecord', models.FloatField(default=0)),
                ('costTurnOnGroupBucket', models.FloatField(default=0)),
                ('costPerGroupSideBucket', models.FloatField(default=0)),
                ('costBundlePerRecord', models.FloatField(default=0)),
                ('costPer24hBundle', models.FloatField(default=0)),
                ('hardwareModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.HardwareModel')),
            ],
        ),
        migrations.CreateModel(
            name='CounterCostName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DBInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recordSize', models.IntegerField(default=0, verbose_name='Record Size')),
            ],
            options={
                'ordering': ['db'],
            },
        ),
        migrations.CreateModel(
            name='DBName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('ndbRefPlaceholderRatio', models.FloatField(default=0, verbose_name='Reference Placeholder Ratio for NDB')),
                ('isPrefixTable', models.BooleanField(default=False, verbose_name='Is Prefix Table?')),
                ('prefixTableIndexNumber', models.IntegerField(default=0, verbose_name='Prefix Table Index Number')),
                ('rtdbOverhead', models.FloatField(default=0, verbose_name='RTDB Overhead')),
                ('todoLogSize', models.IntegerField(default=0, verbose_name='Todo Log Size')),
                ('mateLogSize', models.IntegerField(default=0, verbose_name='Mate Log Size')),
                ('updateTimes', models.FloatField(default=0, verbose_name='Update Times')),
                ('defaultMemberFactor', models.FloatField(default=0, verbose_name='Default Factor for Member')),
                ('defaultGroupFactor', models.FloatField(default=0, verbose_name='Default Factor for Group')),
                ('defaultMemberCounterFactor', models.FloatField(default=0, verbose_name='Default Factor for Member Counter')),
                ('defaultGroupCounterFactor', models.FloatField(default=0, verbose_name='Default Factor for Group Counter')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FeatureCallTypeConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featureApplicable', models.FloatField(default=1)),
                ('callType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.CallType')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureCPUImpact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccImpactCPUTime', models.FloatField(default=0)),
                ('ccImpactCPUPercentage', models.FloatField(default=0)),
                ('ss7In', models.IntegerField(default=0)),
                ('ss7Out', models.IntegerField(default=0)),
                ('reImpactCPUTime', models.FloatField(default=0)),
                ('reImpactCPUPercentage', models.FloatField(default=0)),
                ('ldapMessageSize', models.IntegerField(default=0)),
                ('diameterMessageSize', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureDBImpact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memberImpactFactor', models.FloatField(default=0)),
                ('groupImpactFactor', models.FloatField(default=0)),
                ('dbName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.DBName')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('impactDB', models.CharField(max_length=64)),
                ('comment', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OtherApplicationInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maxTrafficPerNode', models.IntegerField()),
                ('clientNumber', models.IntegerField()),
                ('minClient', models.IntegerField()),
                ('maxNodePerSystem', models.IntegerField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.ApplicationName')),
                ('hardwareModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.HardwareModel')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('sequence', models.IntegerField()),
                ('callRecordSize', models.IntegerField()),
                ('ldapCIPSize', models.IntegerField()),
                ('sessionCIPSize', models.IntegerField()),
                ('otherCIPSize', models.IntegerField()),
                ('cpuCostForNormalAMA', models.FloatField(default=0.8)),
                ('cPUCostForMultipleAMA', models.FloatField(default=0.4)),
                ('amaSizePerBlock', models.IntegerField(default=3072)),
                ('amaNumberPerGroupCall', models.IntegerField(default=1)),
                ('counterNumberPerRecord', models.IntegerField(default=6)),
            ],
            options={
                'ordering': ['-sequence'],
            },
        ),
        migrations.AddField(
            model_name='featuredbimpact',
            name='featureName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.FeatureName'),
        ),
        migrations.AddField(
            model_name='featurecpuimpact',
            name='featureName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.FeatureName'),
        ),
        migrations.AddField(
            model_name='featurecalltypeconfiguration',
            name='featureName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.FeatureName'),
        ),
        migrations.AddField(
            model_name='dbinformation',
            name='db',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.DBName'),
        ),
        migrations.AddField(
            model_name='dbinformation',
            name='mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.DBMode'),
        ),
        migrations.AddField(
            model_name='dbinformation',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Release'),
        ),
        migrations.AddField(
            model_name='currentrelease',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Release'),
        ),
        migrations.AddField(
            model_name='countercost',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Release'),
        ),
        migrations.AddField(
            model_name='callcost',
            name='callType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.CallType'),
        ),
        migrations.AddField(
            model_name='callcost',
            name='dbMode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.DBMode'),
        ),
        migrations.AddField(
            model_name='callcost',
            name='hardwareModel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.HardwareModel'),
        ),
        migrations.AddField(
            model_name='callcost',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Release'),
        ),
        migrations.AddField(
            model_name='applicationinformation',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.ApplicationName'),
        ),
        migrations.AddField(
            model_name='applicationinformation',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Release'),
        ),
    ]
