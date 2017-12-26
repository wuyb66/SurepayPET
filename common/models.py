from django.db import models


class GlobalConfiguration(models.Model):
    maintananceWindowHour = models.IntegerField(default=10)
    trafficPercentageUnderMaitananceWindow = models.FloatField(default=1)
    releaseCPUImpact = models.FloatField(default=0.05)
    releaseAppMemoryImpact = models.FloatField(default=0.1)
    releaseDBMemoryImpact = models.FloatField(default=0.1)
    releaseCountCPUImpact = models.FloatField(default=0.05)
    reservedCPURatio = models.FloatField(default=0.15)
    ndbRTDBCostRatio = models.FloatField(default=1.3)


class DBMode(models.Model):
    DATABASE_MODE_OPTION = (('RTDB', 'RTDB'), ('NDB', 'NDB'))

    name = models.CharField(max_length=10, choices=DATABASE_MODE_OPTION, default='RTDB')

    def __str__(self):
        return self.name


class NetworkInfo(models.Model):
    defaultSIGTRANLinkSpeed = models.IntegerField()
    defaultSIGTRANLinkNumber = models.IntegerField()
    maxSIGTRANPortUtil = models.FloatField()
