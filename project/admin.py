from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect
from django import forms
from .models import Project, ProjectInformation, TrafficInformation, FeatureConfiguration, \
    DBConfiguration, CounterConfiguration, CallTypeCounterConfiguration, SystemConfiguration, \
    Customer, WorkingProject, ApplicationConfiguration, CalculatedResult, DimensioningResult, \
    DimensioningResultPerSystem
    # City1, Country, State, Address
    # Province, City, SelectP
from hardware.models import HardwareModel, HardwareType
from service.models import  ApplicationName
from .forms import ProjectForm1, ProjectInformationForm, \
    TrafficInformationForm, FeatureConfigurationForm, CounterConfigurationForm, \
    CallTypeCounterConfigurationForm, DBConfigurationForm, SystemConfigurationForm, ApplicationConfigurationForm
from django.contrib import messages
# from ajax_select import make_ajax_form
# from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline, AjaxSelectAdminStackedInline


class ProjectInline(admin.TabularInline):
    model = Project
    suit_classes = 'suit-tab suit-tab-projects suit-tab-hardwares'

class HardwareModelForm(forms.ModelForm):
    class Meta:
        forms.model = HardwareModel

# class ProjectAdmin(admin.ModelAdmin):
#     #inlines = [HardwareModel, ]
#
#     form = HardwareModelForm
#
#     fieldsets = [
#         (None, {
#             'classes': ('suit-tab', 'suit-tab-general',),
#             'fields': ['release', 'customer', 'version',]
#         }),
#         ('Hardware', {
#             'classes': ('suit-tab', 'suit-tab-general',),
#             'fields': ['hardwareModel', 'vmType', 'cpuNumber', 'memory',
#                        'clientNumber',]}),
#
#         ('Network', {
#             'classes': ('suit-tab', 'suit-tab-general',),
#             'fields': ['sigtranLinkSpeed', 'sigtranLinkNumber', 'sigtranPortUtil',]}),
#         (None, {
#             'classes': ('suit-tab', 'suit-tab-release',),
#             'fields': ['release', 'customer', 'version',]
#         }),
#     ]
#
#     suit_form_tabs = (('general', 'General'), ('release', 'Release Info'))
#     #raw_id_fields =['hardwareModel',]
#     list_display = ('name', 'customer', 'version', 'createTime', 'vmType', 'cpuNumber', 'memory',
#                     'clientNumber', 'sigtranLinkSpeed', 'sigtranLinkNumber', 'sigtranPortUtil',
#                     'amaRecordPerBillingBlock', 'numberReleaseToEstimate', 'cpuImpactPerRelease',
#                     'memoryImpactPerRelease', 'dbImpactPerRelease', 'database_type', 'deploy_option',
#                     'averageAMARecordPerCall', 'amaStoreDay', 'activeSubscriber', 'inactiveSubscriber',
#                     'groupAccountNumber', 'cpuUsageTuning', 'memoryUsageTuning')
#
#     list_filter = ('user', 'release', 'hardwareModel', 'customer', 'vmType', 'database_type')
#
#     search_fields = ('user__username', 'release__name', 'hardwareModel__hardwareType__name',
#                      'hardwareModel__cpu__name', 'customer', 'vmType__type', 'database_type__name')



