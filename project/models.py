from django.db import models
from django.contrib.auth.models import User
from service.models import Release, CallType, FeatureName, DBInformation, CallCost, \
    ApplicationName, FeatureDBImpact, FeatureCallTypeConfiguration, FeatureCPUImpact, \
    CounterCost, ApplicationInformation, FeatureAdditionalImpact, OtherApplicationInformation
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

BOUND_TYPE_OPTION = (('CPU Bound', 'CPU Bound'), ('Memory Bound', 'Memory Bound'), ('-', '-'))

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM = 0.15

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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer')
    version = models.IntegerField(default=1, verbose_name='Version')
    createTime = models.TimeField(auto_now=True, verbose_name='Create Time')

    comment = models.TextField(default='', verbose_name='Comment', blank=True)

    database_type = models.ForeignKey(DBMode, on_delete=models.CASCADE, verbose_name='Database Type')

    def __str__(self):
        return self.name

    @property
    def hardwareType(self):
        return self.hardwareModel.hardwareType

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Project'

    def save(self, *args, **kwargs):
        db_config_list = DBConfiguration.current_objects.all()

        for db_config in db_config_list:
            db_info_list = DBInformation.objects.all().filter(
                db=db_config.dbInfo.db,
                mode=self.database_type,
                release=self.release,
            )
            if db_info_list.count() > 0:
                db_config.dbInfo = db_info_list[0]
                db_config.recordSize = db_config.get_record_size()
                if (self.database_type.name == 'NDB') and (db_config.placeholderRatio <= 0):
                    db_config.placeholderRatio = db_config.dbInfo.db.ndbRefPlaceholderRatio
                db_config.save()

        super(Project, self).save(*args, **kwargs)


class WorkingProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name


class CurrentProjectInformationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return ProjectInformation.objects.none()


