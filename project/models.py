from django.db import models
from django.contrib.auth.models import User
from service.models import Release, CallType, FeatureName, DBInformation, CallCost, \
    ApplicationName, FeatureDBImpact, FeatureCallTypeConfiguration, FeatureCPUImpact, \
    CounterCost, ApplicationInformation
from hardware.models import CPUTuning, MemoryUsageTuning, HardwareModel, VMType, \
    HardwareType, CPU, CPUList, MemoryList
from common.models import DBMode, GlobalConfiguration
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import ValidationError

import math

# from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField, ChainedManyToManyField2


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

SERVER_STATUS = (
    (0, u"Normal"),
    (1, u"Down"),
    (2, u"No Connect"),
    (3, u"Error"),
)
SERVICE_TYPES = (
    ('moniter', u"Moniter"),
    ('lvs', u"LVS"),
    ('db', u"Database"),
    ('analysis', u"Analysis"),
    ('admin', u"Admin"),
    ('storge', u"Storge"),
    ('web', u"WEB"),
    ('email', u"Email"),
    ('mix', u"Mix"),
)

BYTES_TO_MILLION = 1024000

# class Province(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

# class City(models.Model):
#     name = models.CharField(max_length=40)
#     province = models.ForeignKey(Province)

#     def __str__(self):
#         return self.name

# class SelectP(models.Model):
#     province = models.ForeignKey(Province)
#     city = ChainedForeignKey(
#         'City',
#         chained_field="province",
#         chained_model_field="province",
#         show_all=False,
#         auto_choose=True,
#         help_text='Location aaa',
#     )
    # city = models.ForeignKey(City)

# class Country(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
# class State(models.Model):
#     name = models.CharField(max_length=50)
#     country = models.ForeignKey(Country)
#
#     def __str__(self):
#         return self.name
#
#
# class City1(models.Model):
#     name = models.CharField(max_length=50)
#     state = models.ForeignKey(State)
#
#     def __str__(self):
#         return self.name
#
#
# class Address(models.Model):
#     country = models.ForeignKey(Country)
#     state = models.ForeignKey(State)
#     city = models.ForeignKey(City1)
#     street = models.CharField(max_length=100)
#     zip = models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.street
#
# @python_2_unicode_compatible
# class IDC(models.Model):
#     name = models.CharField(max_length=64)
#     description = models.TextField()
#
#     contact = models.CharField(max_length=32)
#     telphone = models.CharField(max_length=32)
#     address = models.CharField(max_length=128)
#     customer_id = models.CharField(max_length=128)
#     groups = models.ManyToManyField(Group)  # many
#
#     create_time = models.DateField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = u"IDC"
#         verbose_name_plural = verbose_name
#
# @python_2_unicode_compatible
# class Host(models.Model):
#     idc = models.ForeignKey(IDC)
#     name = models.CharField(max_length=64)
#     nagios_name = models.CharField(u"Nagios Host ID", max_length=64, blank=True, null=True)
#     ip = models.GenericIPAddressField(blank=True, null=True)
#     internal_ip = models.GenericIPAddressField(blank=True, null=True)
#     user = models.CharField(max_length=64)
#     password = models.CharField(max_length=128)
#     ssh_port = models.IntegerField(blank=True, null=True)
#     status = models.SmallIntegerField(choices=SERVER_STATUS)
#
#     brand = models.CharField(max_length=64, choices=[(i, i) for i in (u"DELL", u"HP", u"Other")])
#     model = models.CharField(max_length=64)
#     cpu = models.CharField(max_length=64)
#     core_num = models.SmallIntegerField(choices=[(i * 2, "%s Cores" % (i * 2)) for i in range(1, 15)])
#     hard_disk = models.IntegerField()
#     memory = models.IntegerField()
#
#     system = models.CharField(u"System OS", max_length=32, choices=[(i, i) for i in (u"CentOS", u"FreeBSD", u"Ubuntu")])
#     system_version = models.CharField(max_length=32)
#     system_arch = models.CharField(max_length=32, choices=[(i, i) for i in (u"x86_64", u"i386")])
#
#     create_time = models.DateField()
#     guarantee_date = models.DateField()
#     service_type = models.CharField(max_length=32, choices=SERVICE_TYPES)
#     description = models.TextField()
#
#     administrator = models.ForeignKey(AUTH_USER_MODEL, verbose_name="Admin")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = u"Host"
#         verbose_name_plural = verbose_name
#
#
# @python_2_unicode_compatible
# class MaintainLog(models.Model):
#     host = models.ForeignKey(Host)
#     maintain_type = models.CharField(max_length=32)
#     hard_type = models.CharField(max_length=16)
#     time = models.DateTimeField()
#     operator = models.CharField(max_length=16)
#     note = models.TextField()
#
#     def __str__(self):
#         return '%s maintain-log [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
#                                                self.maintain_type, self.hard_type)
#
#     class Meta:
#         verbose_name = u"Maintain Log"
#         verbose_name_plural = verbose_name


class Customer(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=120, verbose_name='Name', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='User')
    release = models.ForeignKey(Release, on_delete=models.CASCADE, verbose_name='Release')

    hardwareModel = models.ForeignKey(HardwareModel, on_delete=models.CASCADE, verbose_name='Hardware Model')

    customer = models.ForeignKey(Customer, verbose_name='Customer')
    version = models.IntegerField(default=1, verbose_name='Version')
    createTime = models.TimeField(auto_now=True, verbose_name='Create Time')

    comment = models.TextField(default='', verbose_name='Comment', blank=True)

    database_type = models.ForeignKey(DBMode, verbose_name='Database Type')

    def __str__(self):
        # return u'%(hardwareType)s %(hardwareModel)s' % {
        #     'hardwareType': self.hardwareType,
        #     'hardwareModel': self.hardwareModel,
        # }
        return self.name

    @property
    def hardwareType(self):
        return self.hardwareModel.hardwareType

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Project'


class WorkingProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name


class CurrentProjectInformationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return ProjectInformation.objects.none()

