from django.db import models
from hardware.models import CPU, HardwareModel
from common.models import DBMode


class Release(models.Model):
    name = models.CharField(max_length=20)
    sequence = models.IntegerField()

    callRecordSize = models.IntegerField()
    ldapCIPSize = models.IntegerField()
    sessionCIPSize = models.IntegerField()
    otherCIPSize = models.IntegerField()

    cpuCostForNormalAMA = models.FloatField(default=0.8)     # Call cost(ms) based on Bono blade
    cPUCostForMultipleAMA = models.FloatField(default=0.4)     # Call cost(ms) based on Bono blade
    amaSizePerBlock = models.IntegerField(default=3072)
    amaNumberPerGroupCall = models.IntegerField(default=1)

    counterNumberPerRecord = models.IntegerField(default=6)     # Counter number per CTRTDB record



    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-sequence']


class CurrentRelease(models.Model):
    release = models.ForeignKey(Release)

    def __str__(self):
        return self.release.name

    name = property(__str__)

class ApplicationName(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class ApplicationInformation(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    application = models.ForeignKey(ApplicationName, on_delete=models.CASCADE)

    callRecordSize = models.IntegerField(default=0)     # Bytes
    textSize = models.IntegerField(default=0)           # MB
    initialDataSize = models.IntegerField(default=0)    # MB
    ldapCIPSize = models.IntegerField(default=0)        # Bytes
    sessionCIPSize = models.IntegerField(default=0)     # Bytes
    otherCIPSize = models.IntegerField(default=0)       # Bytes
    callCost  = models.FloatField(default=0)            # Call cost(ms) based on Bono blade
    cpuCostForServer = models.FloatField(default=0.15)      # Call cost(ms) for server based on Bono blade

    def __str__(self):
        return self.release.name + '_' + self.application.name

    name = property(__str__)

class OtherApplicationInformation(models.Model):
    # release = models.ForeignKey(Release, on_delete=models.CASCADE)
    application = models.ForeignKey(ApplicationName, on_delete=models.CASCADE)
    hardwareModel = models.ForeignKey(HardwareModel, on_delete=models.CASCADE)
    #dbMode = models.ForeignKey(DBMode, on_delete=models.CASCADE)

    maxTrafficPerNode = models.IntegerField()
    clientNumber = models.IntegerField()
    minClient = models.IntegerField()
    maxNodePerSystem = models.IntegerField()

    @property
    def name(self):
        return self.application.name + '_' + self.hardwareModel.name

    def __str__(self):
        return self.application.name

class DBName(models.Model):
    name = models.CharField(max_length=20)

    ndbRefPlaceholderRatio = models.FloatField(
        default=0,
        verbose_name='Reference Placeholder Ratio for NDB',
    )

    isPrefixTable = models.BooleanField(
        default=False,
        verbose_name='Is Prefix Table?',
    )

    prefixTableIndexNumber = models.IntegerField(
        default=0,
        verbose_name='Prefix Table Index Number',
    )

    rtdbOverhead = models.FloatField(
        default=0,
        verbose_name='RTDB Overhead',
    )     # 1.3 or 7.9
    todoLogSize = models.IntegerField(
        default=0,
        verbose_name='Todo Log Size',
    )
    mateLogSize  = models.IntegerField(
        default=0,
        verbose_name='Mate Log Size',
    )
    updateTimes = models.FloatField(
        default=0,
        verbose_name='Update Times',
    )     # Update times for todo log and mate log

    defaultMemberFactor = models.FloatField(
        default=0,
        verbose_name='Default Factor for Member',
    )

    defaultGroupFactor = models.FloatField(
        default=0,
        verbose_name='Default Factor for Group',
    )

    defaultMemberCounterFactor = models.FloatField(
        default=0,
        verbose_name='Default Factor for Member Counter',
    )

    defaultGroupCounterFactor = models.FloatField(
        default=0,
        verbose_name='Default Factor for Group Counter',
    )


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
class DBInformation(models.Model):
    db = models.ForeignKey(DBName, on_delete=models.CASCADE)
    mode = models.ForeignKey(DBMode, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE)

    recordSize = models.IntegerField(
        default=0,
        verbose_name='Record Size',
    )



    @property
    def name(self):
        return self.db.name + '_' +  self.release.name + '_' + self.mode.name

    def __str__(self):
        return self.db.name
    class Meta:
        ordering = ['db']

class FeatureName(models.Model):
    name = models.CharField(max_length=64)
    impactDB = models.CharField(max_length=64)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return self.name

'''
    Define the database impact parameter by feature.
    Need to add the default impact for some tables such as: SIM, ACM, AI, GPRSSIM, GTM
'''
class FeatureDBImpact(models.Model):
    dbName = models.ForeignKey(DBName, on_delete=models.CASCADE)
    featureName = models.ForeignKey(FeatureName, on_delete=models.CASCADE)

    memberImpactFactor = models.FloatField(default=0)
    groupImpactFactor = models.FloatField(default=0)

    def __str__(self):
        return self.dbName.name + '_' + self.featureName.name

    name = property(__str__)


class FeatureCPUImpact(models.Model):
    featureName = models.ForeignKey(FeatureName, on_delete=models.CASCADE)

    ccImpactCPUTime = models.FloatField(default=0)
    ccImpactCPUPercentage = models.FloatField(default=0)
    ss7In = models.IntegerField(default=0)
    ss7Out = models.IntegerField(default=0)
    reImpactCPUTime = models.FloatField(default=0)
    reImpactCPUPercentage = models.FloatField(default=0)
    #reSS7InSize = models.IntegerField(default=0)
    #reSS7OutSize = models.IntegerField(default=0)
    ldapMessageSize = models.IntegerField(default=0)
    diameterMessageSize = models.IntegerField(default=0)

    def __str__(self):
        return self.featureName.name

    name = property(__str__)


class CallType(models.Model):
    name = models.CharField(max_length=64, verbose_name='Call Type')

    ss7InSize = models.IntegerField(default=0)
    ss7OutSize = models.IntegerField(default=0)
    ss7Number = models.IntegerField(default=0)
    tcpipSize = models.IntegerField(default=0)
    tcpipNumber = models.IntegerField(default=0)
    diameterSize = models.IntegerField(default=0)
    diameterNumber = models.IntegerField(default=0)
    mateUpdateNumber = models.IntegerField(default=0)

    ndbCPUUsageLimitation = models.FloatField(default=0.6)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CallCost(models.Model):
    callType = models.ForeignKey(CallType, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    hardwareModel = models.ForeignKey(HardwareModel, on_delete=models.CASCADE)
    dbMode = models.ForeignKey(DBMode, on_delete=models.CASCADE)

    callCost = models.FloatField()

    def __str__(self):
        return self.callType.name + '_' +  self.release.name + '_' + self.hardwareModel.name + '_' + self.dbMode.name

    name = property(__str__)


class FeatureCallTypeConfiguration(models.Model):
    callType = models.ForeignKey(CallType, on_delete=models.CASCADE)
    featureName = models.ForeignKey(FeatureName, on_delete=models.CASCADE)

    featureApplicable = models.FloatField(default=1)



class CounterCostName(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CounterCost(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    hardwareModel = models.ForeignKey(HardwareModel, on_delete=models.CASCADE)
    counterNumberPerRecord = models.IntegerField(default=6)
    costDBReadUpdatePerRecord = models.FloatField(default=0)
    costPerAppliedBucket = models.FloatField(default=0)
    costPerAppliedUBD = models.FloatField(default=0)
    costPerUnappliedBucket = models.FloatField(default=0)
    costPerUnappliedUBD = models.FloatField(default=0)
    costPerUnappliedCounterWithBasicCriteria = models.FloatField(default=0)
    costTurnOnbucket = models.FloatField(default=0)
    costTurnOnUBD = models.FloatField(default=0)
    costTurnOnUnappliedCounter = models.FloatField(default=0)
    costCounterNumberImpact = models.FloatField(default=0)
    percentageCounterNumberImpact = models.FloatField(default=0)
    costGroupDBReadUpdatePerRecord = models.FloatField(default=0)
    costTurnOnGroupBucket = models.FloatField(default=0)
    costPerGroupSideBucket = models.FloatField(default=0)
    costBundlePerRecord = models.FloatField(default=0)
    costPer24hBundle = models.FloatField(default=0)

    def __str__(self):
        return self.release.name + '_' + self.hardwareModel.name

    name = property(__str__)
