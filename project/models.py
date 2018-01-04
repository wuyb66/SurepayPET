from django.db import models
from django.contrib.auth.models import User
from service.models import Release, CallType, FeatureName, DBInformation, CallCost, \
    ApplicationName, FeatureDBImpact, FeatureCallTypeConfiguration, FeatureCPUImpact, \
    CounterCost, ApplicationInformation
from hardware.models import CPUTuning, MemoryUsageTuning, HardwareModel, VMType, \
    HardwareType, CPU, CPUList, MemoryList
from common.models import DBMode, GlobalConfiguration
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import ValidationError

from common import logger
from common.logger import logged
import sys
import os.path

import math

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
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    cpuNumber = models.ForeignKey(CPUList, verbose_name='CPU Number', )

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
    deploy_option = models.CharField(max_length=16, choices=NDB_DEPLOY_OPTION, default='combo',
                                     verbose_name='NDB Deploy Option')

    averageAMARecordPerCall = models.FloatField(verbose_name='Average AMA Record per Call')
    amaStoreDay = models.FloatField(verbose_name='AMA Store Days')

    activeSubscriber = models.IntegerField(verbose_name='Active Subscriber')
    inactiveSubscriber = models.IntegerField(verbose_name='Inactive Subscriber')
    groupAccountNumber = models.IntegerField(verbose_name='Number of Group Account')

    cpuUsageTuning = models.ForeignKey(CPUTuning, on_delete=models.CASCADE, verbose_name='CPU Usage Tuning')
    memoryUsageTuning = models.ForeignKey(MemoryUsageTuning, on_delete=models.CASCADE,
                                          verbose_name='Memory Usage Tuning')

    objects = models.Manager()  # The default manager.
    current_objects = CurrentProjectInformationManager()  # The project-specific manager.

    def __str__(self):
        return self.project.name

    name = property(__str__)

    class Meta:
        verbose_name = 'Project General Information'
        verbose_name_plural = 'Project General Information'


class CurrentTrafficInformationManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    activeSubscriber = models.IntegerField(
        verbose_name='Active Subscriber')  # Need to set default=project.activeSubscriber
    inactiveSubscriber = models.IntegerField(
        verbose_name='Inactive Subscriber')  # Need to set default=project.inactiveSubscriber

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
    diamCPUCost = models.FloatField(default=0)
    aprocCPUCost = models.FloatField(default=0)  # APROC
    asCPUCost = models.FloatField(default=0)  # Aerospike Server

    spaDataSize = models.IntegerField(default=0)

    ss7InSizePerSecond = models.FloatField(default=0)
    ss7OutSizePerSecond = models.FloatField(default=0)
    ldapSizePerSecond = models.FloatField(default=0)
    diameterSizePerSecond = models.FloatField(default=0)
    muTCPSize = models.FloatField(default=0)  # Mate update Size
    featureSS7InSize = models.FloatField(default=0)
    featureSS7OutSize = models.FloatField(default=0)
    featureLDAPSize = models.FloatField(default=0)
    featureDiameterSize = models.FloatField(default=0)

    ndbCPULimitation = models.FloatField(default=0)

    featureCost = models.FloatField(default=0)
    counterCost = models.FloatField(default=0)
    groupCounterCost = models.FloatField(default=0)

    objects = models.Manager()  # The default manager.
    current_objects = CurrentTrafficInformationManager()  # The project-specific manager.

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def counter_configuration(self):
        counter_configuration_list = CallTypeCounterConfiguration.current_objects.all().filter(
            callType=self.callType
        )
        if counter_configuration_list.count() > 0:
            return counter_configuration_list[0]
        return None

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def application(self):
        application_name_list = ApplicationName.objects.all().filter(
            name='EPAY',
        )

        if application_name_list.count() > 0:
            return application_name_list[0]
        return None

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def application_information(self):
        application_information_list = ApplicationInformation.objects.all().filter(
            release=self.project.release,
            application=self.application,
        )
        if application_information_list.count() > 0:
            return application_information_list[0]
        return None

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_information(self):
        if ProjectInformation.current_objects.all().count() > 0:
            return ProjectInformation.current_objects.all()[0]
        return None

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_call_type_config_list(self):
        return FeatureCallTypeConfiguration.objects.all().filter(
            callType=self.callType,
        )

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_list(self):
        return FeatureConfiguration.current_objects.all()

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_cost(self):
        feature_total_cost = 0

        call_cost = self.get_call_cost()
        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature.feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature.feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                feature_total_cost += feature.featurePenetration * \
                                      ((feature_cpu_impact[0].ccImpactCPUPercentage +
                                        feature_cpu_impact[0].reImpactCPUPercentage) *
                                       feature_call_type_conf[0].featureApplicable * call_cost +
                                       (feature_cpu_impact[0].ccImpactCPUTime +
                                        feature_cpu_impact[0].reImpactCPUTime))

        return feature_total_cost

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_ss7_in_size(self):
        feature_ss7_in_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature.feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature.feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_ss7_in_size += penetration * feature.ss7_in_size

        return feature_ss7_in_size

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_ss7_out_size(self):
        feature_ss7_out_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature.feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature.feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_ss7_out_size += penetration * feature.ss7_out_size

        return feature_ss7_out_size

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_ldap_size(self):
        feature_ldap_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature.feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature.feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_ldap_size += penetration * feature.ldap_message_size

        return feature_ldap_size

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_diameter_size(self):
        feature_diameter_size = 0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature.feature,
            )
            feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                featureName=feature.feature,
            )
            if (feature_call_type_conf.count() > 0) and (feature_cpu_impact.count() > 0):
                penetration = feature.featurePenetration * feature_call_type_conf[0].featureApplicable
                feature_diameter_size += penetration * feature.diameter_message_size
        return feature_diameter_size

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = TrafficInformation.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(callType=self.callType).exists():
                raise ValidationError('Call Type: %s existed!' % self.callType)

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save(self, *args, **kwargs):
        self.validate_unique()
        super(TrafficInformation, self).save(*args, **kwargs)

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps(self):
        return self.activeSubscriber * self.trafficBHTA / 3600

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_bhca(self):
        return self.trafficBHTA * 3600 / self.activeSubscriber if self.activeSubscriber > 0 else 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_default_active_subscriber(self):
        if self.feature_information:
            return self.feature_information.activeSubscriber
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_default_inactive_subscriber(self):
        if self.feature_information:
            return self.feature_information.inactiveSubscriber

    def __str__(self):
        return self.callType.name

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

            if call_cost_list.count() > 0:  # exact match
                return call_cost_list[0].callCost * call_cost_list[0].hardwareModel.cpu.singleThreadCapacity

            call_cost_list = call_cost_orig_list.filter(
                hardwareModel=self.project.hardwareModel,
            )
            if call_cost_list.count() > 0:  # Database type not match
                cost_ratio = 1
                if GlobalConfiguration.objects.all().count() > 0:
                    if call_cost_list[0].dbMode.name == 'RTDB':  # RTDB cost --> NDB cost
                        cost_ratio = GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio
                    else:  # NDB cost --> RTDB cost
                        if GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio > 0:
                            cost_ratio = 1 / GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio
                return call_cost_list[0].callCost * call_cost_list[
                    0].hardwareModel.cpu.singleThreadCapacity * cost_ratio

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
                            call_cost = call_cost_object.callCost * \
                                        call_cost_object.hardwareModel.cpu.singleThreadCapacity
                    else:
                        if call_cost == 0:
                            call_cost_priority = 1
                            call_cost = call_cost_object.callCost * \
                                        call_cost_object.hardwareModel.cpu.singleThreadCapacity

                return call_cost
        else:
            raise ValidationError(
                f'Call Cost for Call Type: {self.callType} of Release {self.project.release} not configured!')

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_cost(self):
        return self.get_call_cost() + self.feature_cost

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_server_cost(self):
        if self.application_information is not None:
            return self.trafficTPS * self.application_information.cpuCostForServer
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tcp_cost(self):
        if (self.application_information is not None) and (self.callType.tcpipNumber > 0):
            logger.g_logger.info('trafficTPS: %s, tcpCost: %s' % (
                self.trafficTPS, self.application_information.tcpCost))
            return self.trafficTPS * self.application_information.tcpCost

        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_diam_cost(self):
        if (self.application_information is not None) and (self.callType.diameterNumber > 0):
            return self.trafficTPS * self.application_information.diamCost
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_cost(self):
        if (self.application_information is not None) and (self.callType.ss7Number > 0):
            return self.trafficTPS * self.application_information.ss7Cost
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_aproc_cost(self):
        if self.application_information is not None:
            return self.trafficTPS * self.application_information.aprocCost
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_as_cost(self):
        if self.application_information is not None:
            return self.trafficTPS * self.application_information.asCost
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_spa_data_size_for_diameter_session(self):
        diameter_cps = self.activeSubscriber * (self.timeCCRiBHTA + self.volumeCCRiBHTA) / 3600
        diameter_session_size = self.project.release.ldapCIPSize + self.project.release.otherCIPSize + \
                                self.project.release.sessionCIPSize * self.averageCategoryPerSession
        if self.averageActiveSessionPerSubscriber > 0:
            return diameter_session_size * self.averageActiveSessionPerSubscriber * \
                   self.activeSubscriber / BYTES_TO_MILLION
        return diameter_session_size * diameter_cps * self.callHoldingTime / BYTES_TO_MILLION

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_spa_data_size(self):
        if self.volumeCCRiBHTA > 0 or self.timeCCRiBHTA > 0:
            return self.get_spa_data_size_for_diameter_session()
        return self.trafficTPS * self.callHoldingTime * self.project.release.callRecordSize

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_in_size(self):
        return self.trafficTPS * self.callType.ss7InSize

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_out_size(self):
        return self.trafficTPS * self.callType.ss7OutSize

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ldap_size(self):
        return self.trafficTPS * self.callType.tcpipSize

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_diameter_size(self):
        return self.trafficTPS * self.callType.diameterSize

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_mu_size(self):
        return self.trafficTPS * self.callType.mateUpdateSize

    # @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate_for_traffic(self):
        self.serverCPUCost = self.get_server_cost()
        self.cpuCostPerCall = self.get_total_cost()
        self.totalCPUCost = self.cpuCostPerCall * self.trafficTPS
        self.ss7CPUCost = self.get_ss7_cost()
        self.tcpCPUCost = self.get_tcp_cost()
        self.diamCPUCost = self.get_diam_cost()
        self.aprocCPUCost = self.get_aproc_cost()
        self.asCPUCost = self.get_as_cost()

        self.spaDataSize = self.get_spa_data_size()

        self.ss7InSizePerSecond = self.get_ss7_in_size()
        self.ss7OutSizePerSecond = self.get_ss7_out_size()
        self.ldapSizePerSecond = self.get_ldap_size()
        self.diameterSizePerSecond = self.get_diameter_size()
        self.muTCPSize = self.get_mu_size()  # Mate update Size
        self.featureSS7InSize = self.feature_ss7_in_size
        self.featureSS7OutSize = self.feature_ss7_out_size
        self.featureLDAPSize = self.feature_ldap_size
        self.featureDiameterSize = self.feature_diameter_size

        self.ndbCPULimitation = self.callType.ndbCPUUsageLimitation

        self.featureCost = self.feature_cost
        if self.counter_configuration is not None:
            self.counterCost = self.counter_configuration.get_counter_cost()
            self.groupCounterCost = self.counter_configuration.get_group_counter_cost()
        else:
            self.counterCost = 0
            self.groupCounterCost = 0

        self.save()

    name = property(__str__)

    class Meta:
        # db_table = 'Traffic Information'
        unique_together = ("project", "callType")


class CurrentFeatureConfigurationManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentFeatureConfigurationManager()  # The current project specific manager.

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = FeatureConfiguration.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(feature=self.feature).exists():
                raise ValidationError('Feature Name: %s existed!' % self.feature)

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save(self, *args, **kwargs):
        self.validate_unique()
        super(FeatureConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return self.project.name + "_" + self.feature.name

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def feature_cpu_impact(self):
        feature_cpu_impact_list = FeatureCPUImpact.objects.all().filter(
            featureName=self.feature
        )
        if feature_cpu_impact_list.count() > 0:
            return feature_cpu_impact_list[0]
        return None

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ss7_in_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ss7In
        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ss7_out_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ss7Out
        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ldap_message_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ldapMessageSize
        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def diameter_message_size(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.diameterMessageSize
        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def cpu_time(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ccImpactCPUTime + self.feature_cpu_impact.reImpactCPUTime
        return 0

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def cpu_percentage(self):
        if self.feature_cpu_impact:
            return self.feature_cpu_impact.ccImpactCPUPercentage + self.feature_cpu_impact.reImpactCPUPercentage
        return 0

    name = property(__str__)

    class Meta:
        unique_together = (("project", "feature"),)


class CurrentDBConfigurationManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentDBConfigurationManager()  # The current project specific manager.

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_record_size(self):
        return self.dbInfo.recordSize

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_record_number(self):
        return math.ceil(self.subscriberNumber * self.dbFactor)

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
            node_size = math.ceil(
                math.pow(tree_level, 2) / BYTES_TO_MILLION * per_node_size * factor) * rproc_number * index_number

        return node_size

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ndb_node_size(self):
        record_number = self.get_record_number()
        r = math.ceil(record_number / 18)
        index_number = self.dbInfo.db.prefixTableIndexNumber

        ndb_node_size = math.ceil(record_number / BYTES_TO_MILLION * 64 * 2 +
                                  (record_number * 3 + 2 * r) / BYTES_TO_MILLION * 28.44 * index_number)

        return ndb_node_size

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_node_size(self):
        if self.dbInfo.db.name == 'RTDB':
            return self.get_rtdb_node_size()
        else:
            return self.get_ndb_node_size()

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_cache_size(self):
        if self.dbInfo.db.name == 'RTDB':
            db_overhead = self.dbInfo.db.rtdbOverhead
        else:
            db_overhead = 1

        return math.ceil(self.recordSize * self.recordNumber * db_overhead *
                         (1 - self.placeholderRatio) / BYTES_TO_MILLION) + self.get_node_size()

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_todo_log_size(self, db_blade_needed, traffic):
        if self.dbInfo.db.name == 'NDB':
            return 0
        cache_size = self.get_cache_size()
        rproc_number = math.ceil(cache_size / 2000, db_blade_needed)
        impact_size = self.dbInfo.db.todoLogSize

        todo_log_size = math.ceil(impact_size * traffic * 3600 * 24 * 2 / BYTES_TO_MILLION / 10) * 10

        if todo_log_size > (1000 * 2 * rproc_number):
            return 1000 * 2 * rproc_number
        else:
            return todo_log_size

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_mate_log_size(self, traffic):
        global_configuration = GlobalConfiguration.objects.all()
        if global_configuration.count() > 0:
            maintenance_window_hour = global_configuration[0].maintananceWindowHour
            traffic_percentage_under_maintenance_window = global_configuration[0].trafficPercentageUnderMaitananceWindow
        else:
            maintenance_window_hour = 10
            traffic_percentage_under_maintenance_window = 1

        impact_size = self.dbInfo.db.mateLogSize

        b = 3600 * maintenance_window_hour * traffic_percentage_under_maintenance_window / BYTES_TO_MILLION
        return math.ceil(impact_size * traffic * b / 10) * 10

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ndb_reference_placeholder_ratio(self):
        return self.dbInfo.db.ndbRefPlaceholderRatio

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def reference_db_factor(self):
        if WorkingProject.objects.all().count() > 0:
            feature_list = FeatureConfiguration.objects.all().filter(
                project=WorkingProject.objects.all()[0].project,
            )

            if feature_list.count() == 0:
                return 0
        else:
            return 0

        feature_db_impact_list = FeatureDBImpact.objects.all().filter(
            dbName=self.dbInfo.db,
        )
        if feature_db_impact_list.count() == 0:
            return 0

        reference_db_factor = 0
        for feature in feature_list:
            feature_db_impact = feature_db_impact_list.filter(
                featureName=feature.feature,
            )

            if feature_db_impact.count() > 0:
                if self.memberGroupOption == 'Member':
                    reference_db_factor += feature.featurePenetration * feature_db_impact[0].memberImpactFactor
                else:
                    reference_db_factor += feature.featurePenetration * feature_db_impact[0].groupImpactFactor

        if self.memberGroupOption == 'Member':
            reference_db_factor += self.dbInfo.db.defaultMemberFactor
            counter_configuration = CounterConfiguration.objects.all().filter(
                project=self.project,
            )
            if counter_configuration.count() > 0:
                reference_db_factor += (math.ceil(counter_configuration[0].total_bundle_number() / 6) +
                                        math.ceil(counter_configuration[0].get_total_counter() / 6)) * \
                                       self.dbInfo.db.defaultMemberCounterFactor
        else:
            reference_db_factor += self.dbInfo.db.defaultGroupFactor
            counter_configuration = CounterConfiguration.objects.all().filter(
                project=self.project,
            )
            if counter_configuration.count() > 0:
                reference_db_factor += (math.ceil(counter_configuration[0].groupBucketNumber / 6) +
                                        math.ceil(counter_configuration[0].groupBundleNumber / 6)) * \
                                       self.dbInfo.db.defaultGroupCounterFactor
        return reference_db_factor

    def __str__(self):
        return self.project.name + "_" + self.dbInfo.db.name

    name = property(__str__)


'''
    Define counter configuration for the project.
    Need to calculate the db impact for CTRTDB.
'''


class CurrentCounterConfigurationManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentCounterConfigurationManager()  # The current project specific manager.

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_bundle_number(self):
        return self.averageBundleNumberPerSubscriber + self.average24hBundleNumberPerSubscriber

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
               self.appliedBucketNumber + self.appliedUBDNumber

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_group_counter_number(self):
        return self.groupBundleNumber + self.groupBucketNumber

    def __str__(self):
        return self.project.name

    name = property(__str__)

    class Meta:
        verbose_name = 'Counter Configuration'
        verbose_name_plural = 'Counter Configuration'

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_counter(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + self.appliedBucketNumber + self.appliedUBDNumber


class CurrentCallTypeCounterConfigurationManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_call_type_counter_configuration(
            self, project, call_type, average_bundle_number_per_subscriber, average_24h_bundle_number_per_subscriber,
            non_applied_bucket_number, non_applied_ubd_number, applied_bucket_number, applied_ubd_number):
        call_type_counter_configuration = self.create(
            project=project,
            callType=call_type,
            average24hBundleNumberPerSubscriber=average_24h_bundle_number_per_subscriber,
            averageBundleNumberPerSubscriber=average_bundle_number_per_subscriber,
            nonAppliedUBDNumber=non_applied_ubd_number,
            nonAppliedBucketNumber=non_applied_bucket_number,
            appliedUBDNumber=applied_ubd_number,
            appliedBucketNumber=applied_bucket_number,
        )
        return call_type_counter_configuration

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentCallTypeCounterConfigurationManager()  # The current project specific manager.

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
               self.appliedBucketNumber + self.appliedUBDNumber

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_bundle_number(self):
        return self.averageBundleNumberPerSubscriber + self.average24hBundleNumberPerSubscriber

    class Meta:
        verbose_name = 'Counter Configuration For Call Type'
        verbose_name_plural = 'Counter Configuration For Call Type'

    def __str__(self):
        return self.callType.name

    name = property(__str__)

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_counter_cpu_impact(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_multiple_ama_number(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_multiple_ama_impact(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_cpu_impact(self):
        pass
        # return getCounterCPUImpact() + getMultipleAMANumber() + getMultipleAMAImpact()

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_counter_cost_record(self):
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project
            counter_cost_list = CounterCost.objects.all().filter(
                release=project.release,
                hardwareModel=project.hardwareModel,
            )
            if counter_cost_list.count() > 0:
                return counter_cost_list[0]

            counter_cost_list = CounterCost.objects.order_by('-release__sequence')
            if counter_cost_list.count() > 0:
                release = counter_cost_list[0].release
                counter_cost_list0 = counter_cost_list.filter(
                    release=release,
                    hardwareModel=project.hardwareModel,
                )
                if counter_cost_list0.count() > 0:
                    return counter_cost_list0[0]

                counter_cost_list0 = counter_cost_list.filter(
                    release=release,
                )
                if counter_cost_list0.count() > 0:
                    for counterCost in counter_cost_list0:
                        if counterCost.hardwareModel.hardwareType == project.hardwareModel.hardwareType:
                            return counterCost

                    return counter_cost_list0[0]

                return None
        else:
            return None

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_counter_cost(self):
        counter_cost_record = self.get_counter_cost_record()

        if counter_cost_record is not None:
            return 0

        if GlobalConfiguration.objects.all().count() > 0:
            release_count_cpu_impact = GlobalConfiguration.objects.all()[0].releaseCountCPUImpact
        else:
            release_count_cpu_impact = 0.05

        release_gap = 0
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project

            release_gap = project.release.sequence - counter_cost_record.release.sequence

            if release_gap < 0:
                release_gap = 0

        release_impact = math.pow((1 + release_count_cpu_impact), release_gap)

        counter_configuration_list = CounterConfiguration.objects.all().filter(
            project=self.project,
        )

        if counter_configuration_list.count() > 0:
            counter_configuration = counter_configuration_list[0]
        else:
            return 0

        if counter_configuration.turnOnBasicCriteriaCheck:
            cpu_per_non_applied_counter = counter_cost_record.costPerUnappliedCounterWithBasicCriteria
            cpu_per_non_applied_ubd = counter_cost_record.costPerUnappliedCounterWithBasicCriteria
            total_used_ubd_number = self.appliedUBDNumber
            total_used_bucket_number = self.appliedBucketNumber

            non_applied_counter_overhead = counter_cost_record.costCounterNumberImpact / 4
        else:
            cpu_per_non_applied_counter = 0
            cpu_per_non_applied_ubd = 0
            non_applied_counter_overhead = 0
            total_used_ubd_number = self.appliedUBDNumber + self.nonAppliedUBDNumber
            total_used_bucket_number = self.appliedBucketNumber + self.nonAppliedBucketNumber

        total_counter_number = self.appliedUBDNumber + self.nonAppliedUBDNumber + \
                               self.appliedBucketNumber + self.nonAppliedBucketNumber

        cpu_impact = 0
        if self.nonAppliedBucketNumber > 0:  # need to include overhead for non-applied bucket
            cpu_impact = cpu_impact + non_applied_counter_overhead + \
                         cpu_per_non_applied_counter * self.nonAppliedBucketNumber

        if self.nonAppliedUBDNumber > 0:  # need to include overhead for non-applied UBD
            cpu_impact = cpu_impact + non_applied_counter_overhead + \
                         cpu_per_non_applied_ubd * self.nonAppliedUBDNumber

        if self.appliedBucketNumber > 0:  # need to include overhead for bucket
            cpu_impact = cpu_impact + counter_cost_record.costTurnOnbucket + \
                         self.appliedBucketNumber * counter_cost_record.costPerAppliedBucket

        if self.appliedUBDNumber > 0:  # need to include overhead for UBD
            cpu_impact = cpu_impact + counter_cost_record.costTurnOnUBD + \
                         self.appliedUBDNumber * counter_cost_record.costPerAppliedUBD

        if total_counter_number > 0:  # need to include RTDB read/update overhead
            cpu_impact = cpu_impact + math.ceil(total_counter_number / counter_cost_record.counterNumberPerRecord) * \
                         counter_cost_record.costDBReadUpdatePerRecord

        if total_used_ubd_number > 0:
            cpu_impact = cpu_impact + counter_cost_record.costCounterNumberImpact * \
                         math.pow(1 + counter_cost_record.percentageCounterNumberImpact, total_used_ubd_number)

        if total_used_bucket_number > 0:
            cpu_impact = cpu_impact + counter_cost_record.costCounterNumberImpact * \
                         math.pow(1 + counter_cost_record.percentageCounterNumberImpact, total_used_bucket_number)

        if counter_configuration.generateMultipleAMAForCounter:  # Multiple AMA
            cpu_impact = cpu_impact + self.project.release.cPUCostForMultipleAMA * math.ceil(total_counter_number / 10)

        if self.averageBundleNumberPerSubscriber > 0:
            cpu_impact = cpu_impact + counter_cost_record.costBundlePerRecord * self.averageBundleNumberPerSubscriber

        if self.average24hBundleNumberPerSubscriber > 0:
            cpu_impact = cpu_impact + counter_cost_record.costPer24hBundle * self.average24hBundleNumberPerSubscriber

        return cpu_impact * release_impact

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_group_counter_cost(self):
        counter_cost_record = self.get_counter_cost_record()

        if counter_cost_record is not None:
            return 0

        if GlobalConfiguration.objects.all().count() > 0:
            release_count_cpu_impact = GlobalConfiguration.objects.all()[0].releaseCountCPUImpact
        else:
            release_count_cpu_impact = 0.05

        release_gap = 0
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project

            release_gap = project.release.sequence - counter_cost_record.release.sequence

            if release_gap < 0:
                release_gap = 0

        release_impact = math.pow((1 + release_count_cpu_impact), release_gap)

        counter_configuration_list = CounterConfiguration.objects.all().filter(
            project=self.project,
        )

        if counter_configuration_list.count() > 0:
            counter_configuration = counter_configuration_list[0]
        else:
            return 0

        total_group_counter_number = counter_configuration.total_group_counter_number

        cpu_impact = math.ceil(total_group_counter_number / counter_cost_record.counterNumberPerRecord) * \
                     counter_cost_record.costGroupDBReadUpdatePerRecord + \
                     counter_cost_record.costTurnOnGroupBucket + \
                     counter_cost_record.costPerGroupSideBucket * total_group_counter_number

        return cpu_impact * release_impact

    class Meta:
        verbose_name = 'Counter Configuration for Call Type'
        verbose_name_plural = 'Counter Configuration for Call Type'


class CurrentSystemConfigurationManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return SystemConfiguration.objects.none()

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_system_configuration(
            self, project, application_name,
            backup_app_node_number_per_system, spare_app_node_number_per_system,
            backup_db_node_number_per_system, spare_db_node_pair_number_per_system
    ):
        system_configuration = self.create(
            project=project,
            applicationName=application_name,
            backupAppNodeNumberPerSystem=backup_app_node_number_per_system,
            spareAppNodeNumberPerSystem=spare_app_node_number_per_system,
            backupDBNodeNumberPerSystem=backup_db_node_number_per_system,
            spareDBNodePairNumberPerSystem=spare_db_node_pair_number_per_system,
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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentSystemConfigurationManager()  # The current project specific manager.

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
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return ApplicationConfiguration.objects.none()

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_application_config(
            self, project, application_name, deployOption,):

        traffic_information_list = TrafficInformation.current_objects.all()

        if traffic_information_list.count() > 0:
            traffic_information = traffic_information_list[0]
            activeSubscriber = traffic_information.activeSubscriber
            inactiveSubscriber = traffic_information.inactiveSubscriber
        else:
            activeSubscriber = 0
            inactiveSubscriber = 0

        application_config = self.create(
            project=project,
            applicationName=application_name,
            deployOption=deployOption,
            activeSubscriber=activeSubscriber,
            inactiveSubscriber=inactiveSubscriber,
        )
        return application_config


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
    )  # Need to set default=project.activeSubscriber

    inactiveSubscriber = models.IntegerField(
        default=0,
        verbose_name='Inactive Subscriber',
    )  # Need to set default=project.inactiveSubscriber

    trafficTPS = models.FloatField(
        verbose_name='CPS/TPS',
        default=0,
    )

    serverCPUCost = models.FloatField(default=0)
    clientCPUCost = models.FloatField(default=0)
    totalCPUCost = models.FloatField(default=0)
    ss7CPUCost = models.FloatField(default=0)
    tcpCPUCost = models.FloatField(default=0)
    diamCPUCost = models.FloatField(default=0)
    aprocCPUCost = models.FloatField(default=0)  # APROC
    asCPUCost = models.FloatField(default=0)  # Aerospike Server
    miscCPUCost = models.FloatField(default=0)
    cpuBudget = models.FloatField(default=0)

    ss7InSizePerSecond = models.FloatField(default=0)
    ss7OutSizePerSecond = models.FloatField(default=0)
    ldapSizePerSecond = models.FloatField(default=0)
    diameterSizePerSecond = models.FloatField(default=0)
    muTCPSize = models.FloatField(default=0)  # Mate update Size
    featureSS7InSize = models.FloatField(default=0)
    featureSS7OutSize = models.FloatField(default=0)
    featureLDAPSize = models.FloatField(default=0)
    featureDiameterSize = models.FloatField(default=0)
    spaDataSize = models.FloatField(default=0)

    featureCost = models.FloatField(default=0)
    counterCost = models.FloatField(default=0)
    groupCounterCost = models.FloatField(default=0)

    ndbCPULimitation = models.FloatField(default=0)

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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentApplicationConfigurationManager()  # The current project specific manager.

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def current_application_information(self):
        current_application_information_list = ApplicationInformation.objects.all().filter(
            release=self.project.release,
            application=self.applicationName,
        )
        if current_application_information_list.count() > 0:
            return current_application_information_list[0]

        return None

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def traffic_information_list(self):
        return TrafficInformation.current_objects.all()

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_node_number_needed(self):
        if self.cpuBaseNodeNumber >= self.memoryBaseNodeNumber:
            self.nodeNumberNeeded = self.cpuBaseNodeNumber
            self.boundType = 'CPU Bound'
        else:
            self.nodeNumberNeeded = self.memoryBaseNodeNumber
            self.boundType = 'Memory Bound'

    # @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate_cost_for_epay(self):

        for traffic in self.traffic_information_list:
            traffic.calculate_for_traffic()
            self.serverCPUCost += traffic.serverCPUCost
            self.clientCPUCost += traffic.cpuCostPerCall
            self.totalCPUCost += traffic.totalCPUCost
            self.ss7CPUCost += traffic.ss7CPUCost
            self.tcpCPUCost += traffic.tcpCPUCost
            self.diamCPUCost += traffic.diamCPUCost
            self.aprocCPUCost += traffic.aprocCPUCost
            self.asCPUCost += traffic.asCPUCost

            self.spaDataSize += traffic.spaDataSize

            self.ss7InSizePerSecond += traffic.ss7InSizePerSecond
            self.ss7OutSizePerSecond += traffic.ss7OutSizePerSecond
            self.ldapSizePerSecond += traffic.ldapSizePerSecond
            self.diameterSizePerSecond += traffic.diameterSizePerSecond
            self.muTCPSize += traffic.muTCPSize  # Mate update Size
            self.featureSS7InSize += traffic.featureSS7InSize
            self.featureSS7OutSize += traffic.featureSS7OutSize
            self.featureLDAPSize += traffic.featureLDAPSize
            self.featureDiameterSize += traffic.featureDiameterSize

            self.ndbCPULimitation += traffic.ndbCPULimitation * self.trafficTPS
            self.trafficTPS += traffic.trafficTPS

            self.featureCost += traffic.featureCost

            self.counterCost += traffic.counterCost
            self.groupCounterCost += traffic.groupCounterCost

        self.totalCPUCost = self.serverCPUCost + self.clientCPUCost
        self.miscCPUCost = self.ss7CPUCost + self.tcpCPUCost + self.diamCPUCost
        if self.trafficTPS > 0:
            self.ndbCPULimitation = self.ndbCPULimitation / self.trafficTPS
        else:
            self.ndbCPULimitation = 0

        self.save()

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_client_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic.get_total_cost()

        return total_call_cost

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_sever_cpu_cost(self):
        if self.current_application_information is not None:
            total_call_cost = 0

            for traffic in self.traffic_information_list:
                total_call_cost += self.current_application_information.cpuCostForServer * traffic.trafficTPS

            return total_call_cost

        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def tcp_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic.tcpCPUCost
            logger.g_logger.info('tcpCPUCost: %s, total_call_cost: %s' % (traffic.tcpCPUCost, total_call_cost))

        return total_call_cost

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ss7_cpu_cost(self):
        if self.current_application_information is not None:
            total_call_cost = 0

            for traffic in self.traffic_information_list:
                total_call_cost += traffic.ss7CPUCost

            return total_call_cost

        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def db_cpu_cost(self):
        # if not self.current_application_information:
        #     total_call_cost = 0
        #
        #     for traffic in self.traffic_information_list:
        #         total_call_cost += traffic.ss7CPUCost
        #
        #     return total_call_cost

        return 0

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def misc_cpu_cost(self):
        return self.ss7_cpu_cost + self.tcp_cpu_cost + self.db_cpu_cost + self.total_sever_cpu_cost

    @property
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_cpu_cost(self):
        return self.misc_cpu_cost + self.total_client_cpu_cost

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_app_memory(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_db_cache_size(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_ama_disk_size(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_db_disk_size(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ama_record_per_second(self):
        pass

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = ApplicationConfiguration.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(applicationName=self.applicationName).exists():
                raise ValidationError('Application: %s existed!' % self.applicationName)

    class Meta:
        verbose_name = 'Application Configuration'
        verbose_name_plural = 'Application Configuration'


class CurrentCalculatedResultManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_calculated_result(
            self, project, application_name, app_node_number,
            db_node_number, io_node_number, ):
        calculated_result = self.create(
            project=project,
            applicationName=application_name,
            appNodeNumber=app_node_number,
            dbNodeNumber=db_node_number,
            ioNodeNumber=io_node_number,
        )
        return calculated_result

    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    objects = models.Manager()  # The default manager.
    current_objects = CurrentCalculatedResultManager()  # The current project specific manager.

    def __str__(self):
        return self.applicationName.name

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
    dbCacheSize = models.FloatField(default=0)  # MB
    totalMemoryUsage = models.FloatField(default=0)  # MB
    sigtranSpeed = models.FloatField(default=0)  # Byte/Second
    ethernetPortsRequiredNumber = models.IntegerField(default=0)
    totalTCPUDPSpeed = models.FloatField(default=0)  # Byte/Second
    amaRecordNumberPerSecond = models.FloatField(default=0)
    dialyBillingFileSize = models.FloatField(default=0)  # MB
    amaRetrieveSpeed = models.FloatField(default=0)  # Byte/Second
    ladpDiameterUDP = models.FloatField(default=0)  # Byte/Second
    muSpeed = models.FloatField(default=0)  # Byte/Second

    memoryUsagePerAppNode = models.FloatField(default=0)  # MB
    memoryUsagePerClient = models.FloatField(default=0)  # MB
    appNodeMemoryUsagePercent = models.FloatField(default=0)  # %

    pilotSharedDiskSize = models.FloatField(default=0)  # MB
    dbDiskSizeForMateUpdate = models.FloatField(default=0)  # MB
    diskSizeForDB = models.FloatField(default=0)  # MB

    objects = models.Manager()  # The default manager.
    current_objects = CurrentDimensioningResultManager()  # The current project specific manager.

    class Meta:
        verbose_name = 'Dimensioning Result'
        verbose_name_plural = 'Dimensioning Result'

    def __str__(self):
        return self.applicationName.name

class CurrentDimensioningResultPerSystemManager(models.Manager):
    @logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    dbCacheSize = models.FloatField(default=0)  # MB
    totalMemoryUsage = models.FloatField(default=0)  # MB
    sigtranSpeed = models.FloatField(default=0)  # Byte/Second
    totalTCPUDPSpeed = models.FloatField(default=0)  # Byte/Second
    amaRecordNumberPerSecond = models.FloatField(default=0)
    dialyBillingFileSize = models.FloatField(default=0)  # MB
    amaRetrieveSpeed = models.FloatField(default=0)  # Byte/Second
    ladpDiameterUDP = models.FloatField(default=0)  # Byte/Second
    muSpeed = models.FloatField(default=0)  # Byte/Second

    memoryUsagePerAppNode = models.FloatField(default=0)  # MB
    memoryUsagePerClient = models.FloatField(default=0)  # MB
    appNodeMemoryUsagePercent = models.FloatField(default=0)  # %

    pilotSharedDiskSize = models.FloatField(default=0)  # MB
    dbDiskSizeForMateUpdate = models.FloatField(default=0)  # MB
    diskSizeForDB = models.FloatField(default=0)  # MB

    objects = models.Manager()  # The default manager.
    current_objects = CurrentDimensioningResultPerSystemManager()  # The current project specific manager.

    class Meta:
        verbose_name = 'Dimensioning Result Per System'
        verbose_name_plural = 'Dimensioning Result Per System'