class ProjectInformation(models.Model):
    NDB_DEPLOY_OPTION = (('individual', 'Individual'), ('combo', 'Combo'))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    vmType = models.ForeignKey(VMType, on_delete=models.CASCADE, verbose_name='VM Type')
    cpuNumber = models.ForeignKey(CPUList, verbose_name='CPU Number',)

    memory = models.ForeignKey(MemoryList, verbose_name='Memory')
    clientNumber = models.IntegerField(verbose_name='Client Number')

    sigtranLinkSpeed = models.IntegerField(verbose_name='SIGTRAN Link Speed')
    sigtranLinkNumber = models.IntegerField(verbose_name='SIGTRAN Link Number')
    sigtranPortUtil = models.FloatField(verbose_name='SIGTRAN Port Utility')

    amaRecordPerBillingBlock = models.FloatField(default=1, verbose_name='AMA Record Number per Billing Block')
    numberReleaseToEstimate = models.IntegerField(default=0, verbose_name='Number of Release to Estimate')
    cpuImpactPerRelease = models.FloatField(default=0.05, verbose_name='CPU Impact per Release')
    memoryImpactPerRelease = models.FloatField(default=0.1, verbose_name='Memory Impact per Release')
    dbImpactPerRelease = models.FloatField(default=0.1, verbose_name='DB Impact per Release')
    deploy_option=models.CharField(max_length=16, choices=NDB_DEPLOY_OPTION, default='combo',
                                   verbose_name='NDB Deploy Option')

    averageAMARecordPerCall = models.FloatField(verbose_name='Average AMA Record per Call')
    amaStoreDay = models.FloatField(verbose_name='AMA Store Days')

    activeSubscriber = models.IntegerField(verbose_name='Active Subscriber')
    inactiveSubscriber = models.IntegerField(verbose_name='Inactive Subscriber')
    groupAccountNumber = models.IntegerField(verbose_name='Number of Group Account')

    cpuUsageTuning = models.ForeignKey(CPUTuning, on_delete=models.CASCADE, verbose_name='CPU Usage Tuning')
    memoryUsageTuning = models.ForeignKey(MemoryUsageTuning, on_delete=models.CASCADE,
                                          verbose_name='Memory Usage Tuning')

    objects = models.Manager() # The default manager.
    current_objects = CurrentProjectInformationManager() # The project-specific manager.

    def __str__(self):
        return self.project.name

    name = property(__str__)

    class Meta:
        verbose_name = 'Project General Information'
        verbose_name_plural = 'Project General Information'


class CurrentTrafficInformationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return TrafficInformation.objects.none()


