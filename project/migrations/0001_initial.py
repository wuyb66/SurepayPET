# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-26 06:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deployOption', models.CharField(choices=[('EPAY Node', 'EPAY Node'), ('DRouter Node', 'DRouter Node'), ('CDR Pre-Processor Node', 'CDR Pre-Processor Node'), ('eCGS Node', 'eCGS Node'), ('NTGW Node', 'NTGW Node'), ('eCTRL Node', 'eCTRL Node'), ('EPPSM Node', 'EPPSM Node'), ('GRouter Node', 'GRouter Node')], max_length=30, verbose_name='Deploy Option')),
                ('activeSubscriber', models.IntegerField(default=0, verbose_name='Active Subscriber')),
                ('inactiveSubscriber', models.IntegerField(default=0, verbose_name='Inctive Subscriber')),
                ('trafficTPS', models.FloatField(default=0, verbose_name='CPS/TPS')),
                ('serverCPUCost', models.FloatField(default=0)),
                ('clientCPUCost', models.FloatField(default=0)),
                ('totalCPUCost', models.FloatField(default=0)),
                ('ss7CPUCost', models.FloatField(default=0)),
                ('tcpCPUCost', models.FloatField(default=0)),
                ('miscCPUCost', models.FloatField(default=0)),
                ('cpuBudget', models.FloatField(default=0)),
                ('ss7InSizePerSecond', models.FloatField(default=0)),
                ('ss7OutSizePerSecond', models.FloatField(default=0)),
                ('ldapSizePerSecond', models.FloatField(default=0)),
                ('diameterSizePerSecond', models.FloatField(default=0)),
                ('muTCPSize', models.FloatField(default=0)),
                ('featureLDAPSize', models.FloatField(default=0)),
                ('featureDiameterSize', models.FloatField(default=0)),
                ('memoryUsage', models.FloatField(default=0)),
                ('clientCPUUsagePercentage', models.FloatField(default=0)),
                ('dbCacheSize', models.FloatField(default=0)),
                ('spaTextSize', models.FloatField(default=0)),
                ('amaPerSecond', models.FloatField(default=0)),
                ('cpuBaseNodeNumber', models.FloatField(default=0)),
                ('memoryBaseNodeNumber', models.FloatField(default=0)),
                ('ss7BaseNodeNumber', models.FloatField(default=0)),
                ('nodeNumberNeeded', models.FloatField(default=0)),
                ('ndbMateNode', models.FloatField(default=0)),
                ('ndbRoutingNode', models.FloatField(default=0)),
                ('dbNodeNumberNeeded', models.FloatField(default=0)),
                ('ss7BaseIONodeNumber', models.FloatField(default=0)),
                ('ldapBaseIONodeNumber', models.FloatField(default=0)),
                ('diameterBaseIONodeNumber', models.FloatField(default=0)),
                ('ioNodeNumberNeeded', models.FloatField(default=0)),
                ('boundType', models.CharField(choices=[('CPU Bound', 'CPU Bound'), ('Memory Bound', 'Memory Bound')], default='CPU Bound', max_length=20, verbose_name='Bound Type')),
                ('applicationName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.ApplicationName', verbose_name='Application Name')),
            ],
            options={
                'verbose_name': 'Application Configuration',
                'verbose_name_plural': 'Application Configuration',
            },
        ),
        migrations.CreateModel(
            name='CallTypeCounterConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('averageBundleNumberPerSubscriber', models.FloatField(default=0, verbose_name='Number of Bundle')),
                ('average24hBundleNumberPerSubscriber', models.FloatField(default=0, verbose_name='Number of 24h Bundle')),
                ('nonAppliedBucketNumber', models.FloatField(default=0, verbose_name='Non Applied Bucket Number')),
                ('nonAppliedUBDNumber', models.FloatField(default=0, verbose_name='Non Applied UBD Number')),
                ('appliedBucketNumber', models.FloatField(default=0, verbose_name='Applied Bucket Number')),
                ('appliedUBDNumber', models.FloatField(default=0, verbose_name='Applied UBD Number')),
                ('callType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.CallType')),
            ],
            options={
                'verbose_name': 'Counter Configuration for Call Type',
                'verbose_name_plural': 'Counter Configuration for Call Type',
            },
        ),
        migrations.CreateModel(
            name='CounterConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('averageBundleNumberPerSubscriber', models.FloatField(default=0, verbose_name='Number of Bundle')),
                ('average24hBundleNumberPerSubscriber', models.FloatField(default=0, verbose_name='Number of 24h Bundle')),
                ('nonAppliedBucketNumber', models.FloatField(default=0, verbose_name='Non Applied Bucket Number')),
                ('nonAppliedUBDNumber', models.FloatField(default=0, verbose_name='Non Applied UBD Number')),
                ('appliedBucketNumber', models.FloatField(default=0, verbose_name='Applied Bucket Number')),
                ('appliedUBDNumber', models.FloatField(default=0, verbose_name='Applied UBD Number')),
                ('groupBundleNumber', models.FloatField(default=0, verbose_name='Number of Group Bundle')),
                ('groupBucketNumber', models.FloatField(default=0, verbose_name='Group Bucket Number')),
                ('generateMultipleAMAForCounter', models.BooleanField(default=False, verbose_name='Generate Multiple AMA For Counter')),
                ('turnOnBasicCriteriaCheck', models.BooleanField(default=False, verbose_name='Enable Basic Criteria Check')),
                ('configureForCallType', models.BooleanField(default=False, verbose_name='Configure Counter For Call Types')),
            ],
            options={
                'verbose_name': 'Counter Configuration',
                'verbose_name_plural': 'Counter Configuration',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='DBConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dbFactor', models.FloatField(default=0, verbose_name='DB Factor')),
                ('placeholderRatio', models.FloatField(default=0, verbose_name='Placeholder Ratio (%)')),
                ('memberGroupOption', models.CharField(choices=[('Member', 'Member'), ('Group', 'Group')], default='member', max_length=10, verbose_name='DB Option')),
                ('recordSize', models.IntegerField(default=0)),
                ('subscriberNumber', models.IntegerField(default=0)),
                ('recordNumber', models.IntegerField(default=0)),
                ('cacheSize', models.IntegerField(default=0)),
                ('todoLogSize', models.IntegerField(default=0)),
                ('mateLogSize', models.IntegerField(default=0)),
                ('referencePlaceholderRatio', models.IntegerField(default=0)),
                ('referenceDBFactor', models.IntegerField(default=0)),
                ('dbInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.DBInformation', verbose_name='DB Name')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featurePenetration', models.FloatField(default=0, verbose_name='Feature Penetration (%)')),
                ('colocateMemberGroup', models.BooleanField(default=True)),
                ('rtdbSolution', models.BooleanField(default=True)),
                ('groupNumber', models.FloatField(default=1)),
                ('ratioOfLevel1', models.FloatField(default=1)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.FeatureName', verbose_name='Feature Name')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Name')),
                ('version', models.IntegerField(default=1, verbose_name='Version')),
                ('createTime', models.TimeField(auto_now=True, verbose_name='Create Time')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Customer', verbose_name='Customer')),
                ('database_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.DBMode', verbose_name='Database Type')),
                ('hardwareModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.HardwareModel', verbose_name='Hardware Model')),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Release', verbose_name='Release')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Project',
            },
        ),
        migrations.CreateModel(
            name='ProjectInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientNumber', models.IntegerField(verbose_name='Client Number')),
                ('sigtranLinkSpeed', models.IntegerField(verbose_name='SIGTRAN Link Speed')),
                ('sigtranLinkNumber', models.IntegerField(verbose_name='SIGTRAN Link Number')),
                ('sigtranPortUtil', models.FloatField(verbose_name='SIGTRAN Port Utility')),
                ('amaRecordPerBillingBlock', models.FloatField(default=1, verbose_name='AMA Record Number per Billing Block')),
                ('numberReleaseToEstimate', models.IntegerField(default=0, verbose_name='Number of Release to Estimate')),
                ('cpuImpactPerRelease', models.FloatField(default=0.05, verbose_name='CPU Impact per Release')),
                ('memoryImpactPerRelease', models.FloatField(default=0.1, verbose_name='Memory Impact per Release')),
                ('dbImpactPerRelease', models.FloatField(default=0.1, verbose_name='DB Impact per Release')),
                ('deploy_option', models.CharField(choices=[('individual', 'Individual'), ('combo', 'Combo')], default='combo', max_length=16, verbose_name='NDB Deploy Option')),
                ('averageAMARecordPerCall', models.FloatField(verbose_name='Average AMA Record per Call')),
                ('amaStoreDay', models.FloatField(verbose_name='AMA Store Days')),
                ('activeSubscriber', models.IntegerField(verbose_name='Active Subscriber')),
                ('inactiveSubscriber', models.IntegerField(verbose_name='Inactive Subscriber')),
                ('groupAccountNumber', models.IntegerField(verbose_name='Number of Group Account')),
                ('cpuNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.CPUList', verbose_name='CPU Number')),
                ('cpuUsageTuning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.CPUTuning', verbose_name='CPU Usage Tuning')),
                ('memory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.MemoryList', verbose_name='Memory')),
                ('memoryUsageTuning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.MemoryUsageTuning', verbose_name='Memory Usage Tuning')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('vmType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.VMType', verbose_name='VM Type')),
            ],
            options={
                'verbose_name': 'Project General Information',
                'verbose_name_plural': 'Project General Information',
            },
        ),
        migrations.CreateModel(
            name='SystemConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cabinetNumberPerSystem', models.IntegerField(default=1, verbose_name='Number of Cabinet Per System')),
                ('backupAppNodeNumberPerSystem', models.IntegerField(default=0, verbose_name='Number of Backup App Node Per System')),
                ('spareAppNodeNumberPerSystem', models.IntegerField(default=0, verbose_name='Number of Spare App Node Per System')),
                ('backupDBNodeNumberPerSystem', models.IntegerField(default=0, verbose_name='Number of Backup DB Node Per System')),
                ('spareDBNodePairNumberPerSystem', models.IntegerField(default=0, verbose_name='Number of Spare DB Node Pair Per System')),
                ('applicationName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.ApplicationName', verbose_name='Application Name')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
            options={
                'verbose_name': 'System Configuration',
                'verbose_name_plural': 'System Configuration',
            },
        ),
        migrations.CreateModel(
            name='TrafficInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activeSubscriber', models.IntegerField(verbose_name='Active Subscriber')),
                ('inactiveSubscriber', models.IntegerField(verbose_name='Inctive Subscriber')),
                ('trafficBHTA', models.FloatField(default=0, verbose_name='BHCA/BHTA')),
                ('trafficTPS', models.FloatField(default=0, verbose_name='CPS/TPS')),
                ('callHoldingTime', models.IntegerField(default=0, verbose_name='Call Holding Time')),
                ('averageActiveSessionPerSubscriber', models.FloatField(default=0)),
                ('averageCategoryPerCCR', models.FloatField(default=1)),
                ('averageCategoryPerSession', models.FloatField(default=1)),
                ('volumeCCRiBHTA', models.FloatField(default=0)),
                ('volumeCCRuBHTA', models.FloatField(default=0)),
                ('volumeCCRtBHTA', models.FloatField(default=0)),
                ('timeCCRiBHTA', models.FloatField(default=0)),
                ('timeCCRuBHTA', models.FloatField(default=0)),
                ('timeCCRtBHTA', models.FloatField(default=0)),
                ('serverCPUCost', models.FloatField(default=0)),
                ('cpuCostPerCall', models.FloatField(default=0)),
                ('totalCPUCost', models.FloatField(default=0)),
                ('ss7CPUCost', models.FloatField(default=0)),
                ('tcpCPUCost', models.FloatField(default=0)),
                ('ss7InSizePerSecond', models.FloatField(default=0)),
                ('ss7OutSizePerSecond', models.FloatField(default=0)),
                ('ldapSizePerSecond', models.FloatField(default=0)),
                ('diameterSizePerSecond', models.FloatField(default=0)),
                ('muTCPSize', models.FloatField(default=0)),
                ('featureLDAPSize', models.FloatField(default=0)),
                ('featureDiameterSize', models.FloatField(default=0)),
                ('ndbCPULimitation', models.FloatField(default=0)),
                ('featureCost', models.FloatField(default=0)),
                ('counterCost', models.FloatField(default=0)),
                ('callType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.CallType', verbose_name='Call Type')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
        ),
        migrations.AddField(
            model_name='featureconfiguration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='dbconfiguration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='counterconfiguration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='calltypecounterconfiguration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='applicationconfiguration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='trafficinformation',
            unique_together=set([('project', 'callType')]),
        ),
        migrations.AlterUniqueTogether(
            name='featureconfiguration',
            unique_together=set([('project', 'feature')]),
        ),
    ]