class ProjectInformation(models.Model):
    NDB_DEPLOY_OPTION = (('Combo', 'Combo'), ('Individual', 'Individual'), )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    vmType = models.ForeignKey(VMType, on_delete=models.CASCADE, verbose_name='VM Type')
    cpuNumber = models.ForeignKey(CPUList, on_delete=models.CASCADE, related_name='APP_CPU_Number', verbose_name='CPU Number', )

    memory = models.ForeignKey(MemoryList, on_delete=models.CASCADE, related_name='APP_Memory', verbose_name='Memory')
    clientNumber = models.IntegerField(verbose_name='Client Number', default=0)

    # dbCPUNumber = models.IntegerField(default=40, verbose_name='DB CPU Number', )
    dbCPUNumber = models.ForeignKey(CPUList, on_delete=models.CASCADE, related_name='DB_CPU_Number', verbose_name='DB CPU Number',
                                    null=True, blank=True)
    # dbMemory = models.IntegerField(default=105, verbose_name='DB Memory', )
    dbMemory = models.ForeignKey(MemoryList, on_delete=models.CASCADE, related_name='DB_Memory', verbose_name='DB Memory',
                                 null=True, blank=True)

    pilotCPUNumber = models.ForeignKey(CPUList, on_delete=models.CASCADE, related_name='Pilot_CPU_Number', verbose_name='Pilot CPU Number',
                                       null=True, blank=True)
    pilotMemory = models.ForeignKey(MemoryList, on_delete=models.CASCADE, related_name='Pilot_Memory', verbose_name='Pilot Memory',
                                    null=True, blank=True)

    ioCPUNumber = models.ForeignKey(CPUList, on_delete=models.CASCADE, related_name='IO_CPU_Number', verbose_name='IO CPU Number',
                                    null=True, blank=True)
    ioMemory = models.ForeignKey(MemoryList, on_delete=models.CASCADE, related_name='IO_Memory', verbose_name='IO Memory',
                                 null=True, blank=True)

    # pilotCPUNumber = models.IntegerField(default=8, verbose_name='Pilot CPU Number', )
    # pilotMemory = models.IntegerField(default=32, verbose_name='Pilot Memory')
    #
    # ioCPUNumber = models.IntegerField(default=16, verbose_name='IO CPU Number', )
    # ioMemory = models.IntegerField(default=32, verbose_name='IO Memory')

    mateCPUNumber = models.IntegerField(default=16, verbose_name='Mate CPU Number', )
    mateMemory = models.IntegerField(default=64, verbose_name='Mate Memory')

    sigtranLinkSpeed = models.IntegerField(verbose_name='SIGTRAN Link Speed (Mb/s)', default=10000)
    sigtranLinkNumber = models.IntegerField(verbose_name='SIGTRAN Link Number', default=1)
    sigtranPortUtil = models.FloatField(verbose_name='SIGTRAN Port Utility', default=0.3)

    amaRecordPerBillingBlock = models.FloatField(default=1, verbose_name='AMA Record Number per Billing Block')
    numberReleaseToEstimate = models.IntegerField(default=0, verbose_name='Number of Release to Estimate')
    cpuImpactPerRelease = models.FloatField(default=5, verbose_name='CPU Impact per Release (%)')
    memoryImpactPerRelease = models.FloatField(default=10, verbose_name='Memory Impact per Release (%)')
    dbImpactPerRelease = models.FloatField(default=10, verbose_name='DB Impact per Release (%)')
    deploy_option = models.CharField(max_length=16, choices=NDB_DEPLOY_OPTION, default='Combo',
                                     verbose_name='NDB Deploy Option')

    averageAMARecordPerCall = models.FloatField(verbose_name='Average AMA Record per Call')
    amaStoreDay = models.FloatField(verbose_name='AMA Store Days')

    activeSubscriber = models.IntegerField(verbose_name='Active Subscriber')
    inactiveSubscriber = models.IntegerField(verbose_name='Inactive Subscriber')
    groupAccountNumber = models.IntegerField(verbose_name='Number of Group Account', default=0,
                                             null=True, blank=True)

    cpuUsageTuning = models.ForeignKey(CPUTuning, on_delete=models.CASCADE, verbose_name='CPU Usage Tuning')
    memoryUsageTuning = models.ForeignKey(MemoryUsageTuning, on_delete=models.CASCADE,
                                          verbose_name='Memory Usage Tuning')

    objects = models.Manager()  # The default manager.
    current_objects = CurrentProjectInformationManager()  # The project-specific manager.



    def __str__(self):
        return self.project.name

    name = property(__str__)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save(self, *args, **kwargs):
        if self.project.hardwareType.isVM is not True:
            self.vmType = VMType.objects.all().filter(
                type='Native',
            )[0]

            self.cpuNumber = CPUList.objects.all().filter(
                hardwareModel=self.project.hardwareModel,
                clientNumber=self.cpuNumber.clientNumber,
            )[0]

        if self.project.hardwareType.isVM is not True or self.project.hardwareType.isSingleServer:
            self.dbCPUNumber = self.cpuNumber
            self.dbMemory = self.memory

        super(ProjectInformation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Project General Information'
        verbose_name_plural = 'Project General Information'


class CurrentTrafficInformationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_traffic_information(
            self, project, call_type, activeSubscriber, inactiveSubscriber,trafficBHTA,
            trafficTPS, callHoldingTime, ):
        traffic_information = self.create(
            project=project,
            callType=call_type,
            activeSubscriber=activeSubscriber,
            inactiveSubscriber=inactiveSubscriber,
            trafficBHTA=trafficBHTA,
            trafficTPS=trafficTPS,
            callHoldingTime=callHoldingTime,
        )
        return traffic_information

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
                # callType__isShow=True,
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
    cpuCostForRoutingClient = models.FloatField(default=0)
    aprocRoutingCost = models.FloatField(default=0)
    cpuCostPerCall = models.FloatField(default=0)
    totalCPUCost = models.FloatField(default=0)
    ss7CPUCost = models.FloatField(default=0)
    tcpCPUCost = models.FloatField(default=0)
    diamCPUCost = models.FloatField(default=0)
    aprocCPUCost = models.FloatField(default=0)  # APROC
    asdCPUCost = models.FloatField(default=0)  # Aerospike Server
    asdMateCost = models.FloatField(default=0)

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

    total_counter_number = 0
    call_cost = None
    cost_ratio = 0.0
    application = None
    application_information = None
    counter_configuration = None
    project_information = None
    feature_call_type_config_list = None
    feature_list = None
    counter_memory = 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_bhca_for_diameter_session(self):
        return self.volumeCCRiBHTA + self.volumeCCRuBHTA + self.volumeCCRtBHTA + \
               self.timeCCRiBHTA + self.timeCCRuBHTA + self.timeCCRtBHTA

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_counter_number(self):
        if CounterConfiguration.current_objects.count() > 0:
            return CounterConfiguration.current_objects.all()[0].total_counter_number
        else:
            return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_call_cost_record(self):
        # get call cost list for current call type and release
        call_cost_orig_list = CallCost.objects.all().filter(
            callType=self.callType,
            release=self.project.release,
        )

        call_cost_record = None

        if call_cost_orig_list.count() > 0:
            call_cost_list = call_cost_orig_list.filter(
                hardwareModel=self.project.hardwareModel,
                dbMode=self.project.database_type,
            )

            if call_cost_list.count() > 0:  # exact match
                return call_cost_list[0]

            call_cost_list = call_cost_orig_list.filter(
                hardwareModel=self.project.hardwareModel,
            )
            if call_cost_list.count() > 0:  # Database type not match
                return call_cost_list[0]

            call_cost_list = call_cost_orig_list.filter(
                dbMode=self.project.database_type,
            )

            if call_cost_list.all().count() > 0:
                call_cost_priority = 0
                for call_cost_object in call_cost_list:
                    if call_cost_object.hardwareModel.hardwareType == self.project.hardwareModel.hardwareType:
                        call_cost_record = call_cost_object
                        call_cost_priority = 3
                    elif call_cost_object.hardwareModel.cpu == self.project.hardwareModel.cpu:
                        if (call_cost_record is None) or (call_cost_priority < 2):
                            call_cost_priority = 2
                            call_cost_record = call_cost_object
                    else:
                        if call_cost_record is None:
                            call_cost_priority = 1
                            call_cost_record = call_cost_object

            if call_cost_record is None:
                call_cost_priority = 0
                for call_cost_object in call_cost_orig_list:
                    if call_cost_object.hardwareModel.hardwareType == self.project.hardwareModel.hardwareType:
                        call_cost_record = call_cost_object
                        call_cost_priority = 3
                    elif call_cost_object.hardwareModel.cpu == self.project.hardwareModel.cpu:
                        if (call_cost_record is None) or (call_cost_priority < 2):
                            call_cost_priority = 2
                            call_cost_record = call_cost_object
                    else:
                        if call_cost_record is None:
                            call_cost_priority = 1
                            call_cost_record = call_cost_object

        if call_cost_record is not None:
            return call_cost_record
        else:
            raise ValidationError(
                f'Call Cost for Call Type: {self.callType} of Release {self.project.release} not configured!')

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_cost_ratio(self):
        cost_ratio = self.call_cost.hardwareModel.cpu.singleThreadCapacity

        if self.call_cost.dbMode.name != self.project.database_type.name:
            if self.call_cost.dbMode.name == 'RTDB':  # RTDB cost --> NDB cost
                cost_ratio = cost_ratio * GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio
            else:  # NDB cost --> RTDB cost
                if GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio > 0:
                    cost_ratio = cost_ratio / GlobalConfiguration.objects.all()[0].ndbRTDBCostRatio

        return cost_ratio

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_counter_configuration(self):
        counter_configuration_list = CallTypeCounterConfiguration.current_objects.all().filter(
            callType=self.callType
        )
        if counter_configuration_list.count() > 0:
            return counter_configuration_list[0]
        return None

    # @property
    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def feature_configuration_list(self):
    #     return FeatureConfiguration.current_objects.all()
    #
    # @property
    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def feature_cpu_impact_percentage(self):
    #     cpu_impact_percentage = 0
    #     for feature_configuration in self.feature_configuration_list:
    #         feature_configuration.set_feature_cpu_impact(self.callType)
    #         cpu_impact_percentage += feature_configuration.cpu_percentage
    #
    #     return cpu_impact_percentage
    #
    # @property
    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def feature_ss7_in_size(self):
    #     ss7_in_size = 0
    #     for feature_configuration in self.feature_configuration_list:
    #         feature_configuration.set_feature_cpu_impact(self.callType)
    #         ss7_in_size += feature_configuration.ss7_in_size
    #
    #     return ss7_in_size
    #
    # @property
    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def feature_ss7_out_size(self):
    #     ss7_out_size = 0
    #     for feature_configuration in self.feature_configuration_list:
    #         feature_configuration.set_feature_cpu_impact(self.callType)
    #         ss7_out_size += feature_configuration.ss7_out_size
    #
    #     return ss7_out_size
    #
    # @property
    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def feature_ldap_message_size(self):
    #     ldap_message_size = 0
    #     for feature_configuration in self.feature_configuration_list:
    #         feature_configuration.set_feature_cpu_impact(self.callType)
    #         ldap_message_size += feature_configuration.ldap_message_size
    #
    #     return ldap_message_size
    #
    # @property
    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def feature_diameter_message_size(self):
    #     diameter_message_size = 0
    #     for feature_configuration in self.feature_configuration_list:
    #         feature_configuration.set_feature_cpu_impact(self.callType)
    #         diameter_message_size += feature_configuration.diameter_message_size
    #
    #     return diameter_message_size

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_application(self):
        application_name_list = ApplicationName.objects.all().filter(
            name='EPAY',
        )

        if application_name_list.count() > 0:
            return application_name_list[0]
        return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_application_information(self):
        application_information_list = ApplicationInformation.objects.all().filter(
            release=self.project.release,
            application=self.application,
        )
        if application_information_list.count() > 0:
            return application_information_list[0]
        return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_project_information(self):
        if ProjectInformation.current_objects.all().count() > 0:
            return ProjectInformation.current_objects.all()[0]
        return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_feature_call_type_config_list(self):
        return FeatureCallTypeConfiguration.objects.all().filter(
            callType=self.callType,
        )

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def gprs_cps(self):
        return (self.volumeCCRiBHTA + self.timeCCRiBHTA) * self.activeSubscriber / 3600

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def data_session_cip_size(self):
        if self.application_information is not None:
            return self.application_information.sessionCIPSize + \
                   self.application_information.ldapCIPSize  * self.averageCategoryPerSession + \
                   self.application_information.otherCIPSize
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_feature_list(self):
        return FeatureConfiguration.current_objects.all()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_feature_cost_impact(self):
        feature_total_cost_percent = 0.0
        feature_total_cost = 0.0

        for feature in self.feature_list:
            feature_call_type_conf = self.feature_call_type_config_list.filter(
                featureName=feature.feature,
            )
            if (feature_call_type_conf.count() > 0):
                feature_applicable = feature_call_type_conf[0].featureApplicable
            else:
                feature_applicable = 1

            if feature_applicable <= 0:
                continue

            if feature.feature.name == 'Online Hierarchy':
                feature_total_cost_percent += feature.featurePenetration * feature_applicable * \
                                      self.get_olh_cpu_impact(feature)
            elif feature.feature.name == 'Uncorrelated CCR-U/T Handling':
                feature_total_cost_percent += feature.featurePenetration * feature_applicable * \
                                              self.get_uncorrelated_ccrut_impact()
            else:
                feature_cpu_impact = FeatureCPUImpact.objects.all().filter(
                    featureName=feature.feature,
                )
                if (feature_cpu_impact.count() > 0):
                    feature_total_cost_percent += feature.featurePenetration * feature_applicable * \
                                                  (feature_cpu_impact[0].ccImpactCPUPercentage +
                                            feature_cpu_impact[0].reImpactCPUPercentage)
                    feature_total_cost += feature.featurePenetration * feature_applicable * self.trafficTPS * \
                                          (feature_cpu_impact[0].ccImpactCPUTime +
                                            feature_cpu_impact[0].reImpactCPUTime)

        return feature_total_cost_percent / 100, feature_total_cost / 100

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_olh_cpu_impact(self, feature):
        if FeatureAdditionalImpact.objects.all().count() > 0:
            feature_additional_impact = FeatureAdditionalImpact.objects.all()[0]
        else:
            return 0

        if feature.groupNumber < 1:
            feature.groupNumber = 1

        if feature.ratioOfLevel1 > 1:
            feature.ratioOfLevel1 = 1

        ratioOfLevel2 = 1 - feature.ratioOfLevel1

        if feature.colocateMemberGroup:
            olh_cpu_impact = feature_additional_impact.sameSys1GroupLevel1 * feature.ratioOfLevel1 + \
                             feature_additional_impact.sameSys1GroupLevel2 * ratioOfLevel2 + \
                             (feature.groupNumber - 1) * (feature_additional_impact.sameSys1GroupLevel1 * feature.ratioOfLevel1 +
                                                          feature_additional_impact.sameSys1GroupLevel2 * ratioOfLevel2)
        else:
            olh_cpu_impact = feature_additional_impact.diffSys1GroupLevel1 * feature.ratioOfLevel1 + \
                             feature_additional_impact.diffSys1GroupLevel2 * ratioOfLevel2 + \
                             (feature.groupNumber - 1) * (feature_additional_impact.diffSys1GroupLevel1 * feature.ratioOfLevel1 +
                                                          feature_additional_impact.diffSys1GroupLevel2 * ratioOfLevel2)
        return olh_cpu_impact

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_uncorrelated_ccrut_impact(self):
        if FeatureAdditionalImpact.objects.all().count() > 0:
            feature_additional_impact = FeatureAdditionalImpact.objects.all()[0]
        else:
            return 0

        ccrut_bhca = self.volumeCCRtBHTA + self.volumeCCRuBHTA + self.timeCCRtBHTA + self.timeCCRuBHTA
        total_bhca = ccrut_bhca + self.timeCCRiBHTA + self.volumeCCRiBHTA

        if total_bhca > 0:
            return feature_additional_impact.uncorrelatedCCRUTHandling * ccrut_bhca / total_bhca
        else:
            return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                feature_ss7_in_size += penetration * feature.ss7_in_size * self.trafficTPS

        return feature_ss7_in_size

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                feature_ss7_out_size += penetration * feature.ss7_out_size  * self.trafficTPS

        return feature_ss7_out_size

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                feature_ldap_size += penetration * feature.ldap_message_size * self.trafficTPS

        return feature_ldap_size

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                feature_diameter_size += penetration * feature.diameter_message_size * self.trafficTPS
        return feature_diameter_size

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = TrafficInformation.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(callType=self.callType).exists():
                raise ValidationError('Call Type: %s existed!' % self.callType)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save(self, *args, **kwargs):
        self.validate_unique()
        super(TrafficInformation, self).save(*args, **kwargs)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps(self):
        return self.activeSubscriber * self.trafficBHTA / 3600

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_bhca(self):
        return self.trafficBHTA * 3600 / self.activeSubscriber if self.activeSubscriber > 0 else 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_default_active_subscriber(self):
        if self.project_information is not None:
            return self.project_information.activeSubscriber
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_default_inactive_subscriber(self):
        if self.project_information is not None:
            return self.project_information.inactiveSubscriber

    def __str__(self):
        return self.callType.name

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_call_cost(self):
        if self.call_cost is not None:
            return self.call_cost.callCost * self.trafficTPS * self.cost_ratio
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_cost(self):
        total_cost = self.get_call_cost() + self.counterCost
        (feature_impact_percentage, feature_impact_cost) = self.get_feature_cost_impact()
        self.featureCost = total_cost * feature_impact_percentage  + feature_impact_cost
        return self.get_call_cost() + self.featureCost + self.counterCost

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_server_cost(self):
        if self.call_cost is not None:
            return self.trafficTPS * self.call_cost.cpuCostForServer * self.cost_ratio
        if self.application_information is not None:
            return self.trafficTPS * self.application_information.cpuCostForServer
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tcp_cost(self):
        if self.callType is not None and self.callType.tcpipNumber > 0:
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, TCP Cost: %s' % (
                    self.trafficTPS, self.call_cost.tcpCost))
                return self.trafficTPS * self.call_cost.tcpCost * self.cost_ratio

            if (self.application_information is not None):
                logger.g_logger.info('Traffic (TPS): %s, tcpCost: %s' % (
                    self.trafficTPS, self.application_information.tcpCost))
                return self.trafficTPS * self.application_information.tcpCost

        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_diam_cost(self):
        if self.callType is not None and self.callType.diameterNumber > 0:
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, Diam Cost: %s' % (
                    self.trafficTPS, self.call_cost.diamCost))
                return self.trafficTPS * self.call_cost.diamCost * self.cost_ratio

            if (self.application_information is not None):
                logger.g_logger.info('Traffic (TPS): %s, Diam Cost: %s' % (
                    self.trafficTPS, self.application_information.diamCost))
                return self.trafficTPS * self.application_information.diamCost
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_cost(self):
        if self.callType is not None and self.callType.ss7Number > 0:
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, SS7 Cost: %s' % (
                    self.trafficTPS, self.call_cost.ss7Cost))
                return self.trafficTPS * self.call_cost.ss7Cost * self.cost_ratio

            if (self.application_information is not None):
                logger.g_logger.info('Traffic (TPS): %s, SS7 Cost: %s' % (
                    self.trafficTPS, self.application_information.ss7Cost))
                return self.trafficTPS * self.application_information.ss7Cost
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_aproc_cost(self):
        if self.project.database_type.name == 'NDB':
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, APROC Cost: %s' % (
                    self.trafficTPS, self.call_cost.aprocCost))
                return self.trafficTPS * self.call_cost.aprocCost * self.cost_ratio
            if self.application_information is not None:
                logger.g_logger.info('Traffic (TPS): %s, APROC Cost: %s' % (
                    self.trafficTPS, self.application_information.aprocCost))
                return self.trafficTPS * self.application_information.aprocCost
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_asd_cost(self):
        if self.project.database_type.name == 'NDB':
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, ASD Cost: %s' % (
                    self.trafficTPS, self.call_cost.asdCost))
                return self.trafficTPS * self.call_cost.asdCost * self.cost_ratio
            if self.application_information is not None:
                logger.g_logger.info('Traffic (TPS): %s, ASD Cost: %s' % (
                    self.trafficTPS, self.application_information.asdCost))
                return self.trafficTPS * self.application_information.asdCost
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_asd_mate_cost(self):
        if self.project.database_type.name == 'NDB':
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, ASD Cost on Mate: %s' % (
                    self.trafficTPS, self.call_cost.asdMateCost))
                return self.trafficTPS * self.call_cost.asdMateCost * self.cost_ratio
            if self.application_information is not None:
                logger.g_logger.info('Traffic (TPS): %s, ASD Cost on Mate: %s' % (
                    self.trafficTPS, self.application_information.asdMateCost))
                return self.trafficTPS * self.application_information.asdMateCost
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_routing_client_cost(self):
        if self.project.database_type.name == 'NDB':
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, Routing Client Cost: %s' % (
                    self.trafficTPS, self.call_cost.cpuCostForRoutingClient))
                return self.trafficTPS * self.call_cost.cpuCostForRoutingClient * self.cost_ratio
            if self.application_information is not None:
                logger.g_logger.info('Traffic (TPS): %s, Routing Client Cost: %s' % (
                    self.trafficTPS, self.application_information.cpuCostForRoutingClient))
                return self.trafficTPS * self.application_information.cpuCostForRoutingClient
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_aproc_routing_cost(self):
        if self.project.database_type.name == 'NDB':
            if self.call_cost is not None:
                logger.g_logger.info('Traffic (TPS): %s, APROC Routing Cost: %s' % (
                    self.trafficTPS, self.call_cost.aprocRoutingCost))
                return self.trafficTPS * self.call_cost.aprocRoutingCost * self.cost_ratio
            if self.application_information is not None:
                logger.g_logger.info('Traffic (TPS): %s, APROC Routing Cost: %s' % (
                    self.trafficTPS, self.application_information.aprocRoutingCost))
                return self.trafficTPS * self.application_information.aprocRoutingCost
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_counter_memory(self):
        self.total_counter_number = self.get_total_counter_number()

        if (self.application_information is not None) and (self.application_information.counterMemoryImpact > 0):
            return self.application_information.counterMemoryImpact * self.total_counter_number
        else:
            return self.project.release.counterMemoryImpact * self.total_counter_number

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_spa_data_size_for_diameter_session(self):
        diameter_session_size = self.data_session_cip_size + self.counter_memory
        if self.averageActiveSessionPerSubscriber > 0:
            return diameter_session_size * self.averageActiveSessionPerSubscriber * \
                   self.activeSubscriber / BYTES_TO_MILLION
        return diameter_session_size * self.gprs_cps * self.callHoldingTime / BYTES_TO_MILLION

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def call_record_size(self):
        if (self.application_information is not None) and (self.application_information.callRecordSize > 0):
            return self.application_information.callRecordSize
        else:
            return self.project.release.callRecordSize

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_spa_data_size(self):
        self.counter_memory = self.get_counter_memory()

        if self.callHoldingTime < 1:
            self.callHoldingTime = 1
        if self.volumeCCRiBHTA > 0 or self.timeCCRiBHTA > 0:
            return self.get_spa_data_size_for_diameter_session()
        return self.trafficTPS * self.callHoldingTime * \
               (self.call_record_size + self.counter_memory) / BYTES_TO_MILLION

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_in_size(self):
        if self.callType is not None:
            return self.trafficTPS * self.callType.ss7InSize
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_out_size(self):
        if self.callType is not None:
            return self.trafficTPS * self.callType.ss7OutSize
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ldap_size(self):
        if self.callType is not None:
            return self.trafficTPS * self.callType.tcpipSize
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_diameter_size(self):
        if self.callType is not None:
            return self.trafficTPS * self.callType.diameterSize
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_mu_size(self):
        if self.callType is not None:
            return self.trafficTPS * self.callType.mateUpdateSize #* self.callType.mateUpdateNumber
        return 0

    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate_for_traffic(self):
        self.call_cost = self.get_call_cost_record()
        self.cost_ratio = self.get_call_cost()

        self.application = self.get_application()
        self.application_information = self.get_application_information()
        self.counter_configuration = self.get_counter_configuration()
        self.project_information = self.get_project_information()
        self.feature_call_type_config_list = self.get_feature_call_type_config_list()
        self.feature_list = self.get_feature_list()

        self.serverCPUCost = self.get_server_cost()
        if self.call_cost is not None:
            self.cpuCostPerCall = self.call_cost.callCost
        else:
            self.cpuCostPerCall = 0

        self.cpuCostForRoutingClient = self.get_routing_client_cost()
        self.totalCPUCost = self.get_total_cost()
        self.ss7CPUCost = self.get_ss7_cost()
        self.tcpCPUCost = self.get_tcp_cost()
        self.diamCPUCost = self.get_diam_cost()
        self.aprocCPUCost = self.get_aproc_cost()
        self.aprocRoutingCost = self.get_aproc_routing_cost()
        self.asdCPUCost = self.get_asd_cost()
        self.asdMateCost = self.get_asd_mate_cost()

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

        # self.featureCost = self.feature_cost
        if self.counter_configuration is not None:
            self.counterCost = self.counter_configuration.get_counter_cost() * self.trafficTPS
            self.groupCounterCost = self.counter_configuration.get_group_counter_cost()* self.trafficTPS
        else:
            self.counterCost = 0
            self.groupCounterCost = 0

        self.save()

    name = property(__str__)

    class Meta:
        # db_table = 'Traffic Information'
        unique_together = ("project", "callType")


class CurrentFeatureConfigurationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    feature_cpu_impact = None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_project_information(self):
        if ProjectInformation.current_objects.all().count() > 0:
            return ProjectInformation.current_objects.all()[0]
        return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = FeatureConfiguration.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(feature=self.feature).exists():
                raise ValidationError('Feature Name: %s existed!' % self.feature)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save(self, *args, **kwargs):
        if WorkingProject.objects.all().count() > 0:
            self.project = WorkingProject.objects.all()[0].project

        self.validate_unique()
        if self.feature.name == 'Online Hierarchy':
            project_information = self.get_project_information()
            if project_information is not None:
                if project_information.groupAccountNumber == 0:
                    project_information.groupAccountNumber = math.ceil(
                        project_information.activeSubscriber * self.featurePenetration / 100)
                    project_information.save()

        super(FeatureConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        if WorkingProject.objects.all().count() > 0:
            self.project = WorkingProject.objects.all()[0].project

        return self.project.name + "_" + self.feature.name

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def set_feature_cpu_impact(self, call_type):
        feature_cpu_impact_list = FeatureCPUImpact.objects.all().filter(
            featureName=self.feature
        )
        feature_call_type_list = FeatureCallTypeConfiguration.objects.all().filter(
            callType=call_type,
            featureName=self.feature,
        )
        if feature_call_type_list.count() > 0 and feature_call_type_list[0].featureApplicable > 0:
            if feature_cpu_impact_list.count() > 0:
                self.feature_cpu_impact = feature_cpu_impact_list[0]

        self.feature_cpu_impact = None


    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ss7_in_size(self):
        if self.feature_cpu_impact is not None:
            return self.feature_cpu_impact.ss7In
        return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ss7_out_size(self):
        if self.feature_cpu_impact is not None:
            return self.feature_cpu_impact.ss7Out
        return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ldap_message_size(self):
        if self.feature_cpu_impact is not None:
            return self.feature_cpu_impact.ldapMessageSize
        return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def diameter_message_size(self):
        if self.feature_cpu_impact is not None:
            return self.feature_cpu_impact.diameterMessageSize
        return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def cpu_time(self):
        if self.feature_cpu_impact is not None:
            return self.feature_cpu_impact.ccImpactCPUTime + self.feature_cpu_impact.reImpactCPUTime
        return 0

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def cpu_percentage(self):
        if self.feature_cpu_impact is not None:
            return self.feature_cpu_impact.ccImpactCPUPercentage + self.feature_cpu_impact.reImpactCPUPercentage
        return 0

    name = property(__str__)

    class Meta:
        unique_together = (("project", "feature"),)


class CurrentDBConfigurationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return DBConfiguration.objects.none()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_db_configuration(
            self, project, application, db_info, db_factor,
            placeholder_ratio, member_group_option, record_size, subscriber_number,
            reference_placeholder_ratio, reference_db_factor):
        db_configuration = self.create(
            project=project,
            application=application,
            dbInfo=db_info,
            dbFactor=db_factor,
            placeholderRatio=placeholder_ratio,
            memberGroupOption=member_group_option,
            recordSize=record_size,
            subscriberNumber=subscriber_number,
            referencePlaceholderRatio=reference_placeholder_ratio,
            referenceDBFactor=reference_db_factor,
        )
        return db_configuration

class DBConfiguration(models.Model):
    MEMBER_GROUP_OPTION = (('Member', 'Member'), ('Group', 'Group'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    application = models.ForeignKey(ApplicationName, on_delete=models.CASCADE)
    dbInfo = models.ForeignKey(DBInformation, on_delete=models.CASCADE, verbose_name='DB Name')

    dbFactor = models.FloatField(default=0, verbose_name='DB Factor')
    placeholderRatio = models.FloatField(default=0, verbose_name='Placeholder Ratio')
    memberGroupOption = models.CharField(max_length=10, choices=MEMBER_GROUP_OPTION,
                                         default='Member', verbose_name='DB Location')

    recordSize = models.IntegerField(default=0, verbose_name='Record Size (Byte)')
    subscriberNumber = models.IntegerField(default=0, verbose_name='Subscriber Number')
    recordNumber = models.IntegerField(default=0, verbose_name='Record Number')
    cacheSize = models.IntegerField(default=0, verbose_name='Cache Size (MB)')
    todoLogSize = models.IntegerField(default=0, verbose_name='Todo Log Size (MB)')
    mateLogSize = models.IntegerField(default=0, verbose_name='Mate Log Size (MB)')
    referencePlaceholderRatio = models.FloatField(default=0)
    referenceDBFactor = models.FloatField(default=0)

    objects = models.Manager()  # The default manager.
    current_objects = CurrentDBConfigurationManager()  # The current project specific manager.

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_record_size(self):
        return self.dbInfo.recordSize

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_record_number(self):
        return math.ceil(self.subscriberNumber * self.dbFactor)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ndb_node_size(self):
        record_number = self.get_record_number()
        r = math.ceil(record_number / 18)
        index_number = self.dbInfo.db.prefixTableIndexNumber

        ndb_node_size = math.ceil(record_number / BYTES_TO_MILLION * 64 * 2 +
                                  (record_number * 3 + 2 * r) / BYTES_TO_MILLION * 28.44 * index_number)

        return ndb_node_size

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_node_size(self):
        if self.project.database_type.name == 'RTDB':
            return self.get_rtdb_node_size()
        else:
            return self.get_ndb_node_size()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_cache_size(self):
        if self.project.database_type.name == 'RTDB':
            db_overhead = self.dbInfo.db.rtdbOverhead
        else:
            db_overhead = 1

        return math.ceil(self.recordSize * self.recordNumber * db_overhead *
                         (1 - self.placeholderRatio) / BYTES_TO_MILLION) + self.get_node_size()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_todo_log_size(self, db_blade_needed, traffic):
        if self.project.database_type.name == 'NDB':
            return 0
        cache_size = self.get_cache_size()
        rproc_number = math.ceil(cache_size / 2000, db_blade_needed)
        impact_size = self.dbInfo.db.todoLogSize

        todo_log_size = math.ceil(impact_size * traffic * 3600 * 24 * 2 / BYTES_TO_MILLION / 10) * 10

        if todo_log_size > (1000 * 2 * rproc_number):
            return 1000 * 2 * rproc_number
        else:
            return todo_log_size

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ndb_reference_placeholder_ratio(self):
        return self.dbInfo.db.ndbRefPlaceholderRatio

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save(self, *args, **kwargs):
        self.recordNumber = self.get_record_number()
        self.cacheSize = self.get_cache_size()
        #self.todoLogSize = self.get_todo_log_size(db_blade_needed, traffic)
        #self.mateLogSize = self.get_mate_log_size(traffic)

        super(DBConfiguration, self).save(*args, **kwargs)


'''
    Define counter configuration for the project.
    Need to calculate the db impact for CTRTDB.
'''


class CurrentCounterConfigurationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_bundle_number(self):
        return self.averageBundleNumberPerSubscriber + self.average24hBundleNumberPerSubscriber

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
               self.appliedBucketNumber + self.appliedUBDNumber

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_group_counter_number(self):
        return self.groupBundleNumber + self.groupBucketNumber

    def __str__(self):
        return self.project.name

    name = property(__str__)

    class Meta:
        verbose_name = 'Counter Configuration'
        verbose_name_plural = 'Counter Configuration'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_counter(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + self.appliedBucketNumber + self.appliedUBDNumber


class CurrentCallTypeCounterConfigurationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return CounterConfiguration.objects.none()


class CallTypeCounterConfiguration(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    callType = models.ForeignKey(
        CallType,
        on_delete=models.CASCADE,
        verbose_name='Call Type',
    )

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

    counter_cost_record = None

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_counter_number(self):
        return self.nonAppliedBucketNumber + self.nonAppliedUBDNumber + \
               self.appliedBucketNumber + self.appliedUBDNumber

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_bundle_number(self):
        return self.averageBundleNumberPerSubscriber + self.average24hBundleNumberPerSubscriber

    class Meta:
        verbose_name = 'Counter Configuration For Call Type'
        verbose_name_plural = 'Counter Configuration For Call Type'

    def __str__(self):
        return self.callType.name

    name = property(__str__)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def release_impact(self):
        if GlobalConfiguration.objects.all().count() > 0:
            release_count_cpu_impact = GlobalConfiguration.objects.all()[0].releaseCountCPUImpact
        else:
            release_count_cpu_impact = 0.05

        release_gap = 0
        if WorkingProject.objects.all().count() > 0:
            project = WorkingProject.objects.all()[0].project

            release_gap = project.release.sequence - self.counter_cost_record.release.sequence

            if release_gap < 0:
                release_gap = 0

        release_impact = math.pow((1 + release_count_cpu_impact), release_gap)

        logger.g_logger.info('Counter Release: %s, Release Gap: %s, Release Impact: %s' %
                             (self.counter_cost_record.release, release_gap, release_impact))

        return release_impact

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_counter_cost(self):
        self.counter_cost_record = self.get_counter_cost_record()
        
        if self.counter_cost_record is None:
            return 0

        counter_configuration_list = CounterConfiguration.objects.all().filter(
            project=self.project,
        )

        if counter_configuration_list.count() > 0:
            counter_configuration = counter_configuration_list[0]
        else:
            return 0

        if counter_configuration.turnOnBasicCriteriaCheck:
            cpu_per_non_applied_counter = self.counter_cost_record.costPerUnappliedCounterWithBasicCriteria
            cpu_per_non_applied_ubd = self.counter_cost_record.costPerUnappliedCounterWithBasicCriteria
            total_used_ubd_number = self.appliedUBDNumber
            total_used_bucket_number = self.appliedBucketNumber

            non_applied_counter_overhead = self.counter_cost_record.costCounterNumberImpact / 4
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
            cpu_impact = cpu_impact + self.counter_cost_record.costTurnOnBucket + \
                         self.appliedBucketNumber * self.counter_cost_record.costPerAppliedBucket

        if self.appliedUBDNumber > 0:  # need to include overhead for UBD
            cpu_impact = cpu_impact + self.counter_cost_record.costTurnOnUBD + \
                         self.appliedUBDNumber * self.counter_cost_record.costPerAppliedUBD

        if total_counter_number > 0:  # need to include RTDB read/update overhead
            cpu_impact = cpu_impact + math.ceil(total_counter_number / self.counter_cost_record.counterNumberPerRecord) * \
                         self.counter_cost_record.costDBReadUpdatePerRecord

        if total_used_ubd_number > 0:
            cpu_impact = cpu_impact + self.counter_cost_record.costCounterNumberImpact * \
                         math.pow(1 + self.counter_cost_record.percentageCounterNumberImpact, total_used_ubd_number)

        if total_used_bucket_number > 0:
            cpu_impact = cpu_impact + self.counter_cost_record.costCounterNumberImpact * \
                         math.pow(1 + self.counter_cost_record.percentageCounterNumberImpact, total_used_bucket_number)

        if counter_configuration.generateMultipleAMAForCounter:  # Multiple AMA
            cpu_impact = cpu_impact + self.project.release.cPUCostForMultipleAMA * math.ceil(total_counter_number / 10)

        if self.averageBundleNumberPerSubscriber > 0:
            cpu_impact = cpu_impact + self.counter_cost_record.costBundlePerRecord * self.averageBundleNumberPerSubscriber

        if self.average24hBundleNumberPerSubscriber > 0:
            cpu_impact = cpu_impact + self.counter_cost_record.costPer24hBundle * self.average24hBundleNumberPerSubscriber

        return cpu_impact * self.release_impact * self.counter_cost_record.hardwareModel.cpu.singleThreadCapacity

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_group_counter_cost(self):
        if self.counter_cost_record is not None:
            return 0

        counter_configuration_list = CounterConfiguration.objects.all().filter(
            project=self.project,
        )

        if counter_configuration_list.count() > 0:
            counter_configuration = counter_configuration_list[0]
        else:
            return 0

        total_group_counter_number = counter_configuration.total_group_counter_number

        cpu_impact = math.ceil(total_group_counter_number / self.counter_cost_record.counterNumberPerRecord) * \
                     self.counter_cost_record.costGroupDBReadUpdatePerRecord + \
                     self.counter_cost_record.costTurnOnGroupBucket + \
                     self.counter_cost_record.costPerGroupSideBucket * total_group_counter_number

        return cpu_impact * self.release_impact

    class Meta:
        verbose_name = 'Counter Configuration for Call Type'
        verbose_name_plural = 'Counter Configuration for Call Type'


class CurrentSystemConfigurationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return SystemConfiguration.objects.none()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                 ('Group Node', 'Group Node'),
                 ('CDR Pre-Processor Node', 'CDR Pre-Processor Node'),
                 ('eCGS Node', 'eCGS Node'), ('NTGW Node', 'NTGW Node'),
                 ('eCTRL Node', 'eCTRL Node'), ('EPPSM Node', 'EPPSM Node'),
                 ('GRouter Node', 'GRouter Node'),
                 )


class CurrentApplicationConfigurationManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return ApplicationConfiguration.objects.none()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_application_config(
            self, project, application_name, deployOption, olh_penetration=1):

        project_information_list = ProjectInformation.current_objects.all()

        if project_information_list.count() > 0:
            project_information = project_information_list[0]
            active_subscriber = project_information.activeSubscriber * olh_penetration
            inactive_subscriber = project_information.inactiveSubscriber * olh_penetration
        else:
            active_subscriber = 0
            inactive_subscriber = 0

        application_config = self.create(
            project=project,
            applicationName=application_name,
            deployOption=deployOption,
            activeSubscriber=active_subscriber,
            inactiveSubscriber=inactive_subscriber,
        )
        return application_config

class ApplicationConfiguration(models.Model):
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

    trafficBHTA = models.FloatField(default=0)
    serverCPUCost = models.FloatField(default=0)
    clientCPUCost = models.FloatField(default=0)
    totalCPUCost = models.FloatField(default=0)
    cpuCostForRoutingClient = models.FloatField(default=0)
    ss7CPUCost = models.FloatField(default=0)
    tcpCPUCost = models.FloatField(default=0)
    diamCPUCost = models.FloatField(default=0)
    aprocCPUCost = models.FloatField(default=0)  # APROC
    aprocRoutingCost = models.FloatField(default=0)
    asdCPUCost = models.FloatField(default=0)  # Aerospike Server
    asdMateCost = models.FloatField(default=0)
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
    counterMemory = models.FloatField(default=0)

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

    systemNumber = models.FloatField(default=0)

    boundType = models.CharField(max_length=20, choices=BOUND_TYPE_OPTION,
                                 default='CPU Bound', verbose_name='Bound Type')

    objects = models.Manager()  # The default manager.
    current_objects = CurrentApplicationConfigurationManager()  # The current project specific manager.

    current_application_information = None
    traffic_information_list = None
    project_information = None
    application_db_list = None
    app_config = None

    def __str__(self):
        if hasattr(self, 'project'):
            return self.project.name + '_' + self.applicationName.name
        else:
            if WorkingProject.objects.all().count() > 0:
                return WorkingProject.objects.all()[0].project.name + '_' + self.applicationName.name
            else:
                return self.applicationName.name

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps_for_ectrl(self):
        self.traffic_information_list = self.get_traffic_information_list(application_name='EPAY')

        tps = 0
        for traffic_information in self.traffic_information_list:
            if traffic_information.callType.type == 'Voice':
                tps += traffic_information.trafficTPS

        tps = float('%.04f'%tps)
        return tps

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps_for_epay(self):
        self.traffic_information_list = self.get_traffic_information_list(application_name='EPAY')

        tps = 0
        for traffic_information in self.traffic_information_list:
            tps += traffic_information.trafficTPS

        tps = float('%.04f'%tps)
        return tps

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps_for_eppsm(self):
        olh_config_list = FeatureConfiguration.current_objects.all().filter(
            feature__name='Online Hierarchy',
        )

        if olh_config_list.count() > 0:
            epay_tps = self.get_tps_for_epay()
            tps = epay_tps * olh_config_list[0].featurePenetration / 100
        else:
            tps = 0

        tps = float('%.04f'%tps)
        return tps

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps_for_drouter(self):
        self.traffic_information_list = self.get_traffic_information_list(application_name='EPAY')

        tps = 0
        for traffic_information in self.traffic_information_list:
            if traffic_information.callType.type == 'Diameter':
                tps += traffic_information.trafficTPS

        tps = float('%.04f'%tps)
        return tps

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_tps_for_group(self):
        self.traffic_information_list = self.get_traffic_information_list(
            application_name='EPAY')

        tps = 0
        for traffic_information in self.traffic_information_list:
            if traffic_information.callType.name == 'GPRS/Diameter Session Contribution':
                total_bhca = traffic_information.get_total_bhca_for_diameter_session()
                if total_bhca > 0:
                    group_transaction_number = ((traffic_information.volumeCCRiBHTA + traffic_information.timeCCRiBHTA) *
                           traffic_information.callType.groupTransactionNumber +
                           (traffic_information.volumeCCRuBHTA + traffic_information.timeCCRuBHTA) *
                           traffic_information.callType.groupTransactionNumber2 +
                           (traffic_information.volumeCCRtBHTA + traffic_information.timeCCRtBHTA) *
                           traffic_information.callType.groupTransactionNumber3) / total_bhca
                    tps += traffic_information.trafficTPS * group_transaction_number
            else:
                tps += traffic_information.trafficTPS * traffic_information.callType.groupTransactionNumber

        tps = float('%.04f'%tps)
        return tps

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_current_application_information(self):
        current_application_information_list = ApplicationInformation.objects.all().filter(
            release=self.project.release,
            application=self.applicationName,
        )
        if current_application_information_list.count() > 0:
            return current_application_information_list[0]

        return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_release_impact(self, impact_per_release):
        if (self.project_information is not None) and (self.project_information.numberReleaseToEstimate > 0):
            return pow(1 + impact_per_release / 100, self.project_information.numberReleaseToEstimate)

        return 1

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_traffic_information_list(self, application_name=''):
        if application_name == '':
            application_name = self.applicationName.name
        if application_name == 'EPAY':
            return TrafficInformation.current_objects.all().filter(
                callType__isShow=True,
            )
        elif application_name == 'Group':
            return TrafficInformation.current_objects.all().filter(
                callType__name='Group side transaction for OH',
            )
        elif application_name== 'DRouter':
            return TrafficInformation.current_objects.all().filter(
                callType__name='DRouter transaction',
            )
        elif application_name == 'EPPSM':
            return TrafficInformation.current_objects.all().filter(
                callType__name='EPPSM transaction',
            )
        elif application_name == 'eCTRL':
            return TrafficInformation.current_objects.all().filter(
                callType__name='eCTRL call',
            )
        else:
            return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_io_node_number_needed(self):
        self.ss7BaseIONodeNumber = self.get_ss7_io_node_number()
        self.ldapBaseIONodeNumber = self.get_ldap_io_node_number()
        self.diameterBaseIONodeNumber = self.get_diameter_io_node_number()

        return max([self.ss7BaseIONodeNumber, self.ldapBaseIONodeNumber, self.diameterBaseIONodeNumber])

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ss7_io_node_number(self):
        traffic_tps = 0
        io_node_number = 0
        if self.applicationName.name == 'EPAY':
            for traffic in self.traffic_information_list:
                if traffic.callType.type == 'Voice':
                    traffic_tps += traffic.trafficTPS
        elif self.applicationName.name == 'eCRTL':
            for traffic in self.traffic_information_list:
                traffic_tps += traffic.trafficTPS

        if self.project.hardwareModel.defaultCPUNumber > 0:
            io_node_capacity = self.project.hardwareModel.maxSIGTRANPerIONode * \
                               math.sqrt(self.project_information.ioCPUNumber /
                                         self.project.hardwareModel.defaultCPUNumber)

            if io_node_capacity > 0:
                io_node_number = traffic_tps / io_node_capacity

        io_node_number = float('%.04f'%io_node_number)

        return io_node_number

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ldap_io_node_number(self):
        traffic_tps = 0
        io_node_number = 0
        if self.applicationName.name == 'EPAY':
            for traffic in self.traffic_information_list:
                if traffic.callType.type == 'Diameter' or traffic.callType.type == 'LDAP':
                    traffic_tps += traffic.trafficTPS
        else:
            for traffic in self.traffic_information_list:
                traffic_tps += traffic.trafficTPS

        if self.project.hardwareModel.defaultCPUNumber > 0:
            io_node_capacity = self.project.hardwareModel.maxLDAPPerIONode * \
                               math.sqrt(self.project_information.ioCPUNumber /
                                         self.project.hardwareModel.defaultCPUNumber)

            if io_node_capacity > 0:
                io_node_number = traffic_tps / io_node_capacity

        io_node_number = float('%.04f'%io_node_number)

        return io_node_number

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_diameter_io_node_number(self):
        traffic_tps = 0
        io_node_number = 0
        if self.applicationName.name == 'EPAY':
            for traffic in self.traffic_information_list:
                if traffic.callType.type == 'Diameter':
                    traffic_tps += traffic.trafficTPS
        elif self.applicationName.name == 'DRouter':
            for traffic in self.traffic_information_list:
                traffic_tps += traffic.trafficTPS

        if self.project.hardwareModel.defaultCPUNumber > 0:
            io_node_capacity = self.project.hardwareModel.maxDiameterPerIONode * \
                               math.sqrt(self.project_information.ioCPUNumber / self.project.hardwareModel.defaultCPUNumber)

            if io_node_capacity > 0:
                io_node_number = traffic_tps / io_node_capacity

        io_node_number = float('%.04f'%io_node_number)

        return io_node_number

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_node_number_needed(self):
        if self.cpuBaseNodeNumber >= self.memoryBaseNodeNumber:
            self.nodeNumberNeeded = self.cpuBaseNodeNumber
            self.boundType = 'CPU Bound'
        else:
            self.nodeNumberNeeded = self.memoryBaseNodeNumber
            self.boundType = 'Memory Bound'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_project_information(self):
        if ProjectInformation.current_objects.all().count() > 0:
            return ProjectInformation.current_objects.all()[0]
        return None

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_cpu_budget_per_node(self):
        if self.project_information is None:
            return 0

        if self.project is None:
            return 0

        max_client_cpu_usage = self.project_information.cpuUsageTuning.clientCPUUsage

        if self.project.hardwareModel.hardwareType.isVM:
            client_number = self.project_information.cpuNumber.clientNumber
            if self.project.database_type.name == 'NDB':
                if (self.ndbCPULimitation > 0) and (self.ndbCPULimitation < max_client_cpu_usage):
                    max_client_cpu_usage = self.ndbCPULimitation
        else:
            client_number = self.project.hardwareModel.defaultClientNumber

        capacity_ratio = self.project_information.cpuNumber.capacityRatio

        vm_capacity = self.project_information.vmType.capacity

        cpu_single_thread_capacity = self.project.hardwareModel.cpu.singleThreadCapacity

        cpu_budget = client_number * 1000 * max_client_cpu_usage * capacity_ratio * \
                     vm_capacity * cpu_single_thread_capacity

        return cpu_budget

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_memory_budget_per_app_node(self):
        if self.project_information is None:
            return 0

        return self.project_information.memory.memory * 1024 * \
               self.project_information.memoryUsageTuning.memoryUsageTuning - \
               self.get_initial_memory_per_node()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_memory_budget_per_db_node(self):
        if self.project_information is None:
            return 0

        return self.project_information.dbMemory.memory * 1024 *\
               self.project_information.memoryUsageTuning.memoryUsageTuning

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_application_db_list(self):
        if self.applicationName.name == 'EPAY':
            application_db_list = DBConfiguration.current_objects.all().filter(
                application=self.applicationName,
                memberGroupOption='Member',
            )
        elif self.applicationName.name == 'Group':
            application_list = ApplicationName.objects.all().filter(
                name='EPAY',
            )
            if application_list.count() > 0:
                application_db_list = DBConfiguration.current_objects.all().filter(
                    application=application_list[0],
                    memberGroupOption='Group',
                )
            else:
                raise ValidationError('Application EPAY not configured!')
        else:
            application_db_list = DBConfiguration.current_objects.all().filter(
                application=self.applicationName
            )

        return application_db_list

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_db_memory(self):
        if self.application_db_list is None:
            return 0

        db_total_cache_size = 0
        for db in self.application_db_list:
            db.cacheSize = db.get_cache_size()
            db_total_cache_size += db.cacheSize
            db.save()

        return db_total_cache_size

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_db_todo_log_size(self):
        if self.application_db_list is None:
            return 0

        db_total_todo_log_size = 0
        for db in self.application_db_list:
            db.todoLogSize = db.get_todo_log_size()
            db_total_todo_log_size += db.get_todo_log_size()
            db.save()

        return db_total_todo_log_size

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_db_mate_log_size(self):
        if self.application_db_list is None:
            return 0

        db_total_mate_log_size = 0
        for db in self.application_db_list:
            db.mateLogSize = db.get_mate_log_size()
            db_total_mate_log_size += db.get_mate_log_size(self.trafficTPS)
            db.save()

        return db_total_mate_log_size

    def init_calc_fields_for_non_sll_application(self):
        self.serverCPUCost = 0
        self.clientCPUCost = 0
        self.totalCPUCost = 0
        self.cpuCostForRoutingClient = 0
        self.ss7CPUCost = 0
        self.tcpCPUCost = 0
        self.diamCPUCost = 0
        self.aprocCPUCost = 0
        self.aprocRoutingCost = 0
        self.asdCPUCost = 0
        self.asdMateCost = 0

        self.spaDataSize = 0

        self.ss7InSizePerSecond = 0
        self.ss7OutSizePerSecond = 0
        self.ldapSizePerSecond = 0
        self.diameterSizePerSecond = 0
        self.muTCPSize = 0
        self.featureSS7InSize = 0
        self.featureSS7OutSize = 0
        self.featureLDAPSize = 0
        self.featureDiameterSize = 0

        self.ndbCPULimitation = 0

        self.featureCost = 0

        self.counterCost = 0
        self.groupCounterCost = 0
        self.totalCPUCost = 0
        self.miscCPUCost = 0

        self.systemNumber = 0

        if self.project_information is None:
            self.project_information = self.get_project_information()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def init_calc_fields(self):
        self.serverCPUCost = 0
        self.clientCPUCost = 0
        self.totalCPUCost = 0
        self.cpuCostForRoutingClient = 0
        self.ss7CPUCost = 0
        self.tcpCPUCost = 0
        self.diamCPUCost = 0
        self.aprocCPUCost = 0
        self.aprocRoutingCost = 0
        self.asdCPUCost = 0
        self.asdMateCost = 0

        self.spaDataSize = 0

        self.ss7InSizePerSecond = 0
        self.ss7OutSizePerSecond = 0
        self.ldapSizePerSecond = 0
        self.diameterSizePerSecond = 0
        self.muTCPSize = 0
        self.featureSS7InSize = 0
        self.featureSS7OutSize = 0
        self.featureLDAPSize = 0
        self.featureDiameterSize = 0

        self.ndbCPULimitation = 0
        self.trafficTPS = 0
        self.trafficBHTA = 0

        self.featureCost = 0

        self.counterCost = 0
        self.groupCounterCost = 0
        self.totalCPUCost = 0
        self.miscCPUCost = 0

        self.systemNumber = 0

        self.current_application_information = self.get_current_application_information()
        self.traffic_information_list = self.get_traffic_information_list()
        self.project_information = self.get_project_information()
        self.application_db_list = self.get_application_db_list()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_config_for_non_sll_application(self):
        config_list_for_non_sll_application = OtherApplicationInformation.objects.all().filter(
            application=self.applicationName,
            hardwareModel=self.project.hardwareModel,
        )
        if config_list_for_non_sll_application.count() > 0:
            return config_list_for_non_sll_application[0]

        raise ValidationError('Application: %s and Hardware Model: %s not provisioned in '
                              'OtherApplicationInformation table!' % (self.applicationName, self.project.hardwareModel))

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_cost_for_non_sll_application(self):
        if self.project_information is None:
            raise ValidationError('Project Information for the project is not configured!')

        if self.trafficTPS <= 0:
            return 0

        client_number = self.get_client_num_for_non_sll_application()

        call_cost = client_number * 1000 * self.project_information.cpuUsageTuning.clientCPUUsage * \
                    self.project.hardwareModel.cpu.singleThreadCapacity
        return call_cost

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_client_num_for_non_sll_application(self):
        if self.app_config.maxTrafficPerNode > 0:
            needed_client_number = self.trafficTPS / self.app_config.maxTrafficPerNode * self.app_config.clientNumber
            if needed_client_number < self.app_config.minClient:
                needed_client_number = self.app_config.minClient

            return math.ceil(needed_client_number)

        raise ValidationError('maxTrafficPerNode in OtherApplicationInformation table is <= 0!')

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_system_for_non_sll_application(self):
        if self.app_config.maxNodePerSystem > 0 and self.app_config.maxTrafficPerNode > 0:
            system_number = self.trafficTPS / (self.app_config.maxTrafficPerNode * self.app_config.maxNodePerSystem)
        else:
            system_number = 0

        return math.ceil(system_number)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate_for_non_sll_application(self):
        self.init_calc_fields_for_non_sll_application()

        self.app_config = self.get_config_for_non_sll_application()
        self.cpuBudget = self.get_cpu_budget_per_node()

        self.cpuBaseNodeNumber = self.get_cost_for_non_sll_application() / self.cpuBudget
        self.cpuBaseNodeNumber = float('%.04f'%self.cpuBaseNodeNumber)
        self.systemNumber = self.get_system_for_non_sll_application()

        self.save()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate_for_sll_application(self):
        self.init_calc_fields()

        for traffic in self.traffic_information_list:
            traffic.calculate_for_traffic()
            self.serverCPUCost += traffic.serverCPUCost
            self.clientCPUCost += traffic.cpuCostPerCall * traffic.trafficTPS
            #self.totalCPUCost += traffic.totalCPUCost
            self.cpuCostForRoutingClient += traffic.cpuCostForRoutingClient
            self.ss7CPUCost += traffic.ss7CPUCost
            self.tcpCPUCost += traffic.tcpCPUCost
            self.diamCPUCost += traffic.diamCPUCost
            self.aprocCPUCost += traffic.aprocCPUCost
            self.aprocRoutingCost += traffic.aprocRoutingCost
            self.asdCPUCost += traffic.asdCPUCost
            self.asdMateCost += traffic.asdMateCost

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
            self.trafficBHTA += traffic.trafficBHTA

            self.featureCost += traffic.featureCost

            self.counterCost += traffic.counterCost
            self.groupCounterCost += traffic.groupCounterCost

        self.miscCPUCost = self.serverCPUCost + self.ss7CPUCost + self.tcpCPUCost + \
                           self.diamCPUCost + self.aprocRoutingCost  + self.aprocCPUCost + \
                           self.asdMateCost + self.asdCPUCost

        self.totalCPUCost = self.clientCPUCost + self.featureCost + self.counterCost



        if self.trafficTPS > 0:
            self.ndbCPULimitation = self.ndbCPULimitation / self.trafficTPS
        else:
            self.ndbCPULimitation = 0

        self.cpuBudget = self.get_cpu_budget_per_node()
        self.cpuBaseNodeNumber = self.get_cpu_based_node_number()

        self.memoryBaseNodeNumber, self.dbNodeNumberNeeded = self.get_memory_based_node_number()

        self.get_node_number_needed()
        self.ioNodeNumberNeeded = self.get_io_node_number_needed()

        self.save()

    def get_group_call_cost_record(self):
        pass

    def calculate_for_group(self):
        self.init_calc_fields()



        # group_call_cost_record_list =
        pass

    def calculate_for_drouter(self):
        pass

    def calculate_for_ectrl(self):
        pass

    def calculate_for_eppsm(self):
        pass

    def calculate_for_others(self):
        pass

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_cpu_based_node_number(self):
        cpu_base_node_number = self.clientCPUCost * \
                self.get_release_impact(self.project_information.cpuImpactPerRelease) / self.cpuBudget

        cpu_base_node_number = float('%.04f'%cpu_base_node_number)

        return cpu_base_node_number

    def get_initial_memory_per_node(self):
        if self.current_application_information is None:
            return 0

        return self.current_application_information.initialDataSize * \
               self.project_information.clientNumber / BYTES_TO_MILLION

    def get_ndb_db_actual_memory(self):
        if self.project.release is not None and self.project.release.ndbStopWriteRatio > 0:
            return self.get_db_memory() / self.project.release.ndbStopWriteRatio

        return self.get_db_memory() / 0.8

    def get_memory_based_node_number(self):
        if self.project.hardwareType.isSingleServer or ((self.project.database_type.name == 'NDB') and
                (self.project_information.NDB_DEPLOY_OPTION == 'Combo')):
            if self.project.database_type.name == 'NDB':
                if self.project.hardwareType.isSingleServer:
                    app_memory = self.spaDataSize + self.get_ndb_db_actual_memory()
                else:
                    app_memory = self.spaDataSize + self.get_ndb_db_actual_memory() * 2
            else:
                app_memory = self.spaDataSize + self.get_db_memory()
            db_memory = 0
        else:
            db_memory = self.get_db_memory()
            app_memory = self.spaDataSize

        memory_based_app_node = app_memory / self.get_memory_budget_per_app_node()
        memory_based_app_node = float('%.04f'%memory_based_app_node)

        memory_based_db_node = db_memory / self.get_memory_budget_per_db_node()
        memory_based_db_node = float('%.04f'%memory_based_db_node)

        return (memory_based_app_node, memory_based_db_node)

    def get_io_based_node_number(self):
        pass

    def get_ss7_based_node_number(self):
        pass

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_client_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic.get_total_cost()

        return total_call_cost

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_sever_cpu_cost(self):
        if self.current_application_information is not None:
            total_call_cost = 0

            for traffic in self.traffic_information_list:
                total_call_cost += self.current_application_information.cpuCostForServer * traffic.trafficTPS

            return total_call_cost

        return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def tcp_cpu_cost(self):
        if WorkingProject.objects.count() == 0:
            return 0

        total_call_cost = 0
        for traffic in self.traffic_information_list:
            total_call_cost += traffic.tcpCPUCost
            logger.g_logger.info('tcpCPUCost: %s, total_call_cost: %s' % (traffic.tcpCPUCost, total_call_cost))

        return total_call_cost

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def ss7_cpu_cost(self):
        if self.current_application_information is not None:
            total_call_cost = 0

            for traffic in self.traffic_information_list:
                total_call_cost += traffic.ss7CPUCost

            return total_call_cost

        return 0

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def misc_cpu_cost(self):
        return self.ss7_cpu_cost + self.tcp_cpu_cost + self.db_cpu_cost + self.total_sever_cpu_cost

    @property
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def total_cpu_cost(self):
        return self.misc_cpu_cost + self.total_client_cpu_cost

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_app_memory(self):
        pass

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_db_cache_size(self):
        pass

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_ama_disk_size(self):
        pass

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_total_db_disk_size(self):
        pass

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_ama_record_per_second(self):
        pass

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def validate_unique(self, exclude=None):
        if (not self.id) and WorkingProject.objects.all().count() > 0:
            qs = ApplicationConfiguration.objects.filter(project=WorkingProject.objects.all()[0].project)
            if qs.filter(applicationName=self.applicationName).exists():
                raise ValidationError('Application: %s existed!' % self.applicationName)

    class Meta:
        verbose_name = 'Application Configuration'
        verbose_name_plural = 'Application Configuration'


class CurrentCalculatedResultManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_calculated_result(
            self, project, application_name, app_node_number,
            db_node_number, io_node_number, cal_cpu_app_number,
            cal_mem_app_number, cal_db_number, cal_io_number):
        calculated_result = self.create(
            project=project,
            applicationName=application_name,
            calCPUAppNumber=cal_cpu_app_number,
            calMemAppNumber=cal_mem_app_number,
            calDBNumber=cal_db_number,
            calIONumber=cal_io_number,
            appNodeNumber=app_node_number,
            dbNodeNumber=db_node_number,
            ioNodeNumber=io_node_number,
        )
        return calculated_result

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    calCPUAppNumber = models.FloatField(default=0, verbose_name='Calculated App Node Number (CPU Based)')
    calMemAppNumber = models.FloatField(default=0, verbose_name='Calculated App Node Number (Memory Based)')
    calDBNumber = models.FloatField(default=0, verbose_name='Calculated DB Node Number')
    calIONumber = models.FloatField(default=0, verbose_name='Calculated IO Node Number')

    appNodeNumber = models.IntegerField(default=0, verbose_name='App Node Number')
    dbNodeNumber = models.IntegerField(default=0, verbose_name='DB Node Number')
    ioNodeNumber = models.IntegerField(default=0, verbose_name='IO Node Number')

    systemNumber = models.IntegerField(default=0, verbose_name='System Number')

    boundType = models.CharField(max_length=20, choices=BOUND_TYPE_OPTION,
                                 default='-', verbose_name='Bound Type')

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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_dimensioning_result(
            self, project, application_name,
            calculated_app_node_number,
            calculated_db_node_number,
            calculated_io_node_number,
            calculated_system_number,
            bound_type):
        dimensioning_result = self.create(
            project=project,
            applicationName=application_name,
            calculated_app_node_number = calculated_app_node_number,
            calculated_db_node_number = calculated_db_node_number,
            calculated_io_node_number = calculated_io_node_number,
            calculated_system_number = calculated_system_number,
            bound_type = bound_type,
        )
        return dimensioning_result

class DimensioningResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    applicationName = models.ForeignKey(
        ApplicationName,
        on_delete=models.CASCADE,
        verbose_name='Application Name'
    )

    systemNumber = models.IntegerField(default=0, verbose_name='System Number')
    appNodeNeededNumber = models.IntegerField(default=0, verbose_name='APP Node Number')
    dbNodeNeededNumber = models.IntegerField(default=0, verbose_name='DB Node Number')
    ioNodeNeededNumber = models.IntegerField(default=0, verbose_name='IO Node Number')
    pilotNodeNeededNumber = models.IntegerField(default=0, verbose_name='Pilot Node Number')
    mateNodeNeededNumber = models.IntegerField(default=0, verbose_name='Mate Node Number')
    totalNodeNeededNumber = models.IntegerField(default=0, verbose_name='Total Node Number')

    averageClientCPUUsage = models.FloatField(default=0, verbose_name='Needed APP Node Number')
    dbCacheSize = models.FloatField(default=0, verbose_name='DB Cache Size (MB)')  # MB
    totalMemoryUsage = models.FloatField(default=0, verbose_name='Total Memory Usage (MB)')  # MB
    sigtranSpeed = models.FloatField(default=0, verbose_name='SIGTRAN Speed (Byte/S)')  # Byte/Second
    ethernetPortsRequiredNumber = models.IntegerField(default=0, verbose_name='Ethernet Ports Required Number')
    totalTCPUDPSpeed = models.FloatField(default=0, verbose_name='Total TCP/UDP Speed (Byte/S)')  # Byte/Second
    amaRecordNumberPerSecond = models.FloatField(default=0, verbose_name='AMA Record Number Per Second')
    dialyBillingFileSize = models.FloatField(default=0, verbose_name='Billing File Size Per Day (MB)')  # MB
    amaRetrieveSpeed = models.FloatField(default=0, verbose_name='AMA Retrieve Speed (Byte/S)')  # Byte/Second
    ladpDiameterUDP = models.FloatField(default=0, verbose_name='LDAP/Diameter Speed (Byte/S)')  # Byte/Second
    muSpeed = models.FloatField(default=0, verbose_name='Mate Update Speed (Byte/S)')  # Byte/Second

    memoryUsagePerAppNode = models.FloatField(default=0, verbose_name='Memory Usage Per App Node (MB)')  # MB
    memoryUsagePerClient = models.FloatField(default=0, verbose_name='Memory Usage Per Client (MB)')  # MB
    appNodeMemoryUsagePercent = models.FloatField(default=0, verbose_name='App Node Memory Usage (%)')  # %

    pilotSharedDiskSize = models.FloatField(default=0, verbose_name='Pilot Shared Disk Size (MB)')  # MB
    dbDiskSizeForMateUpdate = models.FloatField(default=0, verbose_name='Disk Size For Mate Update (MB)')  # MB
    diskSizeForDB = models.FloatField(default=0, verbose_name='Disk Size For DB (MB)')  # MB

    objects = models.Manager()  # The default manager.
    current_objects = CurrentDimensioningResultManager()  # The current project specific manager.

    calculated_app_node_number = models.IntegerField(default=0)
    calculated_db_node_number = models.IntegerField(default=0)
    calculated_io_node_number = models.IntegerField(default=0)
    calculated_system_number = models.IntegerField(default=0)
    bound_type = models.CharField(max_length=20, default='-')

    db_node_number_per_system = 0
    app_node_number_per_system = 0
    io_node_number_per_system = 0
    pilot_node_number_per_system = 0
    mate_node_number_per_system = 0

    project_information = None

    system_configuration = None
    application_configuration = None


    class Meta:
        verbose_name = 'Dimensioning Result'
        verbose_name_plural = 'Dimensioning Result'

    def __str__(self):
        return self.applicationName.name

    def get_system_configuration(self, application_name):
        system_configuration_list = SystemConfiguration.current_objects.all().filter(
            applicationName=application_name
        )

        if system_configuration_list.count() > 0:
            return system_configuration_list[0]
        else:
            return None

    def get_application_configuration(self, application_name):
        application_configuration_list = ApplicationConfiguration.current_objects.all().filter(
            applicationName=application_name,
        )
        if application_configuration_list.count() > 0:
            return application_configuration_list[0]
        raise ValidationError('Application Configuration not configured for application: %s.'%application_name)

    def get_project_information(self):
        if ProjectInformation.current_objects.all().count() > 0:
            return ProjectInformation.current_objects.all()[0]

        raise ValidationError('Project Information not configured for the project')

    def init_calc_fields(self):
        self.system_configuration = self.get_system_configuration(self.applicationName)
        self.application_configuration = self.get_application_configuration(self.applicationName)
        self.project_information = self.get_project_information()


    def get_sys_num_for_with_db_node(self):
        max_allowed_db_node = self.project.hardwareModel.maxDBNodeNumber
        self.mate_node_number_per_system = 0

        max_allowed_app_node = self.project.hardwareModel.maxAppNodeNumber

        total_node = self.project.hardwareModel.maxNodeNumber

        if self.system_configuration is not None:
            backup_app_node_number = self.system_configuration.backupAppNodeNumberPerSystem
            spare_app_node_number = self.system_configuration.spareAppNodeNumberPerSystem
            backup_db_node_number = self.system_configuration.backupDBNodeNumberPerSystem
            spare_db_node_number = self.system_configuration.spareAppNodeNumberPerSystem
        else:
            backup_app_node_number = 0
            spare_app_node_number = 0
            backup_db_node_number = 0
            spare_db_node_number = 0

        total_spare_node = backup_app_node_number + spare_app_node_number + backup_db_node_number + spare_db_node_number

        max_allowed_db_node = max_allowed_db_node - (backup_db_node_number + spare_db_node_number)
        if max_allowed_db_node < 2:
            raise ValidationError('Backup/Spare db node number is configured too large for application: %s'
                                  %self.applicationName)

        sys_num_for_db = math.ceil(self.calculated_db_node_number * 2 / max_allowed_db_node)

        # At least 1 DB node pair, 1 pliot node pair and 1 IO node pair
        max_allowed_app_node = total_node - (2 + 2 + 2) - total_spare_node
        if max_allowed_app_node < 1:
            raise ValidationError('Backup/Spare app node number is configured too large for application: %s'
                                  %self.applicationName)

        sys_num_for_app = math.ceil(self.calculated_app_node_number / max_allowed_app_node)

        # At least 1 DB node pair, 1 pilot node pair and 1 app node
        max_allowed_io_node = total_node - (2 + 2 + 1) - total_spare_node
        if self.project.hardwareModel.maxIONodeNumber > 0 and \
                        max_allowed_io_node > self.project.hardwareModel.maxIONodeNumber:
            max_allowed_io_node = self.project.hardwareModel.maxIONodeNumber
            sys_num_for_io = math.ceil(self.calculated_io_node_number * 2 / max_allowed_io_node)
        else:
            sys_num_for_io = math.ceil(self.calculated_io_node_number)

        sys_num = max([sys_num_for_db, sys_num_for_app, sys_num_for_io])

        if sys_num > 0:
            while True:
                app_num = math.ceil(self.calculated_app_node_number / sys_num)
                db_num = math.ceil(self.calculated_db_node_number / sys_num)
                io_num = math.ceil(self.calculated_db_node_number / sys_num)

                max_app_num = total_node - 2 - io_num * 2 - db_num * 2 - total_spare_node
                max_db_num = total_node - 2 - io_num * 2 - app_num - total_spare_node
                max_io_num = total_node - 2 - db_num * 2 - app_num - total_spare_node

                if (app_num > max_app_num) or (db_num > max_db_num) or (io_num > max_io_num):
                    sys_num += 1
                else:
                    break

        return sys_num

    def get_sys_num_for_without_db_node(self):
        max_allowed_app_node = self.project.hardwareModel.maxAppNodeNumber

        total_node = self.project.hardwareModel.maxNodeNumber

        if self.calculated_app_node_number < self.calculated_db_node_number:
            self.calculated_app_node_number = self.calculated_db_node_number

        self.calculated_db_node_number = 0

        if self.system_configuration is not None:
            backup_app_node_number = self.system_configuration.backupAppNodeNumberPerSystem
            spare_app_node_number = self.system_configuration.spareAppNodeNumberPerSystem

        else:
            backup_app_node_number = 0
            spare_app_node_number = 0


        total_spare_node = backup_app_node_number + spare_app_node_number

        # At least 1 pliot node pair and 1 IO node pair
        max_allowed_app_node = total_node - (2 + 2) - total_spare_node
        if max_allowed_app_node < 1:
            raise ValidationError('Backup/Spare app node number is configured too large for application: %s'
                                  %self.applicationName)

        sys_num_for_app = math.ceil(self.calculated_app_node_number / max_allowed_app_node)

        # At least 1 pilot node pair and 1 app node
        max_allowed_io_node = total_node - (2 + 1) - total_spare_node
        if self.project.hardwareModel.maxIONodeNumber > 0 and \
                        max_allowed_io_node > self.project.hardwareModel.maxIONodeNumber:
            max_allowed_io_node = self.project.hardwareModel.maxIONodeNumber
            sys_num_for_io = math.ceil(self.calculated_io_node_number * 2 / max_allowed_io_node)
        else:
            sys_num_for_io = math.ceil(self.calculated_io_node_number)

        sys_num = max([sys_num_for_app, sys_num_for_io])

        if sys_num > 0:
            while True:
                app_num = math.ceil(self.calculated_app_node_number / sys_num)
                io_num = math.ceil(self.calculated_io_node_number / sys_num)

                max_app_num = total_node - 2 - io_num * 2 - total_spare_node
                max_io_num = total_node - 2 - app_num - total_spare_node

                if (app_num > max_app_num) or (io_num > max_io_num):
                    sys_num += 1
                else:
                    break

            tps_per_system = self.application_configuration.trafficTPS / sys_num
            if tps_per_system > self.project.release.trafficRequireDedicateMate:
                self.mate_node_number_per_system += 2
                max_allowed_app_node -= self.mate_node_number_per_system
                if max_allowed_app_node > 0:
                    sys_num_for_app = math.ceil(self.calculated_app_node_number / max_allowed_app_node)
                else:
                    raise ValidationError("Can't calculate system number, please check!")

                if sys_num < sys_num_for_app:
                    sys_num = sys_num_for_app

                while self.mate_node_number_per_system < 8:
                    tps_per_system = self.application_configuration.trafficTPS / sys_num
                    if tps_per_system > self.project.release.capacityPerNDBMateVhost:
                        self.mate_node_number_per_system += 2
                        max_allowed_app_node -= self.mate_node_number_per_system
                        if max_allowed_app_node > 0:
                            sys_num_for_app = math.ceil(self.calculated_app_node_number / max_allowed_app_node)
                        else:
                            raise ValidationError("Can't calculate system number, please check!")

                        if sys_num < sys_num_for_app:
                            sys_num = sys_num_for_app
                    else:
                        break

                while True:
                    app_num = math.ceil(self.calculated_app_node_number / sys_num)
                    io_num = math.ceil(self.calculated_io_node_number / sys_num)

                    max_app_num = total_node - 2 - io_num * 2 - total_spare_node
                    max_io_num = total_node - 2 - app_num - total_spare_node

                    if (app_num > max_app_num) or (io_num > max_io_num):
                        sys_num += 1
                    else:
                        break

        return sys_num

    def calculate_system_number(self):
        if self.project.hardwareModel is None:
            raise ValidationError('Hardware Model not configured for the project')

        sys_num = 0
        if self.project.hardwareType.isSingleServer == False:
            if self.project.database_type == 'RTDB' or self.project_information.NDB_DEPLOY_OPTION == 'Individual':
                sys_num = self.get_sys_num_for_with_db_node()

            else:
                sys_num = self.get_sys_num_for_without_db_node()

        return sys_num

    def calculate_for_each_system(self):
        app_num = int(math.ceil(self.calculated_app_node_number / self.systemNumber))
        db_num = int(math.ceil(self.calculated_db_node_number / self.systemNumber)) * 2
        io_num = int(math.ceil(self.calculated_io_node_number / self.systemNumber)) * 2

        total_num = app_num + db_num + io_num + self.mate_node_number_per_system + 2 # 2 nodes for pilot

        for i in range(1, self.systemNumber):
            dimensioning_result_per_system = DimensioningResultPerSystem.current_objects.\
                create_dimensioning_result_per_system(
                self.project,
                self.applicationName,
                app_num,
                db_num,
                io_num,
                2,
                self.mate_node_number_per_system,
                total_num,
                i,
            )

        last_app_num = self.calculated_app_node_number - app_num * (self.systemNumber - 1)
        if last_app_num < 1:
            last_app_num = 1
        last_db_num = self.calculated_db_node_number * 2 - db_num * (self.systemNumber - 1)
        if self.calculated_db_node_number > 0 and last_db_num < 2:
            last_db_num = 2
        last_io_num = self.calculated_io_node_number * 2 - io_num * (self.systemNumber - 1)
        if last_io_num < 2:
            last_io_num = 2

        if db_num > 0:
            app_db_node_ratio1 = app_num / db_num
            app_db_node_ratio2 = last_app_num / last_db_num
        else:
            app_db_node_ratio1 = 0
            app_db_node_ratio2 = 0

        app_io_node_ratio1 = app_num / io_num
        app_io_node_ratio2 = last_app_num / last_io_num

        # Adjust DB/APP node for last system
        while app_db_node_ratio1 > 0 and (math.fabs(app_db_node_ratio1 - app_db_node_ratio2) / app_db_node_ratio1 >
            ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM) and ((last_app_num < app_num) or (last_db_num < db_num)):
            if app_db_node_ratio1 > app_db_node_ratio2:
                if (db_num > 2):
                    while (math.fabs(app_db_node_ratio1 - app_db_node_ratio2) / app_db_node_ratio1 >
                               ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM) and (last_app_num < app_num):
                        last_app_num += 1
                        app_db_node_ratio2 = last_app_num / last_db_num
            else:
                if (app_num > 1):
                    while (math.fabs(app_db_node_ratio1 - app_db_node_ratio2) / app_db_node_ratio1 >
                               ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM) and (last_db_num < db_num):
                        last_db_num += 2
                        app_db_node_ratio2 = last_app_num / last_db_num

        # Adjust IO/APP node for last system
        while app_io_node_ratio1 > 0 and (math.fabs(app_io_node_ratio1 - app_io_node_ratio2) / app_io_node_ratio1 >
                                              ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM) and ((last_app_num < app_num) or (last_io_num < io_num)):
            if app_io_node_ratio1 > app_io_node_ratio2:
                if (io_num > 2):
                    while (math.fabs(app_io_node_ratio1 - app_io_node_ratio2) / app_io_node_ratio1 >
                               ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM) and (last_app_num < app_num):
                        last_app_num += 1
                        app_io_node_ratio2 = last_app_num / last_io_num
            else:
                if (app_num > 1):
                    while (math.fabs(app_io_node_ratio1 - app_io_node_ratio2) / app_io_node_ratio1 >
                               ALLOWED_DIFFERENCE_FOR_LAST_SYSTEM) and (last_io_num < io_num):
                        last_io_num += 2
                        app_io_node_ratio2 = last_app_num / last_io_num

        last_total_num = last_app_num + last_db_num + last_io_num + self.mate_node_number_per_system + 2 # 2 nodes for pilot
        dimensioning_result_per_system = DimensioningResultPerSystem.current_objects. \
            create_dimensioning_result_per_system(
            self.project,
            self.applicationName,
            last_app_num,
            last_db_num,
            last_io_num,
            2,
            self.mate_node_number_per_system,
            last_total_num,
            self.systemNumber,
        )

        self.appNodeNeededNumber = app_num * (self.systemNumber - 1) + last_app_num
        self.dbNodeNeededNumber = db_num * (self.systemNumber - 1) + last_db_num
        self.ioNodeNeededNumber = io_num * (self.systemNumber - 1) + last_io_num
        self.mateNodeNeededNumber = self.mate_node_number_per_system * self.systemNumber
        self.pilotNodeNeededNumber = 2 * self.systemNumber
        self.totalNodeNeededNumber = total_num * (self.systemNumber - 1) + last_total_num

        self.save()

    def calculate_for_sll_application(self):
        self.init_calc_fields()
        DimensioningResultPerSystem.current_objects.all().delete()
        self.systemNumber = self.calculate_system_number()
        if self.systemNumber > 0:
            self.calculate_for_each_system()
        else:
            raise ValidationError('Calculated System Number is 0!')


    def calculate_for_non_sll_application(self):
        pass


class CurrentDimensioningResultPerSystemManager(models.Manager):
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self):
        if WorkingProject.objects.all().count() > 0:
            return super().get_queryset().filter(
                project=WorkingProject.objects.all()[0].project,
            )

        return DimensioningResultPerSystem.objects.none()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def create_dimensioning_result_per_system(
            self, project, application_name,
            calculated_app_node_number = 0,
            calculated_db_node_number = 0,
            calculated_io_node_number = 0,
            calculated_pilot_node_number = 0,
            calculated_mate_node_number = 0,
            calculated_total_node_number = 0,
            system_sequence = 0,
    ):
        dimensioning_result = self.create(
            project=project,
            applicationName=application_name,
            appNodeNumber = calculated_app_node_number,
            dbNodeNumber = calculated_db_node_number,
            ioNodeNumber = calculated_io_node_number,
            pilotNodeNumber = calculated_pilot_node_number,
            mateNodeNumber = calculated_mate_node_number,
            totalNodeNumber = calculated_total_node_number,
            systemSequence = system_sequence,
        )
        return dimensioning_result

class DimensioningResultPerSystem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    applicationName = models.ForeignKey(
        ApplicationName,
        on_delete=models.CASCADE,
        verbose_name='Application Name'
    )
    systemSequence = models.IntegerField(default=0)

    appNodeNumber = models.IntegerField(default=0)
    dbNodeNumber = models.IntegerField(default=0)
    ioNodeNumber = models.IntegerField(default=2)
    pilotNodeNumber = models.IntegerField(default=2)
    mateNodeNumber = models.IntegerField(default=0)
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