class TrafficInformation(models.Model):
    DIAMETER_SESSION_TYPE = (('Volume', 'Volume Based Charging'), ('Time', 'Time Based Charging'))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    callType = models.ForeignKey(CallType, on_delete=models.CASCADE, verbose_name='Call Type')

    activeSubscriber = models.IntegerField(verbose_name='Active Subscriber') # Need to set default=project.activeSubscriber
    inactiveSubscriber = models.IntegerField(verbose_name='Inctive Subscriber') # Need to set default=project.inactiveSubscriber

    trafficBHTA = models.FloatField(verbose_name='BHCA/BHTA', default=0)
    trafficTPS = models.FloatField(verbose_name='CPS/TPS', default=0)
    callHoldingTime = models.IntegerField(verbose_name='Call Holding Time', default=0)

    # Parameter for diameter session call
    averageActiveSessionPerSubscriber = models.FloatField(default=0)
    averageCategoryPerCCR = models.FloatField(default=1)
    averageCategoryPerSession = models.FloatField(default=1)
    volumeCCRiBHTA = models.FloatField(default=0)
    volumeCCRuBHTA = models.FloatField(default=0)
    volumeCCRtBHTA = models.FloatField(default=0)
    timeCCRiBHTA = models.FloatField(default=0)
    timeCCRuBHTA = models.FloatField(default=0)
    timeCCRtBHTA = models.FloatField(default=0)

    serverCPUCost = models.FloatField(default=0)
    cpuCostPerCall = models.FloatField(default=0)
    totalCPUCost = models.FloatField(default=0)
    ss7CPUCost = models.FloatField(default=0)
    tcpCPUCost = models.FloatField(default=0)
    aprocCPUCost = models.FloatField(default=0)     # APROC
    asCPUCost = models.FloatField(default=0)        # Aerospike Server

    ss7InSizePerSecond = models.FloatField(default=0)
    ss7OutSizePerSecond = models.FloatField(default=0)
    ldapSizePerSecond = models.FloatField(default=0)
    diameterSizePerSecond = models.FloatField(default=0)
    muTCPSize = models.FloatField(default=0)    # Mate update Size
    featureLDAPSize = models.FloatField(default=0)
    featureDiameterSize = models.FloatField(default=0)

    ndbCPULimitation = models.FloatField(default=0)

    featureCost = models.FloatField(default=0)
    counterCost = models.FloatField(default=0)

    objects = models.Manager() # The default manager.
    current_objects = CurrentTrafficInformationManager() # The project-specific manager.

    @property
    def feature_call_type_config_list(self):
        return FeatureCallTypeConfiguration.objects.all().filter(
            callType=self.callType,
        )

    @property
    def feature_list(self):
        return FeatureConfiguration.current_objects.all()

    def get_feature_cost(self):
        feature_total_cost = 0

        call_cost = self.get_call_cost()
        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                feature_total_cost += feature.featurePenetration * ((feature_cpu_impact[0].ccImpactCPUPercentage +
                                    feature_cpu_impact[0].reImpactCPUPercentage) *
                                    feature_call_type_conf[0].featureApplicable * call_cost +
                                    (feature_cpu_impact[0].ccImpactCPUTime + feature_cpu_impact[0].reImpactCPUTime))

        return feature_total_cost

    def get_feature_ss7_in_size(self):
        feature_ss7_in_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_ss7_in_size += penetration * feature.ss7_in_size

        return feature_ss7_in_size

    def get_feature_ss7_out_size(self):
        feature_ss7_out_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_ss7_out_size += penetration * feature.ss7_out_size

        return feature_ss7_out_size

    def get_feature_ldap_size(self):
        feature_ldap_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_ldap_size += penetration * feature.ldap_message_size

        return feature_ldap_size

    def get_feature_diameter_size(self):
        feature_diameter_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_diameter_size += penetration * feature.diameter_message_size
        return feature_diameter_size

    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = TrafficInformation.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(callType=self.callType).exists():
                raise ValidationError('Call Type: %s existed!'%self.callType)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(TrafficInformation, self).save(*args, **kwargs)

    def get_tps(self):
        return self.activeSubscriber * self.trafficBHTA / 3600

    def get_bhca(self):
        return self.trafficBHTA * 3600 / self.activeSubscriber if self.activeSubscriber > 0 else 0

    def get_default_active_subscriber(self):
        return self.project.activeSubscriber

    def get_default_inactive_subscriber(self):
        return self.project.inactiveSubscriber

    def __str__(self):
        return self.project.name + '_' + self.callType.name

    def get_call_cost(self):
        # get call cost list for current call type and release
        call_cost_orig_list = CallCost.objects.all().filter(
            callType=self.callType,
            release=self.project.release,
        )

        if call_cost_orig_list.count() > 0:
            call_cost_list = call_cost_orig_list.filter(
                hardwareModel=self.project.hardwareModel,
                dbMode=self.project.database_type,
            )

            if call_cost_list.count() > 0:    # exact match
                return call_cost_list[0].callCost * call_cost_list[0].hardwareModel.cpu.singleThreadCapacity

            call_cost_list = call_cost_orig_list.filter(
                hardwareModel=self.project.hardwareModel,
            )
            if call_cost_list.count() > 0:    # Database type not match
                cost_ratio = 1
                if GlobalConfiguration.objects.all().count() > 0:
                    if call_cost_list[0].dbMode.name == 'RTDB':    # RTDB cost --> NDB cost
                        cost_ratio = GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio
                    else:       # NDB cost --> RTDB cost
                        if GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio > 0:
                            cost_ratio = 1 / GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio
                return call_cost_list[0].callCost * call_cost_list[0].hardwareModel.cpu.singleThreadCapacity * cost_ratio

            call_cost_list = call_cost_orig_list.filter(
                dbMode=self.project.database_type,
            )
            call_cost = 0
            call_cost_priority = 0
            if call_cost_list.count() > 0:
                for call_cost_object in call_cost_list:
                    if call_cost_object.hardwareModel.hardwareType == self.project.hardwareModel.hardwareType:
                        call_cost = call_cost_object.callCost * call_cost_object.hardwareModel.cpu.singleThreadCapacity
                        call_cost_priority = 3
                    elif call_cost_object.hardwareModel.cpu == self.project.hardwareModel.cpu:
                        if (call_cost == 0) or (call_cost_priority < 2):
                            call_cost_priority = 2
                            call_cost = call_cost_object.callCost * call_cost_object.hardwareModel.cpu.singleThreadCapacity
                    else:
                        if call_cost == 0:
                            call_cost_priority = 1
                            call_cost = call_cost_object.callCost * call_cost_object.hardwareModel.cpu.singleThreadCapacity

                return call_cost
        else:
            raise ValidationError('Call Cost for Call Type: %s of Release %s not configured!'
                                  %(self.callType, self.project.release))

    def get_total_cost(self):
        return self.get_call_cost() + self.get_feature_cost()

    name = property(__str__)

    class Meta:
        # db_table = 'Traffic Information'
        unique_together = ("project", "callType")


class CurrentFeatureConfigurationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return FeatureConfiguration.objects.none()