class ProjectAdmin(admin.ModelAdmin):
    # actions = [SetWorkingProjectAction, ]

    # form = HardwareModelForm


    list_display = ('name', 'release', 'customer', 'hardwareModel', 'database_type', 'version',
                  'comment', 'createTime',)
    #
    # # wizard_form_list = [
    # #     ('General', ('release', 'customer', 'version',)),
    # #     ('Hardware Information', ('hardwareType', 'database_type', )),
    # # ]
    # exclude = ('user',)
    # form = ProjectForm
    # form_layout = (
    #     Main(
    #         TabHolder(
    #             Tab(
    #                 "Project",
    #                 Fieldset(
    #                     'General Information',
    #                     'name',
    #                     Row('release', 'customer',),
    #                     Row('hardwareType', 'cpu',),
    #                     Row('database_type','version',),
    #                     'comment',
    #
    #                     description="General information for project",
    #                 ),
    #             ),
    #         ),
    #     ),
        # Side(
        #     Fieldset("Status data", 'amaRecordPerBillingBlock', 'averageAMARecordPerCall', 'amaStoreDay'),
        # )
    # )
    fieldsets = [
        # (None, {
        #     'fields': ('name',)}),
        ('Project', {

            'fields': [
                       ('name','release', 'customer',),
                       ('hardwareType', 'hardwareModel',),
                       ('database_type','version',),
                       'comment',
                       ]}),


    ]

    #inlines = [TrafficInline]
    #inlines = (TrafficInline, DiameterTrafficInline)

    list_filter = ('release', 'hardwareModel', 'customer', 'database_type')

    search_fields = ('name', 'release__name', 'hardwareModel__name',
                     'customer__name', 'database_type__name')

    # form = ProjectForm
    form = ProjectForm1

    actions =['set_working_project']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(ProjectAdmin, self).save_model(request, obj, form, change)

    def set_working_project(self, request, queryset):
        n = queryset.count()

        if n == 1:
            set_working_project_message = "Project %s has been set as working project!" % queryset[0].name
            set_working_project_success = True
            message_level = messages.SUCCESS

        else:
            set_working_project_message = "Please select only one project!"
            set_working_project_success = False
            message_level = messages.ERROR

        if set_working_project_success:
            if WorkingProject.objects.count() > 0:
                WorkingProject.objects.all().delete()

            working_project = WorkingProject.objects.create(project=queryset[0])
            working_project.save()

        self.message_user(request, set_working_project_message, level=message_level, extra_tags='safe')

    set_working_project.short_description = "Set selected project to working project"

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              )


class ProjectInformationAdmin(admin.ModelAdmin):
    # list_display = ('name', 'vmType', 'cpuNumber', 'memory', 'clientNumber', )

    form = ProjectInformationForm

    def has_add_permission(self, request):
        if ProjectInformation.current_objects.all().count() > 0:
            return False
        else:
            return True

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['vmType', 'deploy_option', 'cpuNumber', 'memory', 'clientNumber',
                               'sigtranLinkSpeed','sigtranLinkNumber', 'sigtranPortUtil',
                               'numberReleaseToEstimate','cpuImpactPerRelease',
                               'memoryImpactPerRelease', 'dbImpactPerRelease',
                               'amaRecordPerBillingBlock','averageAMARecordPerCall', 'amaStoreDay',
                               'activeSubscriber','inactiveSubscriber','groupAccountNumber',
                               'cpuUsageTuning','memoryUsageTuning',
                               ]
        return self.readonly_fields

    def get_list_display(self, request):
        list_display = ('name',)
        if WorkingProject.objects.count() > 0:
            if WorkingProject.objects.all()[0].project.hardwareModel.hardwareType.isVM:
                list_display += ('vmType',)
            if WorkingProject.objects.all()[0].project.database_type.name == 'NDB':
                list_display += ('deploy_option',)

        list_display += ('cpuNumber', 'memory', 'clientNumber', 'numberReleaseToEstimate',
                         'activeSubscriber','inactiveSubscriber', 'groupAccountNumber', )

        return list_display
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() > 0:
            if WorkingProject.objects.all()[0].project.hardwareModel.hardwareType.isVM:
                fields_row1 += ('vmType',)
            if WorkingProject.objects.all()[0].project.database_type.name == 'NDB':
                fields_row1 += ('deploy_option',)
        else:
            fields_row1 = ('vmType', 'deploy_option',)
            addition_message = ' -- Please set working project first!'

        return [
            # (None, {
            #     'fields': ('name',)}),
            ('Hardware Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('cpuNumber', 'memory',),
                    ('clientNumber',),
                ]}),
            ('Network Information', {
                'fields': [
                    ('sigtranLinkSpeed','sigtranLinkNumber',),
                    ('sigtranPortUtil', ),
                ]}),
            ('Release Impact Information', {
                'fields': [
                    ('numberReleaseToEstimate','cpuImpactPerRelease',),
                    ('memoryImpactPerRelease', 'dbImpactPerRelease',),
                ]}),
            ('AMA Information', {
                'fields': [
                    ('amaRecordPerBillingBlock','averageAMARecordPerCall',),
                    ('amaStoreDay', ),
                ]}),
            ('Account Information', {
                'fields': [
                    ('activeSubscriber','inactiveSubscriber',),
                    ('groupAccountNumber', ),
                ]}),
            ('Usage Tuning', {
                'fields': [
                    ('cpuUsageTuning','memoryUsageTuning',),
                ]}),
        ]

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/set_client_number.js',
              )

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ProjectInformation.objects.none()
        return super(ProjectInformationAdmin,self).get_queryset(request).\
            filter(project=WorkingProject.objects.all()[0].project)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if WorkingProject.objects.count() == 0:
    #         self.message_user(request, 'Please set working project first!', level=messages.ERROR)
    #         return ProjectInformation.objects.none()
    #
    #     return super(ProjectInformationAdmin,self).changeform_view(request,object_id,form_url,extra_context)

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ProjectInformation.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(ProjectInformationAdmin, self).save_model(request, obj, form, change)


class TrafficInformationAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['callType', 'activeSubscriber', 'inactiveSubscriber', 'trafficBHTA', 'trafficTPS',
                     'callHoldingTime', 'averageActiveSessionPerSubscriber', 'averageCategoryPerCCR',
                     'averageCategoryPerSession', 'volumeCCRiBHTA', 'volumeCCRuBHTA', 'volumeCCRtBHTA',
                     'timeCCRiBHTA', 'timeCCRuBHTA', 'timeCCRtBHTA'
                    ]
        return self.readonly_fields

    def get_total_bhta_tps(self):
        traffic_information_list = TrafficInformation.current_objects.all()

        total_bhta = 0
        total_tps = 0
        if traffic_information_list.count() > 0:
            for trafficInformation in traffic_information_list:
                total_bhta += trafficInformation.trafficBHTA
                total_tps += trafficInformation.trafficTPS

        return total_bhta, total_tps

    # totalBHTA, totalTPS = get_total_bhta_tps()

    list_display = ('callType', 'activeSubscriber', 'inactiveSubscriber', 'trafficBHTA', 'trafficTPS',
                    'callHoldingTime')

    list_filter = ('callType',)

    search_fields = ('callType__name', 'project__user__username', 'project__release__name',
                     'project__hardwareModel__hardwareType__name',
                     'project__hardwareModel__cpu__name', 'project__customer',
                     'project__vmType__type', 'project__database_type__name')

    form = TrafficInformationForm

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        return [
            # (None, {
            #     'fields': ('name',)}),
            ('Subscriber Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('activeSubscriber', 'inactiveSubscriber',),
                ]}),
            ('Traffic Information', {
                'fields': [
                    ('callType', 'callHoldingTime',),
                    ('trafficBHTA', 'trafficTPS',),
                ]}),
            ('Diameter Session Information', {
                'fields': [
                    ('averageActiveSessionPerSubscriber', 'averageCategoryPerCCR', 'averageCategoryPerSession',),
                    ('volumeCCRiBHTA', 'volumeCCRuBHTA', 'volumeCCRtBHTA',),
                    ('timeCCRiBHTA', 'timeCCRuBHTA', 'timeCCRtBHTA'),
                ]}),
        ]

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/traffic_information.js',
              )

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return TrafficInformation.objects.none()
        return super(TrafficInformationAdmin,self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

        # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        #     if WorkingProject.objects.count() == 0:
        #         self.message_user(request, 'Please set working project first!', level=messages.ERROR)
        #         return ProjectInformation.objects.none()
        #
        #     return super(ProjectInformationAdmin,self).changeform_view(request,object_id,form_url,extra_context)

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return TrafficInformation.objects.none()
        obj.project=WorkingProject.objects.all()[0].project
        super(TrafficInformationAdmin, self).save_model(request, obj, form, change)


class FeatureConfigurationAdmin(admin.ModelAdmin):
    list_display = ('feature', 'featurePenetration', )

    list_filter = ('feature',)

    search_fields = ('feature__name',)

    form = FeatureConfigurationForm

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['feature', 'featurePenetration', 'colocateMemberGroup', 'rtdbSolution',
                    'groupNumber', 'ratioOfLevel1'
                    ]
        return self.readonly_fields

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/feature_configuration.js',
              )

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return FeatureConfiguration.objects.none()
        return super(FeatureConfigurationAdmin,self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        return [
            ('Feature Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('feature', 'featurePenetration',),
                ]}),
            ('Online Hierarchy Feature Information', {
                'fields': [
                    ('colocateMemberGroup',),
                    ('rtdbSolution',),
                    ('groupNumber', 'ratioOfLevel1'),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return FeatureConfiguration.objects.none()
        obj.project=WorkingProject.objects.all()[0].project
        super(FeatureConfigurationAdmin, self).save_model(request, obj, form, change)

# class DBConfigurationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'dbFactor', 'placeholderRatio', 'memberGroupOption')
#
#     list_filter = ('project', 'dbInfo__db', 'dbInfo__mode', 'dbInfo__release', 'memberGroupOption')
#
#     search_fields = ('dbInfo__db__name', 'dbInfo__mode__name', 'project__user__username', 'project__release__name',
#                      'project__hardwareModel__hardwareType__name',
#                      'project__hardwareModel__cpu__name', 'project__customer',
#                      'project__vmType__type', 'project__database_type__name')


class CallTypeCounterConfigurationAdmin(admin.ModelAdmin):
    model = CallTypeCounterConfiguration
    form = CallTypeCounterConfigurationForm
    list_display = ('callType', 'averageBundleNumberPerSubscriber','average24hBundleNumberPerSubscriber',
              'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
              'appliedUBDNumber',)
    list_filter = ('project', 'callType',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',
                    'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
                    'appliedUBDNumber','callType', 'totalCounterNumber',
                    ]
        # else:
        #     return ['callType', 'totalCounterNumber']
        return self.readonly_fields

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CallTypeCounterConfiguration.objects.none()

        traffic_information_list = TrafficInformation.current_objects.all()

        if traffic_information_list.count() == 0:
            self.message_user(request, 'Please configure traffic first!', level=messages.ERROR)
            return CallTypeCounterConfiguration.objects.none()

        counter_configuration_list = CounterConfiguration.current_objects.all()

        if counter_configuration_list.count() == 0:
            self.message_user(request, 'Please configure counter first!', level=messages.ERROR)
            return CallTypeCounterConfiguration.objects.none()

        counter_configuration = counter_configuration_list[0]

        if not counter_configuration.configureForCallType:
            self.message_user(request, 'Please check "Configure Counter For Call Types" first!', level=messages.ERROR)
            return CallTypeCounterConfiguration.objects.none()

        for trafficInformation in traffic_information_list:
            call_type_counter_configuration_list = CallTypeCounterConfiguration.current_objects.all().filter(
                callType=trafficInformation.callType,
            )
            if call_type_counter_configuration_list.count() == 0:
                call_type_counter_configuration = CallTypeCounterConfiguration.current_objects.create_call_type_counter_configuration(
                    project=WorkingProject.objects.all()[0].project,
                    callType=trafficInformation.callType,
                    average24hBundleNumberPerSubscriber=counter_configuration.average24hBundleNumberPerSubscriber,
                    averageBundleNumberPerSubscriber=counter_configuration.averageBundleNumberPerSubscriber,
                    nonAppliedUBDNumber=counter_configuration.nonAppliedUBDNumber,
                    nonAppliedBucketNumber=counter_configuration.nonAppliedBucketNumber,
                    appliedUBDNumber=counter_configuration.appliedUBDNumber,
                    appliedBucketNumber=counter_configuration.appliedBucketNumber,
                )

        return super(CallTypeCounterConfigurationAdmin,self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        return [
            (None, {
                'fields': [
                    ('callType',),
                ]}),
            ('Bundle Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',),
                ]}),
            ('Bucket/UBD Information', {
                'fields': [
                    ('totalCounterNumber',),
                    ('nonAppliedBucketNumber', 'nonAppliedUBDNumber',),
                    ('appliedBucketNumber', 'appliedUBDNumber',),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CounterConfiguration.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(CallTypeCounterConfigurationAdmin, self).save_model(request, obj, form, change)

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/calltype_counter_configuration.js',
              )


class CounterConfigurationAdmin(admin.ModelAdmin):
    list_display = ('averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',
                    'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
                    'appliedUBDNumber','groupBundleNumber', 'groupBucketNumber',
                    )

    list_filter = ('project',)
    # extra_buttons = [{'href':'cin','title':'Action Stock In'}]

    # search_fields = ('project__user__username', 'project__release__name',
    #                  'project__hardwareModel__hardwareType__name',
    #                  'project__hardwareModel__cpu__name', 'project__customer',
    #                  'project__vmType__type', 'project__database_type__name')

    form = CounterConfigurationForm

    def has_add_permission(self, request):
        if CounterConfiguration.current_objects.all().count() > 0:
            return False
        else:
            return True

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',
                    'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
                    'appliedUBDNumber', 'totalCounterNumber', 'generateMultipleAMAForCounter',
                    'groupBundleNumber', 'groupBucketNumber',
                    ]
        return self.readonly_fields

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/counter_configuration.js',
              )

    def  get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CounterConfiguration.objects.none()
        return super(CounterConfigurationAdmin,self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        return [
            ('Bundle Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',),
                ]}),
            ('Bucket/UBD Information', {
                'fields': [
                    ('totalCounterNumber',),
                    ('nonAppliedBucketNumber', 'nonAppliedUBDNumber',),
                    ('appliedBucketNumber', 'appliedUBDNumber',),
                    ('turnOnBasicCriteriaCheck',),
                    ('generateMultipleAMAForCounter',),
                    # ('turnOnBasicCriteriaCheck', 'generateMultipleAMAForCounter',),
                    ('configureForCallType',)
                ]}),
            ('Group Counter Information', {
                'fields': [
                    ('groupBundleNumber', 'groupBucketNumber',),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CounterConfiguration.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(CounterConfigurationAdmin, self).save_model(request, obj, form, change)

# class CallTypeCounterConfigurationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',
#                     'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
#                     'appliedUBDNumber', 'generateMultipleAMAForCounter' )
#
#     list_filter = ('project', 'callType')
#
#     search_fields = ('callType__name', 'project__user__username', 'project__release__name',
#                      'project__hardwareModel__hardwareType__name',
#                      'project__hardwareModel__cpu__name', 'project__customer',
#                      'project__vmType__type', 'project__database_type__name')


class DBConfigurationAdmin(admin.ModelAdmin):
    list_display = ('dbInfo', 'recordSize', 'subscriberNumber', 'dbFactor', 'recordNumber',
                    'placeholderRatio', 'cacheSize', 'todoLogSize', 'mateLogSize',)
    list_filter = ('dbInfo__db', 'memberGroupOption')
    search_fields = ('dbInfo__db__name',)
    form = DBConfigurationForm

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['dbInfo', 'recordSize', 'subscriberNumber', 'dbFactor', 'recordNumber',
                    'placeholderRatio', 'cacheSize', 'todoLogSize', 'mateLogSize',
                    ]
        return self.readonly_fields

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/db_configuration.js',
              )
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return DBConfiguration.objects.none()
        return super(DBConfigurationAdmin,self).get_queryset(request). \
            filter(
                project=WorkingProject.objects.all()[0].project,
        )

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('DB Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('dbInfo','recordSize',),
                    ('memberGroupOption','subscriberNumber',),
                    ('dbFactor','referencePlaceholderRatio',),
                    ('placeholderRatio',),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return DBConfiguration.objects.none()
        obj.project=WorkingProject.objects.all()[0].project
        super(DBConfigurationAdmin, self).save_model(request, obj, form, change)


class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ('applicationName', 'backupAppNodeNumberPerSystem', 'spareAppNodeNumberPerSystem',
                    'backupDBNodeNumberPerSystem', 'spareDBNodePairNumberPerSystem')

    form = SystemConfigurationForm

    # def has_add_permission(self, request):
    #     if SystemConfiguration.current_objects.all().count() > 0:
    #         return False
    #     else:
    #         return True
        
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return [#'cabinetNumberPerSystem',
                    'applicationName',
                    'backupAppNodeNumberPerSystem', 'spareAppNodeNumberPerSystem',
                    'backupDBNodeNumberPerSystem', 'spareDBNodePairNumberPerSystem'
                    ]
        return self.readonly_fields

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              # '/static/js/db_configuration.js',
              )

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return SystemConfiguration.objects.none()

        application_epay_list = ApplicationName.objects.all().filter(
            name='EPAY',
        )
        if application_epay_list.count() > 0:
            app_conf_list = SystemConfiguration.current_objects.all().filter(
                applicationName=application_epay_list[0],
            )

            if app_conf_list.count() == 0:
                SystemConfiguration.current_objects.create_system_configuration(
                    project=WorkingProject.objects.all()[0].project,
                    applicationName=application_epay_list[0],
                    backupAppNodeNumberPerSystem=0,
                    spareAppNodeNumberPerSystem=0,
                    backupDBNodeNumberPerSystem=0,
                    spareDBNodePairNumberPerSystem=0,
                )

        return super(SystemConfigurationAdmin,self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('System Configuration' + addition_message, {
                'fields': [
                    fields_row1,
                    ('applicationName',),
                    ('backupAppNodeNumberPerSystem', 'spareAppNodeNumberPerSystem',),
                    ('backupDBNodeNumberPerSystem', 'spareDBNodePairNumberPerSystem',),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return SystemConfiguration.objects.none()

        obj.project=WorkingProject.objects.all()[0].project

        super(SystemConfigurationAdmin, self).save_model(request, obj, form, change)


class ApplicationConfigurationAdmin(admin.ModelAdmin):
    list_display = ('applicationName', 'activeSubscriber', 'inactiveSubscriber',
                    'trafficTPS', 'deployOption')

    form = ApplicationConfigurationForm

    list_filter = ('applicationName',)

    search_fields = ('applicationName__name',)
    # def has_add_permission(self, request):
    #     if CounterConfiguration.objects.all().filter(project=WorkingProject.objects.all()[0].project).count() > 0:
    #         return False
    #     else:
    #         return True

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['applicationName', 'activeSubscriber', 'inactiveSubscriber',
                    'trafficTPS', 'deployOption'
                    ]
        return self.readonly_fields

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ApplicationConfiguration.objects.none()
        return super(ApplicationConfigurationAdmin, self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('Application Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('applicationName', 'deployOption',),
                ]}),
            ('Subscriber Information', {
                'fields': [
                    ('activeSubscriber', 'inactiveSubscriber',),
                ]}),
            ('Traffic Information', {
                'fields': [
                    ('trafficTPS', ),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ApplicationConfiguration.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(ApplicationConfigurationAdmin, self).save_model(request, obj, form, change)

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/other_application_information.js',
              )


# class SelectPAdmin(admin.ModelAdmin):
#     class Media:
#         js = ('/static/js/jquery-2.1.1.js',
#               '/static/js/selectp.js',
#               )
# class AddressAdmin(AjaxSelectAdmin):
#
#      form = AddressForm
#
#      class Media:
#         js = ('/static/xadmin/vendor/jquery/jquery.js',
#               '/static/xadmin/vendor/jquery-ui/jquery.ui.js',
#               '/static/js/address.js',
#               )
#         css = {
#             'all':'/static/xadmin/vendor/jquery-ui/jquery-ui.theme.css'
#


class CalculatedResultAdmin(admin.ModelAdmin):
    list_display = ('applicationName', 'appNodeNumber', 'dbNodeNumber',
                    'ioNodeNumber')

    # form = ApplicationConfigurationForm

    list_filter = ('applicationName',)

    search_fields = ('applicationName__name',)

    # change_list_template = "path/to/change_list.html"

    def has_add_permission(self, request):
        return False
        # if CalculatedResult.objects.all().filter(project=WorkingProject.objects.all()[0].project).count() > 0:
        #     return False
        # else:
        #     return True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['applicationName', 'appNodeNumber', 'dbNodeNumber',
                    'ioNodeNumber'
                    ]
        return self.readonly_fields

    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CalculatedResult.objects.none()
        return super(CalculatedResultAdmin, self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('Application Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('applicationName', ),
                ]}),
            ('Calculated Nodes Information', {
                'fields': [
                    ('appNodeNumber', 'dbNodeNumber',),
                    ('ioNodeNumber', ),
                ]}),
        ]

    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CalculatedResult.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(CalculatedResultAdmin, self).save_model(request, obj, form, change)


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [url(r'^project/calculatedresult/calculate/$', self.admin_site.admin_view(self.calculate)),]

        return my_urls + urls

    def calculate(self, request):
        # print('doing evil with', CalculatedResult.objects.get(pk=int(pk)))
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)

        CalculatedResult.current_objects.all().delete()

        CalculatedResult.current_objects.create_calculated_result(
            project=WorkingProject.objects.all()[0].project,
            applicationName=ApplicationName.objects.all().filter(name='EPAY')[0],
            appNodeNumber=5,
            dbNodeNumber=2,
            ioNodeNumber=2,
        )

        return redirect('/admin/project/calculatedresult/')

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/other_application_information.js',
              )


class DimensioningResultAdmin(admin.ModelAdmin):
    pass


class DimensioningResultPerSystemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectInformation, ProjectInformationAdmin)
admin.site.register(TrafficInformation, TrafficInformationAdmin)
admin.site.register(FeatureConfiguration, FeatureConfigurationAdmin)
admin.site.register(DBConfiguration, DBConfigurationAdmin)
admin.site.register(CounterConfiguration, CounterConfigurationAdmin)
admin.site.register(CallTypeCounterConfiguration, CallTypeCounterConfigurationAdmin)
admin.site.register(SystemConfiguration, SystemConfigurationAdmin)
admin.site.register(Customer)
admin.site.register(ApplicationConfiguration, ApplicationConfigurationAdmin)
admin.site.register(CalculatedResult, CalculatedResultAdmin)

# admin.site.register(Province)
# admin.site.register(City1)
# admin.site.register(City)
# admin.site.register(Country)
# admin.site.register(State)
# admin.site.register(SelectP,SelectPAdmin)
# admin.site.register(Address, AddressAdmin)