class FeatureConfiguration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    feature = models.ForeignKey(FeatureName, on_delete=models.CASCADE, verbose_name='Feature Name')
    featurePenetration = models.FloatField(default=0, verbose_name='Feature Penetration (%)')

    # For online hierarchy feature
    colocateMemberGroup = models.BooleanField(default=True)
    rtdbSolution = models.BooleanField(default=True)
    groupNumber = models.FloatField(default=1)
    ratioOfLevel1 = models.FloatField(default=1)

    objects = models.Manager() # The default manager.
    current_objects = CurrentFeatureConfigurationManager() # The current project specific manager.


    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = FeatureConfiguration.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(feature=self.feature).exists():
                raise ValidationError('Feature Name: %s existed!'%self.feature)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(FeatureConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return self.project.name + "_" + self.feature.name

    @property
    def feature_cpu_impact(self):
        feature_cpu_impact_list = FeatureCPUImpact.objects.all().filter(
            featureName=self.feature
        )
        if feature_cpu_impact_list.count() > 0:
            return feature_cpu_impact_list[0]
        return None

    @property
    def ss7_in_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ss7In
        return 0

    @property
    def ss7_out_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ss7Out
        return 0

    @property
    def ldap_message_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ldapMessageSize
        return 0

    @property
    def diameter_message_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.diameterMessageSize
        return 0

    @property
    def cpu_time(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ccImpactCPUTime + self.feature_cpu_impact.reImpactCPUTime
        return 0

    def cpu_percentage(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ccImpactCPUPercentage + self.feature_cpu_impact.reImpactCPUPercentage
        return 0

    name = property(__str__)

    class Meta:
        unique_together = (("project", "feature"),)


class CurrentDBConfigurationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return DBConfiguration.objects.none()


class DBConfiguration(models.Model):
    MEMBER_GROUP_OPTION = (('Member', 'Member'), ('Group', 'Group'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dbInfo = models.ForeignKey(DBInformation, on_delete=models.CASCADE, verbose_name='DB Name')

    dbFactor = models.FloatField(default=0, verbose_name='DB Factor')
    placeholderRatio = models.FloatField(default=0, verbose_name='Placeholder Ratio (%)')
    memberGroupOption = models.CharField(max_length=10, choices=MEMBER_GROUP_OPTION,
                                         default='member', verbose_name='DB Option')

    recordSize = models.IntegerField(default=0)
    subscriberNumber = models.IntegerField(default=0)
    recordNumber = models.IntegerField(default=0)
    cacheSize = models.IntegerField(default=0)
    todoLogSize = models.IntegerField(default=0)
    mateLogSize = models.IntegerField(default=0)
    referencePlaceholderRatio = models.IntegerField(default=0)
    referenceDBFactor = models.IntegerField(default=0)

    objects = models.Manager() # The default manager.
    current_objects = CurrentDBConfigurationManager() # The current project specific manager.

    def get_record_size(self):
        return self.dbInfo.recordSize

    def get_subscriber_number(self):
        if WorkingProject.objects.all().count() > 0:
            if self.memberGroupOption == 'Member':
                return ProjectInformation.objects.all().filter(
                    project=WorkingProject.objects.all()[0].project)[0].activeSubscriber
            else:
                return ProjectInformation.objects.all().filter(
                    project=WorkingProject.objects.all()[0].project)[0].groupAccountNumber
        else:
            return 0

    def get_record_number(self):
        return math.ceil(self.subscriberNumber * self.dbFactor)

    def get_rtdb_node_size(self):
        rproc_number = 8

        if self.get_record_number() <= 0:
            node_size = 0
        else:
            kpn = 20
            factor = 1.5
            # Factor = 1

            # Fix 40 bytes overhead and 8 byte per slot
            per_node_size = 44 + kpn * 8

            index_number = self.dbInfo.db.prefixTableIndexNumber
            if index_number < 0:
                index_number = 0
            elif index_number > 4:
                index_number = 4

            total_nodes = math.ceil(self.get_record_number() * 1.2 / rproc_number / kpn)
            tree_level = math.ceil(math.log2(total_nodes))
            node_size = math.ceil(math.pow(tree_level, 2) / BYTES_TO_MILLION * per_node_size * factor) * rproc_number * index_number

        return node_size

    def get_ndb_node_size(self):
        record_number = self.get_record_number()
        r = math.ceil(record_number / 18)
        index_number = self.dbInfo.db.prefixTableIndexNumber

        ndb_node_size = math.ceil(record_number / BYTES_TO_MILLION * 64 * 2 +
                                (record_number * 3 + 2 * r) / BYTES_TO_MILLION * 28.44 * index_number)

        return ndb_node_size

    def get_node_size(self):
        if self.dbInfo.db.name == 'RTDB':
            return self.get_rtdb_node_size()
        else:
            return self.get_ndb_node_size()

    def get_cache_size(self):
        if self.dbInfo.db.name == 'RTDB':
            db_overhead = self.dbInfo.db.rtdbOverhead
        else:
            db_overhead = 1

        return math.ceil(self.recordSize * self.recordNumber * db_overhead *
                         (1 - self.placeholderRatio) / BYTES_TO_MILLION) + \
               self.get_node_size()

    def get_todo_log_size(self, dbBladeNeeded, traffic):
        if self.dbInfo.db.name == 'NDB':
            return 0
        cache_size = self.get_cache_size()
        rproc_number = math.ceil(cache_size / 2000, dbBladeNeeded)
        impact_size = self.dbInfo.db.todoLogSize

        todo_log_size = math.ceil(impact_size * traffic * 3600 * 24 * 2 / BYTES_TO_MILLION / 10) * 10

        if todo_log_size > (1000 * 2 * rproc_number):
            return 1000 * 2 * rproc_number
        else:
            return todo_log_size

    def get_mate_log_size(self, traffic):
        global_configuration = GlobalConfiguration.objects.all()
        if global_configuration.count() > 0:
            maintanance_window_hour = global_configuration[0].maintananceWindowHour
            traffic_percentage_under_maitanance_window = global_configuration[0].trafficPercentageUnderMaitananceWindow
        else:
            maintanance_window_hour = 10
            traffic_percentage_under_maitanance_window = 1

        impact_size = self.dbInfo.db.mateLogSize

        b = 3600 * maintanance_window_hour * traffic_percentage_under_maitanance_window / BYTES_TO_MILLION
        return math.ceil(impact_size * traffic * b / 10) * 10

    def get_ndb_reference_placeholder_ratio(self):
        return self.dbInfo.db.ndbRefPlaceholderRatio

    def get_reference_db_factor(self):
        if WorkingProject.objects.all().count() > 0:
            featureList = FeatureConfiguration.objects.all().filter(
                project=WorkingProject.objects.all()[0].project,
            )

            if featureList.count() == 0:
                return 0
        else:
            return 0

        featureDBImpactList = FeatureDBImpact.objects.all().filter(
            dbName=self.dbInfo.db,
        )
        if featureDBImpactList.count() == 0:
            return 0

        referenceDBFactor = 0
        for feature in featureList:
            featureDBImpact = featureDBImpactList.filter(
                featureName=feature.feature,
            )

            if featureDBImpact.count() > 0:
                if self.memberGroupOption == 'Member':
                    referenceDBFactor += feature.featurePenetration * featureDBImpact[0].memberImpactFactor
                else:
                    referenceDBFactor += feature.featurePenetration * featureDBImpact[0].groupImpactFactor

        if self.memberGroupOption == 'Member':
            referenceDBFactor += self.dbInfo.db.defaultMemberFactor
            counterConfiguration = CounterConfiguration.objects.all().filter(
                project=self.project,
            )
            if counterConfiguration.count() > 0:
                referenceDBFactor += (math.ceil(counterConfiguration[0].total_bundle_number() / 6) +
                                      math.ceil(counterConfiguration[0].get_total_counter() / 6)) * \
                                     self.dbInfo.db.defaultMemberCounterFactor
        else:
            referenceDBFactor += self.dbInfo.db.defaultGroupFactor
            counterConfiguration = CounterConfiguration.objects.all().filter(
                project=self.project,
            )
            if counterConfiguration.count() > 0:
                referenceDBFactor += (math.ceil(counterConfiguration[0].groupBucketNumber / 6) +
                                      math.ceil(counterConfiguration[0].groupBundleNumber / 6)) * \
                                     self.dbInfo.db.defaultGroupCounterFactor
        return referenceDBFactor

    def __str__(self):
        return self.project.name + "_" + self.dbInfo.db.name

    name = property(__str__)


'''
    Define counter configuration for the project.
    Need to calculate the db impact for CTRTDB.
'''
class CurrentCounterConfigurationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return CounterConfiguration.objects.none()


class CounterConfiguration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    averageBundleNumberPerSubscriber = models.FloatField(
        default=0,
        verbose_name='Number of Bundle',
    )
    average24hBundleNumberPerSubscriber = models.FloatField(
        default=0,
        verbose_name='Number of 24h Bundle',
    )
    nonAppliedBucketNumber = models.FloatField(
        default=0,
        verbose_name='Non Applied Bucket Number',
    )
    nonAppliedUBDNumber = models.FloatField(
        default=0,
        verbose_name='Non Applied UBD Number',
    )
    appliedBucketNumber = models.FloatField(
        default=0,
        verbose_name='Applied Bucket Number',
    )
    appliedUBDNumber = models.FloatField(
        default=0,
        verbose_name='Applied UBD Number',
    )
    groupBundleNumber = models.FloatField(
        default=0,
        verbose_name='Number of Group Bundle',
    )
    groupBucketNumber = models.FloatField(
        default=0,
        verbose_name='Group Bucket Number',
    )

    generateMultipleAMAForCounter = models.BooleanField(
        default=False,
        verbose_name='Generate Multiple AMA For Counter',
    )
    turnOnBasicCriteriaCheck = models.BooleanField(
        default=False,
        verbose_name='Enable Basic Criteria Check',
    )
    configureForCallType = models.BooleanField(
        default=False,
        verbose_name='Configure Counter For Call Types',
    )

    objects = models.Manager() # The default manager.
    current_objects = CurrentCounterConfigurationManager() # The current project specific manager.

    @property
    def total_bundle_number(self):
        return self.averageBundleNumberPerSubscriber + self.average24hBundleNumberPerSubscriber

    @property
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
            self.appliedBucketNumber + self.appliedUBDNumber

    @property
    def total_group_counter_number(self):
        return self.groupBundleNumber + self.groupBucketNumber

    def __str__(self):
        return self.project.name

    name = property(__str__)

    class Meta:
        verbose_name = 'Counter Configuration'
        verbose_name_plural = 'Counter Configuration'

    def get_total_counter(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + self.appliedBucketNumber + self.appliedUBDNumber


class CurrentCallTypeCounterConfigurationManager(models.Manager):
    def create_call_type_counter_configuration(
            self, project, callType, averageBundleNumberPerSubscriber,average24hBundleNumberPerSubscriber,
            nonAppliedBucketNumber, nonAppliedUBDNumber, appliedBucketNumber, appliedUBDNumber):
        callTypeCounterConfiguration = self.create(
            project = project,
            callType = callType,
            average24hBundleNumberPerSubscriber=average24hBundleNumberPerSubscriber,
            averageBundleNumberPerSubscriber = averageBundleNumberPerSubscriber,
            nonAppliedUBDNumber = nonAppliedUBDNumber,
            nonAppliedBucketNumber = nonAppliedBucketNumber,
            appliedUBDNumber = appliedUBDNumber,
            appliedBucketNumber = appliedBucketNumber,
        )
        return callTypeCounterConfiguration

    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return CounterConfiguration.objects.none()


class CallTypeCounterConfiguration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    callType = models.ForeignKey(CallType, on_delete=models.CASCADE)

    averageBundleNumberPerSubscriber = models.FloatField(
        default=0,
        verbose_name='Number of Bundle',
    )
    average24hBundleNumberPerSubscriber = models.FloatField(
        default=0,
        verbose_name='Number of 24h Bundle',
    )
    nonAppliedBucketNumber = models.FloatField(
        default=0,
        verbose_name='Non Applied Bucket Number',
    )
    nonAppliedUBDNumber = models.FloatField(
        default=0,
        verbose_name='Non Applied UBD Number',
    )
    appliedBucketNumber = models.FloatField(
        default=0,
        verbose_name='Applied Bucket Number',
    )
    appliedUBDNumber = models.FloatField(
        default=0,
        verbose_name='Applied UBD Number',
    )

    objects = models.Manager() # The default manager.
    current_objects = CurrentCallTypeCounterConfigurationManager() # The current project specific manager.

    @property
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
               self.appliedBucketNumber + self.appliedUBDNumber

    @property
    def total_bundle_number(self):
        return self.averageBundleNumberPerSubscriber + self.average24hBundleNumberPerSubscriber

    @property
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
               self.appliedBucketNumber + self.appliedUBDNumber

    class Meta:
        verbose_name = 'Counter Configuration For Call Type'
        verbose_name_plural = 'Counter Configuration For Call Type'

    def __str__(self):
        return self.callType.name

    name = property(__str__)

    def get_counter_cpu_impact(self):
        pass

    def get_multiple_ama_number(self):
        pass

    def get_multiple_ama_impact(self):
        pass

    def get_total_cpu_impact(self):
        pass
        #return getCounterCPUImpact() + getMultipleAMANumber() + getMultipleAMAImpact()

    def get_counter_cost_record(self):
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project
            counterCostList = CounterCost.objects.all().filter(
                release=project.release,
                hardwareModel=project.hardwareModel,
            )
            if counterCostList.count() > 0:
                return counterCostList[0]

            counterCostList = CounterCost.objects.order_by('-release__sequence')
            if counterCostList.count() > 0:
                release = counterCostList[0].release
                counterCostList0 = counterCostList.filter(
                    release=release,
                    hardwareModel=project.hardwareModel,
                )
                if counterCostList0.count() > 0:
                    return counterCostList0[0]

                counterCostList0 = counterCostList.filter(
                    release=release,
                )
                if counterCostList0.count() > 0:
                    for counterCost in counterCostList0:
                        if counterCost.hardwareModel.hardwareType == project.hardwareModel.hardwareType:
                            return counterCost

                    return counterCostList0[0]

                return None
        else:
            return None

    def get_counter_cost(self):
        counterCostRecord = self.get_counter_cost_record()

        if not counterCostRecord:
            return 0

        if GlobalConfiguration.objects.all().count() > 0:
            releaseCountCPUImpact = GlobalConfiguration.objects.all()[0].releaseCountCPUImpact
        else:
            releaseCountCPUImpact = 0.05

        releaseGap = 0
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project

            releaseGap = project.release.sequence - counterCostRecord.release.sequence

            if releaseGap < 0:
                releaseGap = 0

        releaseImpact = math.pow((1 + releaseCountCPUImpact), releaseGap)

        counterConfigurationList = CounterConfiguration.objects.all().filter(
            project=self.project,
        )

        if counterConfigurationList.count() > 0:
            counterConfiguration = counterConfigurationList[0]
        else:
            return 0

        if counterConfiguration.turnOnBasicCriteriaCheck:
            cpuPerNonappliedCounter = counterCostRecord.costPerUnappliedCounterWithBasicCriteria
            cpuPerNonappliedUBD = counterCostRecord.costPerUnappliedCounterWithBasicCriteria
            totalUsedUBDNumber = self.appliedUBDNumber
            totalUsedBucketNumber = self.appliedBucketNumber

            nonappliedCounterOverhead = counterCostRecord.costCounterNumberImpact / 4
        else:
            cpuPerNonappliedCounter = 0
            cpuPerNonappliedUBD = 0
            nonappliedCounterOverhead = 0
            totalUsedUBDNumber = self.appliedUBDNumber + self.nonAppliedUBDNumber
            totalUsedBucketNumber = self.appliedBucketNumber + self.nonAppliedBucketNumber

        totalCounterNumber = self.appliedUBDNumber + self.nonAppliedUBDNumber + \
                             self.appliedBucketNumber + self.nonAppliedBucketNumber

        cpuImpact = 0
        if self.nonAppliedBucketNumber > 0:     # need to include overhead for non-applied bucket
            cpuImpact = cpuImpact + nonappliedCounterOverhead + cpuPerNonappliedCounter * self.nonAppliedBucketNumber

        if self.nonAppliedUBDNumber > 0:    # need to include overhead for non-applied UBD
            cpuImpact = cpuImpact + nonappliedCounterOverhead + cpuPerNonappliedUBD * self.nonAppliedUBDNumber

        if self.appliedBucketNumber > 0:    # need to include overhead for bucket
            cpuImpact = cpuImpact + counterCostRecord.costTurnOnbucket + \
                        self.appliedBucketNumber * counterCostRecord.costPerAppliedBucket

        if self.appliedUBDNumber > 0:   # need to include overhead for UBD
            cpuImpact = cpuImpact + counterCostRecord.costTurnOnUBD + \
                        self.appliedUBDNumber * counterCostRecord.costPerAppliedUBD

        if totalCounterNumber > 0:  # need to include RTDB read/update overhead
            cpuImpact = cpuImpact + math.ceil(totalCounterNumber / counterCostRecord.counterNumberPerRecord) * \
                        counterCostRecord.costDBReadUpdatePerRecord

        if totalUsedUBDNumber > 0:
            cpuImpact = cpuImpact + counterCostRecord.costCounterNumberImpact * \
                        math.pow(1 + counterCostRecord.percentageCounterNumberImpact, totalUsedUBDNumber)

        if totalUsedBucketNumber > 0:
            cpuImpact = cpuImpact + counterCostRecord.costCounterNumberImpact * \
                        math.pow(1 + counterCostRecord.percentageCounterNumberImpact, totalUsedBucketNumber)

        if counterConfiguration.generateMultipleAMAForCounter:  # Multiple AMA
            cpuImpact = cpuImpact + self.project.release.cPUCostForMultipleAMA * math.ceil(totalCounterNumber / 10)

        if self.averageBundleNumberPerSubscriber > 0:
            cpuImpact = cpuImpact + counterCostRecord.costBundlePerRecord * self.averageBundleNumberPerSubscriber

        if self.average24hBundleNumberPerSubscriber > 0:
            cpuImpact = cpuImpact + counterCostRecord.costPer24hBundle * self.average24hBundleNumberPerSubscriber

        return cpuImpact * releaseImpact

    def get_group_counter_cost(self):
        counterCostRecord = self.get_counter_cost_record()

        if not counterCostRecord:
            return 0

        if GlobalConfiguration.objects.all().count() > 0:
            releaseCountCPUImpact = GlobalConfiguration.objects.all()[0].releaseCountCPUImpact
        else:
            releaseCountCPUImpact = 0.05

        releaseGap = 0
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project

            releaseGap = project.release.sequence - counterCostRecord.release.sequence

            if releaseGap < 0:
                releaseGap = 0

        releaseImpact = math.pow((1 + releaseCountCPUImpact), releaseGap)

        counterConfigurationList = CounterConfiguration.objects.all().filter(
            project=self.project,
        )

        if counterConfigurationList.count() > 0:
            counterConfiguration = counterConfigurationList[0]
        else:
            return 0

        totalGroupCounterNumber = counterConfiguration.total_group_counter_number

        cpuImpact = math.ceil(totalGroupCounterNumber / counterCostRecord.counterNumberPerRecord) * \
                    counterCostRecord.costGroupDBReadUpdatePerRecord + counterCostRecord.costTurnOnGroupBucket + \
                    counterCostRecord.costPerGroupSideBucket * totalGroupCounterNumber

        return cpuImpact * releaseImpact

    class Meta:
        verbose_name = 'Counter Configuration for Call Type'
        verbose_name_plural = 'Counter Configuration for Call Type'


class CurrentSystemConfigurationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return SystemConfiguration.objects.none()

    def create_system_configuration(
        self, project, applicationName,
        backupAppNodeNumberPerSystem, spareAppNodeNumberPerSystem,
        backupDBNodeNumberPerSystem, spareDBNodePairNumberPerSystem
    ):
        system_configuration = self.create(
            project=project,
            applicationName=applicationName,
            backupAppNodeNumberPerSystem=backupAppNodeNumberPerSystem,
            spareAppNodeNumberPerSystem=spareAppNodeNumberPerSystem,
            backupDBNodeNumberPerSystem=backupDBNodeNumberPerSystem,
            spareDBNodePairNumberPerSystem=spareDBNodePairNumberPerSystem,
        )
        return system_configuration


class SystemConfiguration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    applicationName = models.ForeignKey(
        ApplicationName,
        on_delete=models.CASCADE,
        verbose_name='Application Name'
    )

    cabinetNumberPerSystem = models.IntegerField(
        default=1,
        verbose_name='Number of Cabinet Per System',
    )
    backupAppNodeNumberPerSystem = models.IntegerField(
        default=0,
        verbose_name='Number of Backup App Node Per System',
    )
    spareAppNodeNumberPerSystem = models.IntegerField(
        default=0,
        verbose_name='Number of Spare App Node Per System',
    )
    backupDBNodeNumberPerSystem = models.IntegerField(
        default=0,
        verbose_name='Number of Backup DB Node Per System',
    )
    spareDBNodePairNumberPerSystem = models.IntegerField(
        default=0,
        verbose_name='Number of Spare DB Node Pair Per System'
    )

    objects = models.Manager() # The default manager.
    current_objects = CurrentSystemConfigurationManager() # The current project specific manager.

    def __str__(self):
        return self.applicationName.name

    name = property(__str__)

    class Meta:
        verbose_name = 'System Configuration'
        verbose_name_plural = 'System Configuration'


DEPLOY_OPTION = (('EPAY Node', 'EPAY Node'), ('DRouter Node', 'DRouter Node'),
                 ('CDR Pre-Processor Node', 'CDR Pre-Processor Node'),
                 ('eCGS Node', 'eCGS Node'), ('NTGW Node', 'NTGW Node'),
                 ('eCTRL Node', 'eCTRL Node'), ('EPPSM Node', 'EPPSM Node'),
                 ('GRouter Node', 'GRouter Node'),
                 )


class CurrentApplicationConfigurationManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return ApplicationConfiguration.objects.none()


class ApplicationConfiguration(models.Model):
    BOUND_TYPE_OPTION = (('CPU Bound', 'CPU Bound'), ('Memory Bound', 'Memory Bound'))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    applicationName = models.ForeignKey(
        ApplicationName,
        on_delete=models.CASCADE,
        verbose_name='Application Name'
    )

    deployOption = models.CharField(
        max_length=30,
        choices=DEPLOY_OPTION,
        verbose_name='Deploy Option',
    )

    activeSubscriber = models.IntegerField(
        default=0,
        verbose_name='Active Subscriber',
    )   # Need to set default=project.activeSubscriber

    inactiveSubscriber = models.IntegerField(
        default=0,
        verbose_name='Inctive Subscriber',
    )   # Need to set default=project.inactiveSubscriber

    trafficTPS = models.FloatField(
        verbose_name='CPS/TPS',
        default=0,
    )

    serverCPUCost = models.FloatField(default=0)
    clientCPUCost = models.FloatField(default=0)
    totalCPUCost = models.FloatField(default=0)
    ss7CPUCost = models.FloatField(default=0)
    tcpCPUCost = models.FloatField(default=0)
    miscCPUCost = models.FloatField(default=0)
    cpuBudget = models.FloatField(default=0)

    ss7InSizePerSecond = models.FloatField(default=0)
    ss7OutSizePerSecond = models.FloatField(default=0)
    ldapSizePerSecond = models.FloatField(default=0)
    diameterSizePerSecond = models.FloatField(default=0)
    muTCPSize = models.FloatField(default=0)    # Mate update Size
    featureLDAPSize = models.FloatField(default=0)
    featureDiameterSize = models.FloatField(default=0)

    memoryUsage = models.FloatField(default=0)
    clientCPUUsagePercentage = models.FloatField(default=0)
    dbCacheSize = models.FloatField(default=0)
    spaTextSize = models.FloatField(default=0)

    amaPerSecond = models.FloatField(default=0)

    cpuBaseNodeNumber = models.FloatField(default=0)
    memoryBaseNodeNumber = models.FloatField(default=0)
    ss7BaseNodeNumber = models.FloatField(default=0)
    nodeNumberNeeded = models.FloatField(default=0)

    ndbMateNode = models.FloatField(default=0)
    ndbRoutingNode = models.FloatField(default=0)

    dbNodeNumberNeeded = models.FloatField(default=0)

    ss7BaseIONodeNumber = models.FloatField(default=0)
    ldapBaseIONodeNumber = models.FloatField(default=0)
    diameterBaseIONodeNumber = models.FloatField(default=0)
    ioNodeNumberNeeded = models.FloatField(default=0)

    boundType = models.CharField(max_length=20, choices=BOUND_TYPE_OPTION,
                                 default='CPU Bound', verbose_name='Bound Type')

    objects = models.Manager() # The default manager.
    current_objects = CurrentApplicationConfigurationManager() # The current project specific manager.

    @property
    def current_application_information(self):
        current_application_information_list  = ApplicationInformation.objects.all().filter(
            release=self.project.release,
            application=self.applicationName,
        )
        if current_application_information_list.count() > 0:
            return current_application_information_list[0]

        return None

    @property
    def traffic_information_list(self):
        return TrafficInformation.current_objects.all()

    def get_node_number_needed(self):
        if self.cpuBaseNodeNumber >= self.memoryBaseNodeNumber:
            self.nodeNumberNeeded = self.cpuBaseNodeNumber
            self.boundType = 'CPU Bound'
        else:
            self.nodeNumberNeeded = self.memoryBaseNodeNumber
            self.boundType = 'Memory Bound'

    def get_total_client_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic.get_total_cost()

        return total_call_cost

    def get_total_sever_cpu_cost(self):
        if not self.current_application_information:
            total_call_cost = 0

            for traffic in self.traffic_information_list:
                total_call_cost += self.current_application_information.cpuCostForServer * traffic.trafficTPS

            return total_call_cost

        return 0

    def get_tcp_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic.tcpCPUCost

        return total_call_cost

    def get_ss7_cpu_cost(self):
        if not self.current_application_information:
            total_call_cost = 0

            for traffic in self.traffic_information_list:
                total_call_cost += traffic.ss7CPUCost

            return total_call_cost

        return 0

    def get_misc_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic

        return total_call_cost

    def get_total_app_memory(self):
        pass

    def get_total_db_cache_size(self):
        pass

    def get_total_ama_disk_size(self):
        pass

    def get_total_db_disk_size(self):
        pass

    def get_ama_record_per_second(self):
        pass

    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = ApplicationConfiguration.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(applicationName=self.applicationName).exists():
                raise ValidationError('Application: %s existed!'%self.applicationName)

    class Meta:
        verbose_name = 'Application Configuration'
        verbose_name_plural = 'Application Configuration'


class CurrentCalculatedResultanager(models.Manager):
    def create_calculated_result(
            self, project, applicationName, appNodeNumber,
            dbNodeNumber, ioNodeNumber, ):
        calculatedResult = self.create(
            project = project,
            applicationName = applicationName,
            appNodeNumber = appNodeNumber,
            dbNodeNumber = dbNodeNumber,
            ioNodeNumber = ioNodeNumber,
        )
        return calculatedResult

    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return CalculatedResult.objects.none()

class CalculatedResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    applicationName = models.ForeignKey(
        ApplicationName,
        on_delete=models.CASCADE,
        verbose_name='Application Name'
    )

    appNodeNumber = models.IntegerField(default=0)
    dbNodeNumber = models.IntegerField(default=0)
    ioNodeNumber = models.IntegerField(default=0)

    objects = models.Manager() # The default manager.
    current_objects = CurrentCalculatedResultanager() # The current project specific manager.

    class Meta:
        verbose_name = 'Calculated Result'
        verbose_name_plural = 'Calculated Result'


class CurrentDimensioningResultManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return DimensioningResult.objects.none()


class DimensioningResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    applicationName = models.ForeignKey(
        ApplicationName,
        on_delete=models.CASCADE,
        verbose_name='Application Name'
    )

    systemNumber = models.IntegerField(default=0)
    appNodeNeededNumber = models.IntegerField(default=0)
    dbNodeNeededNumber = models.IntegerField(default=0)
    ioNodeNeededNumber = models.IntegerField(default=0)
    pilotNodeNeededNumber = models.IntegerField(default=0)
    totalNodeNeededNumber = models.IntegerField(default=0)

    averageClientCPUUsage = models.FloatField(default=0)
    dbCacheSize = models.FloatField(default=0)     # MB
    totalMemoryUsage = models.FloatField(default=0)     # MB
    sigtranSpeed = models.FloatField(default=0)    # Byte/Second
    ethernetPortsRequiredNumber = models.IntegerField(default=0)
    totalTCPUDPSpeed = models.FloatField(default=0)    # Byte/Second
    amaRecordNumberPerSecond = models.FloatField(default=0)
    dialyBillingFileSize = models.FloatField(default=0)     # MB
    amaRetrieveSpeed = models.FloatField(default=0)    # Byte/Second
    ladpDiameterUDP = models.FloatField(default=0)    # Byte/Second
    muSpeed = models.FloatField(default=0)    # Byte/Second

    memoryUsagePerAppNode = models.FloatField(default=0)     # MB
    memoryUsagePerClient = models.FloatField(default=0)     # MB
    appNodeMemoryUsagePercent = models.FloatField(default=0)     # %

    pilotSharedDiskSize = models.FloatField(default=0)     # MB
    dbDiskSizeForMateUpdate = models.FloatField(default=0)     # MB
    diskSizeForDB = models.FloatField(default=0)     # MB

    objects = models.Manager() # The default manager.
    current_objects = CurrentDimensioningResultManager() # The current project specific manager.

    class Meta:
        verbose_name = 'Dimensioning Result'
        verbose_name_plural = 'Dimensioning Result'


class CurrentDimensioningResultPerSystemManager(models.Manager):
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return DimensioningResultPerSystem.objects.none()


class DimensioningResultPerSystem(models.Model):
    dimensioningResult = models.ForeignKey(DimensioningResult, on_delete=models.CASCADE)

    appNodeNumber = models.IntegerField(default=0)
    dbNodeNumber = models.IntegerField(default=0)
    ioNodeNumber = models.IntegerField(default=2)
    pilotNodeNumber = models.IntegerField(default=2)
    totalNodeNumber = models.IntegerField(default=0)

    averageClientCPUUsage = models.FloatField(default=0)
    dbCacheSize = models.FloatField(default=0)     # MB
    totalMemoryUsage = models.FloatField(default=0)     # MB
    sigtranSpeed = models.FloatField(default=0)    # Byte/Second
    totalTCPUDPSpeed = models.FloatField(default=0)    # Byte/Second
    amaRecordNumberPerSecond = models.FloatField(default=0)
    dialyBillingFileSize = models.FloatField(default=0)     # MB
    amaRetrieveSpeed = models.FloatField(default=0)    # Byte/Second
    ladpDiameterUDP = models.FloatField(default=0)    # Byte/Second
    muSpeed = models.FloatField(default=0)    # Byte/Second

    memoryUsagePerAppNode = models.FloatField(default=0)     # MB
    memoryUsagePerClient = models.FloatField(default=0)     # MB
    appNodeMemoryUsagePercent = models.FloatField(default=0)     # %

    pilotSharedDiskSize = models.FloatField(default=0)     # MB
    dbDiskSizeForMateUpdate = models.FloatField(default=0)     # MB
    diskSizeForDB = models.FloatField(default=0)     # MB

    objects = models.Manager() # The default manager.
    current_objects = CurrentDimensioningResultPerSystemManager() # The current project specific manager.


    class Meta:
        verbose_name = 'Dimensioning Result Per System'
        verbose_name_plural = 'Dimensioning Result Per System'