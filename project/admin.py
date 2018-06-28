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
from hardware.models import HardwareModel, HardwareType, VMType, CPUList, MemoryList
from service.models import ApplicationName, CallType, DBName, FeatureDBImpact, DBInformation
from .forms import ProjectForm, ProjectInformationForm, \
    TrafficInformationForm, FeatureConfigurationForm, CounterConfigurationForm, \
    CallTypeCounterConfigurationForm, DBConfigurationForm, SystemConfigurationForm, ApplicationConfigurationForm
from django.contrib import messages
from django.db.models import Q

from common import logger
from common.logger import logged
import sys, math
import os.path


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

    list_display = ('name', 'release', 'customer', 'hardwareModel', 'database_type',
                    #'version',
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
                ('name', 'release',),
                ('hardwareType', 'hardwareModel',),
                ('customer',),
                ('database_type',),
                #('database_type', 'version',),
                'comment',
            ]}),

    ]

    # inlines = [TrafficInline]
    # inlines = (TrafficInline, DiameterTrafficInline)

    list_filter = ('release', 'hardwareModel', 'customer', 'database_type')

    search_fields = ('name', 'release__name', 'hardwareModel__name',
                     'customer__name', 'database_type__name')

    # form = ProjectForm
    form = ProjectForm

    actions = ['set_working_project']

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        # ProjectInformationForm.
        super(ProjectAdmin, self).save_model(request, obj, form, change)


    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_add_permission(self, request):
        if ProjectInformation.current_objects.all().count() > 0:
            return False
        else:
            return True

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['vmType', 'deploy_option', 'cpuNumber', 'memory', 'clientNumber',
                    'sigtranLinkSpeed', 'sigtranLinkNumber', 'sigtranPortUtil',
                    'numberReleaseToEstimate', 'cpuImpactPerRelease',
                    'memoryImpactPerRelease', 'dbImpactPerRelease',
                    'amaRecordPerBillingBlock', 'averageAMARecordPerCall', 'amaStoreDay',
                    'activeSubscriber', 'inactiveSubscriber', 'groupAccountNumber',
                    'cpuUsageTuning', 'memoryUsageTuning',
                    ]
        return self.readonly_fields

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_list_display(self, request):
        list_display = ('name',)
        if WorkingProject.objects.count() > 0:
            if WorkingProject.objects.all()[0].project.hardwareType.isVM:
                list_display += ('vmType',)
            if WorkingProject.objects.all()[0].project.database_type.name == 'NDB':
                list_display += ('deploy_option',)

            if WorkingProject.objects.all()[0].project.hardwareType.isVM:
                list_display += ('cpuNumber', )

        list_display += ('clientNumber', 'memory', )
        if WorkingProject.objects.all()[0].project.hardwareType.isVM and \
            not WorkingProject.objects.all()[0].project.hardwareType.isSingleServer:
            list_display += ('dbCPUNumber', 'dbMemory', )
        list_display += ('numberReleaseToEstimate', 'activeSubscriber', 'inactiveSubscriber', 'groupAccountNumber',)

        return list_display

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        fields_row2 = ()
        fields_row2_2 = ()
        fields_row3 = ()
        fields_row4 = ()
        fields_row5 = ()
        if WorkingProject.objects.count() > 0:
            if WorkingProject.objects.all()[0].project.hardwareModel.hardwareType.isVM:
                fields_row1 += ('vmType',)
                fields_row2 = ('cpuNumber', 'clientNumber',)
                fields_row2_2 = ('memory',)
                if WorkingProject.objects.all()[0].project.hardwareModel.hardwareType.isSingleServer:
                    fields_row3 = ()
                else:
                    fields_row3 = ('dbCPUNumber', 'dbMemory')
                    fields_row4 = ('pilotCPUNumber', 'pilotMemory')
                    fields_row5 = ('ioCPUNumber', 'ioMemory')
                self.form.declared_fields['cpuNumber'].label = 'CPU Number'
                # if self.form.declared_fields['vmType'] is not None:
                #     self.form.declared_fields['vmType'].queryset = VMType.objects.all()
                # self.form.declared_fields['cpuNumber'].queryset = VMType.objects.all()
                # self.form.declared_fields['clientNumber'].queryset = VMType.objects.all()
                # self.form.declared_fields['memory'].queryset = VMType.objects.all()
            else:
                fields_row2 = ('cpuNumber', 'memory')
                self.form.declared_fields['cpuNumber'].label = 'Client Number'

            # self.form.declared_fields['cpuNumber'].queryset = CPUList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['memory'].queryset = MemoryList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['dbCPUNumber'].queryset = CPUList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['dbMemory'].queryset = MemoryList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['pilotCPUNumber'].queryset = CPUList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['pilotMemory'].queryset = MemoryList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['ioCPUNumber'].queryset = CPUList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)
            # self.form.declared_fields['ioMemory'].queryset = MemoryList.objects.all().filter(
            #     hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel)

            if WorkingProject.objects.all()[0].project.database_type.name == 'NDB' and \
                WorkingProject.objects.all()[0].project.hardwareModel.hardwareType.isSingleServer == False:
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
                    fields_row2,
                    fields_row2_2,
                    fields_row3,
                    fields_row4,
                    fields_row5,
                ]}),
            ('Account Information', {
                'fields': [
                    ('activeSubscriber', 'inactiveSubscriber',),
                    ('groupAccountNumber',),
                ]}),
            ('Release Impact Information', {
                'fields': [
                    ('numberReleaseToEstimate',),
                    ('cpuImpactPerRelease',),
                    ('memoryImpactPerRelease',),
                    ('dbImpactPerRelease',),
                ]}),
            ('AMA Information', {
                'fields': [
                    ('amaRecordPerBillingBlock',),
                    ('averageAMARecordPerCall',),
                    ('amaStoreDay',),
                ]}),
            ('Usage Tuning', {
                'fields': [
                    ('cpuUsageTuning',),
                    ('memoryUsageTuning',),
                ]}),
            ('Network Information', {
                'fields': [
                    ('sigtranLinkSpeed',),
                    ('sigtranLinkNumber',),
                    ('sigtranPortUtil',),
                ]}),
        ]

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/set_client_number.js',
              )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ProjectInformation.objects.none()
        return super(ProjectInformationAdmin, self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if WorkingProject.objects.count() == 0:
    #         self.message_user(request, 'Please set working project first!', level=messages.ERROR)
    #         return ProjectInformation.objects.none()
    #
    #     return super(ProjectInformationAdmin,self).changeform_view(request,object_id,form_url,extra_context)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ProjectInformation.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        obj.clientNumber = obj.cpuNumber.clientNumber
        # obj.dbMemory = obj.dbMemory
        # obj.dbCPUNumber = obj.cpuNumber

        super(ProjectInformationAdmin, self).save_model(request, obj, form, change)


class TrafficInformationAdmin(admin.ModelAdmin):
    form = TrafficInformationForm
    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['callType', 'activeSubscriber', 'inactiveSubscriber', 'trafficBHTA', 'trafficTPS',
                    'callHoldingTime', 'averageActiveSessionPerSubscriber', 'averageCategoryPerCCR',
                    'averageCategoryPerSession', 'volumeCCRiBHTA', 'volumeCCRuBHTA', 'volumeCCRtBHTA',
                    'timeCCRiBHTA', 'timeCCRuBHTA', 'timeCCRtBHTA'
                    ]
        return self.readonly_fields

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        if ProjectInformation.current_objects.count() > 0:
            self.form.declared_fields['activeSubscriber'].initial = \
                ProjectInformation.current_objects.all()[0].activeSubscriber
            self.form.declared_fields['inactiveSubscriber'].initial = \
                ProjectInformation.current_objects.all()[0].inactiveSubscriber

        return [
            # (None, {
            #     'fields': ('name',)}),
            ('Subscriber Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('activeSubscriber',),
                    ('inactiveSubscriber',),
                ]}),
            ('Traffic Information', {
                'fields': [
                    ('callType',),
                    ('callHoldingTime',),
                    ('trafficBHTA', 'trafficTPS',),
                ]}),
            ('Diameter Session Information', {
                'fields': [
                    ('averageActiveSessionPerSubscriber',),
                    ('averageCategoryPerCCR',),
                    ('averageCategoryPerSession',),
                    ('volumeCCRiBHTA', 'volumeCCRuBHTA', 'volumeCCRtBHTA',),
                    ('timeCCRiBHTA', 'timeCCRuBHTA', 'timeCCRtBHTA'),
                ]}),
        ]

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/traffic_information.js',
              )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return TrafficInformation.objects.none()
        return super(TrafficInformationAdmin, self).get_queryset(request).filter(
            project=WorkingProject.objects.all()[0].project,
            callType__isShow=True,
        )

        # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        #     if WorkingProject.objects.count() == 0:
        #         self.message_user(request, 'Please set working project first!', level=messages.ERROR)
        #         return ProjectInformation.objects.none()
        #
        #     return super(ProjectInformationAdmin,self).changeform_view(request,object_id,form_url,extra_context)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return TrafficInformation.objects.none()

        obj.project = WorkingProject.objects.all()[0].project
        super(TrafficInformationAdmin, self).save_model(request, obj, form, change)


class FeatureConfigurationAdmin(admin.ModelAdmin):
    list_display = ('feature', 'featurePenetration',)

    list_filter = ('feature',)

    search_fields = ('feature__name',)

    form = FeatureConfigurationForm

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return FeatureConfiguration.objects.none()
        return super(FeatureConfigurationAdmin, self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        return [
            ('Feature Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('feature',),
                    ('featurePenetration',),
                ]}),
            ('Online Hierarchy Feature Information', {
                'fields': [
                    ('colocateMemberGroup',),
                    ('rtdbSolution',),
                    ('groupNumber',),
                    ('ratioOfLevel1',),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return FeatureConfiguration.objects.none()

        if obj.feature.name == 'Online Hierarchy' and obj.featurePenetration >0:
            app_group_list = ApplicationName.objects.all().filter(
                name='Group',
            )
            # Insert one record for EPAY to ApplicationConfiguration if no EPAY record existed.
            if app_group_list.count() > 0:
                app_config_group_list = ApplicationConfiguration.current_objects.all().filter(
                    applicationName=app_group_list[0],
                )
                if app_config_group_list.count() == 0:
                    if obj.colocateMemberGroup:
                        ApplicationConfiguration.current_objects.create_application_config(
                            project=WorkingProject.objects.all()[0].project,
                            application_name=app_group_list[0],
                            deployOption='EPAY Node',
                            olh_penetration=obj.featurePenetration / 100,
                        )
                    else:
                        ApplicationConfiguration.current_objects.create_application_config(
                            project=WorkingProject.objects.all()[0].project,
                            application_name=app_group_list[0],
                            deployOption='Group Node',
                            olh_penetration=obj.featurePenetration / 100,
                        )
                else:
                    if obj.colocateMemberGroup:
                        app_config_group_list.update(deployOption='EPAY Node',)
                    else:
                        app_config_group_list.update(deployOption='Group Node',)

            app_group_list = ApplicationName.objects.all().filter(
                name='EPPSM',
            )
            # Insert one record for EPPSM to ApplicationConfiguration if no EPPSM record existed.
            if app_group_list.count() > 0:
                app_config_group_list = ApplicationConfiguration.current_objects.all().filter(
                    applicationName=app_group_list[0],
                )
                if app_config_group_list.count() == 0:
                    if obj.colocateMemberGroup:
                        ApplicationConfiguration.current_objects.create_application_config(
                            project=WorkingProject.objects.all()[0].project,
                            application_name=app_group_list[0],
                            deployOption='EPPSM Node',
                        )

        obj.project = WorkingProject.objects.all()[0].project
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
    list_display = ('callType', 'averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',
                    'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
                    'appliedUBDNumber',)
    list_filter = ('project', 'callType',)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_delete_permission(self, request, obj=None):
        return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_add_permission(self, request, obj=None):
        return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['averageBundleNumberPerSubscriber', 'average24hBundleNumberPerSubscriber',
                    'nonAppliedBucketNumber', 'nonAppliedUBDNumber', 'appliedBucketNumber',
                    'appliedUBDNumber', 'callType', 'totalCounterNumber',
                    ]
        # else:
        #     return ['callType', 'totalCounterNumber']
        return self.readonly_fields

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                    call_type=trafficInformation.callType,
                    average_24h_bundle_number_per_subscriber=counter_configuration.average24hBundleNumberPerSubscriber,
                    average_bundle_number_per_subscriber=counter_configuration.averageBundleNumberPerSubscriber,
                    non_applied_ubd_number=counter_configuration.nonAppliedUBDNumber,
                    non_applied_bucket_number=counter_configuration.nonAppliedBucketNumber,
                    applied_ubd_number=counter_configuration.appliedUBDNumber,
                    applied_bucket_number=counter_configuration.appliedBucketNumber,
                )

        return super(CallTypeCounterConfigurationAdmin, self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                    'appliedUBDNumber', 'groupBundleNumber', 'groupBucketNumber',
                    )

    list_filter = ('project',)
    # extra_buttons = [{'href':'cin','title':'Action Stock In'}]

    # search_fields = ('project__user__username', 'project__release__name',
    #                  'project__hardwareModel__hardwareType__name',
    #                  'project__hardwareModel__cpu__name', 'project__customer',
    #                  'project__vmType__type', 'project__database_type__name')

    form = CounterConfigurationForm

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_add_permission(self, request):
        if CounterConfiguration.current_objects.all().count() > 0:
            return False
        else:
            return True

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CounterConfiguration.objects.none()
        return super(CounterConfigurationAdmin, self).get_queryset(request). \
            filter(project=WorkingProject.objects.all()[0].project)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'

        return [
            ('Bundle Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('averageBundleNumberPerSubscriber',),
                    ('average24hBundleNumberPerSubscriber',),
                ]}),
            ('Bucket/UBD Information', {
                'fields': [
                    ('totalCounterNumber',),
                    ('nonAppliedBucketNumber',),
                    ('nonAppliedUBDNumber',),
                    ('appliedBucketNumber',),
                    ('appliedUBDNumber',),
                    ('turnOnBasicCriteriaCheck',),
                    ('generateMultipleAMAForCounter',),
                    # ('turnOnBasicCriteriaCheck', 'generateMultipleAMAForCounter',),
                    ('configureForCallType',)
                ]}),
            ('Group Counter Information', {
                'fields': [
                    ('groupBundleNumber',),
                    ('groupBucketNumber',),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    list_display = ('application', 'dbInfo', 'memberGroupOption', 'recordSize', 'subscriberNumber',
                    'dbFactor', 'recordNumber', 'placeholderRatio', 'cacheSize', )
    #('todoLogSize', 'mateLogSize',)
    list_filter = ('application', 'dbInfo__db', 'memberGroupOption')
    search_fields = ('application', 'dbInfo__db__name',)
    form = DBConfigurationForm

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return self.list_display
        return self.readonly_fields

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/db_configuration.js',
              )

    def init_db(self):
        db_list = DBName.objects.all()

        for db in db_list:
            db.defaultGroupCounterFactor = 0
            db.defaultMemberCounterFactor = 0
            db.featureMemberImpactFactor = 0
            db.featureMemberImpactFactor = 0
            db.save()

    def calculate_feature_db_factor(self):
        feature_config_list = FeatureConfiguration.current_objects.all()
        for feature_config in feature_config_list:
            feature_db_impact_list = FeatureDBImpact.objects.all().filter(
                featureName=feature_config.feature,
            )

            for feature_db_impact in feature_db_impact_list:
                db = feature_db_impact.dbName

                db.featureMemberImpactFactor = \
                    feature_db_impact.memberImpactFactor * feature_config.featurePenetration / 100
                db.featureGroupImpactFactor = \
                    feature_db_impact.groupImpactFactor * feature_config.featurePenetration / 100

                db.save()

    def calculate_counter_db_factor(self):
        if CounterConfiguration.current_objects.count() > 0:
            counter_config = CounterConfiguration.current_objects.all()[0]

            db_list = DBName.objects.all().filter(
                name='CTRTDB',
            )
            if db_list.count() > 0:
                db = db_list[0]
                counter_num_per_record = WorkingProject.objects.all()[0].project.release.counterNumberPerRecord
                if counter_num_per_record <= 0:
                    counter_num_per_record = 6
                db.defaultMemberCounterFactor = \
                    math.ceil(counter_config.total_counter_number / counter_num_per_record) + \
                    math.ceil(counter_config.total_bundle_number / counter_num_per_record)
                db.defaultGroupCounterFactor = \
                    math.ceil(counter_config.groupBucketNumber / counter_num_per_record) + \
                    math.ceil(counter_config.groupBundleNumber / counter_num_per_record)
                db.save()
        else:
            return

    def get_ctrtdb_placeholder_ratio(self, original_placeholder_ratio, db_factor,
                                     bundle_num, counter_num, counter_num_per_record):
        if db_factor > 0 and counter_num_per_record > 0:
            placeholder_ratio = original_placeholder_ratio - \
                                (bundle_num + counter_num) / counter_num_per_record / db_factor * 0.12
            return float('%.02f'%placeholder_ratio)
        else:
            return 0

    def update_application_db_configuration(self, application_config):
        project = WorkingProject.objects.all()[0].project
        project_information = ProjectInformation.current_objects.all()[0]

        if application_config.applicationName.name == 'EPAY':
            db_list = DBName.objects.all().filter(
               ~Q(defaultMemberFactor=0)|~Q(defaultGroupFactor=0)|~Q(defaultMemberCounterFactor=0)|
               ~Q(defaultGroupCounterFactor=0)|~Q(featureMemberImpactFactor=0)|~Q(featureGroupImpactFactor=0),
            )
        elif application_config.applicationName.name == 'DRouter':
            db_list = DBName.objects.all().filter(
                ~Q(defaultDRouterFactor=0),
            )
        elif application_config.applicationName.name == 'EPPSM':
            db_list = DBName.objects.all().filter(
                ~Q(defaultEppsmFactor=0),
            )
        elif application_config.applicationName.name == 'eCTRL':
            db_list = DBName.objects.all().filter(
                ~Q(defaultEctrlFactor=0),
            )
        else:
            db_list = DBName.objects.none()

        for db in db_list:
            if project.database_type.name == 'NDB':
                placeholder_ratio = db.ndbRefPlaceholderRatio
            else:
                placeholder_ratio = 0

            db_info_list = DBInformation.objects.all().filter(
                db=db,
                mode=project.database_type,
                release=project.release,
            )

            if db_info_list.count() > 0:
                db_info = db_info_list[0]

                group_factor = 0
                if application_config.applicationName.name == 'EPAY':
                    member_factor = db.member_factor
                    group_factor = db.group_factor
                elif application_config.applicationName.name == 'DRouter':
                    member_factor = db.defaultDRouterFactor
                elif application_config.applicationName.name == 'EPPSM':
                    member_factor = db.defaultEppsmFactor
                elif application_config.applicationName.name == 'eCTRL':
                    member_factor = db.defaultEctrlFactor
                else:
                    member_factor = 0

                if member_factor > 0:
                    member_group_option = 'Member'

                    if application_config.applicationName.name == 'EPAY':
                        if db_info.db.isIncludeInactiveSubscriber:
                            subscriber_number = project_information.activeSubscriber + project_information.inactiveSubscriber
                        else:
                            subscriber_number = project_information.activeSubscriber

                        if project.database_type.name == 'NDB' and db.name == 'CTRTDB':
                            if CounterConfiguration.current_objects.count() > 0:
                                counter_config = CounterConfiguration.current_objects.all()[0]
                                placeholder_ratio = self.get_ctrtdb_placeholder_ratio(
                                    placeholder_ratio,
                                    member_factor,
                                    counter_config.total_bundle_number,
                                    counter_config.total_counter_number,
                                    project.release.counterNumberPerRecord)
                            else:
                                placeholder_ratio = self.get_ctrtdb_placeholder_ratio(
                                    placeholder_ratio,
                                    0,
                                    0,
                                    0,
                                    project.release.counterNumberPerRecord)
                    else:
                        subscriber_number = application_config.activeSubscriber + application_config.inactiveSubscriber
                        if db.name == 'CDBRTDB':
                            subscriber_number = project_information.groupAccountNumber

                    db_config_list = DBConfiguration.current_objects.all().filter(
                        project=project,
                        application=application_config.applicationName,
                        dbInfo=db_info,
                        memberGroupOption=member_group_option,
                    )

                    if db_config_list.count() <= 0 and member_factor > 0:
                        db_config = DBConfiguration.current_objects.create_db_configuration(
                            project=project,
                            application=application_config.applicationName,
                            db_info=db_info,
                            db_factor=member_factor,
                            placeholder_ratio=placeholder_ratio,
                            member_group_option=member_group_option,
                            record_size=db_info.recordSize,
                            subscriber_number=subscriber_number,
                            reference_placeholder_ratio=placeholder_ratio,
                            reference_db_factor=db.member_factor,
                        )
                        db_config.save()

                if group_factor > 0:
                    member_group_option = 'Group'

                    if project_information.groupAccountNumber > 0:
                        subscriber_number = project_information.groupAccountNumber
                    else:
                        feature_config_list = FeatureConfiguration.current_objects.all().filter(
                            feature__name='Online Hierarchy',
                        )
                        if feature_config_list.count() > 0:
                            feature_penetration = feature_config_list[0].featurePenetration
                        else:
                            feature_penetration = 0

                        project_information.groupAccountNumber = math.ceil(
                            project_information.activeSubscriber * feature_penetration / 100)

                        project_information.save()
                        subscriber_number = project_information.groupAccountNumber

                        if project.database_type.name == 'NDB' and db.name == 'CTRTDB':
                            if CounterConfiguration.current_objects.count() > 0:
                                counter_config = CounterConfiguration.current_objects.all()[0]
                                placeholder_ratio = self.get_ctrtdb_placeholder_ratio(
                                    placeholder_ratio,
                                    group_factor,
                                    counter_config.groupBundleNumber,
                                    counter_config.groupBucketNumber,
                                    project.release.counterNumberPerRecord)
                            else:
                                placeholder_ratio = self.get_ctrtdb_placeholder_ratio(
                                    placeholder_ratio,
                                    0,
                                    0,
                                    0,
                                    project.release.counterNumberPerRecord)

                    db_config_list = DBConfiguration.current_objects.all().filter(
                        project=project,
                        application=application_config.applicationName,
                        dbInfo=db_info,
                        memberGroupOption=member_group_option,
                    )

                    if db_config_list.count() <= 0 and db.group_factor > 0:
                        db_config = DBConfiguration.current_objects.create_db_configuration(
                            project=project,
                            application=application_config.applicationName,
                            db_info=db_info,
                            db_factor=group_factor,
                            placeholder_ratio=placeholder_ratio,
                            member_group_option=member_group_option,
                            record_size=db_info.recordSize,
                            subscriber_number=subscriber_number,
                            reference_placeholder_ratio=placeholder_ratio,
                            reference_db_factor=db.member_factor,
                        )
                        db_config.save()

    def update_db_configuration(self):
        application_config_list = ApplicationConfiguration.current_objects.all().filter(
            applicationName__needConfigDB=True,
        )

        for application_config in application_config_list:
            if application_config.trafficTPS > 0:
                self.update_application_db_configuration(application_config)


    def data_pre_process(self):
        if WorkingProject.objects.count() == 0:
            return

        if ProjectInformation.current_objects.all().count() == 0:
            return

        self.init_db()
        self.calculate_feature_db_factor()
        self.calculate_counter_db_factor()
        self.update_db_configuration()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return DBConfiguration.objects.none()
        self.data_pre_process()
        return super(DBConfigurationAdmin, self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('DB Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('application',),
                    ('memberGroupOption', 'dbInfo', ),
                    ('recordSize', 'subscriberNumber',),
                    ('dbFactor', 'referenceDBFactor',),

                    ('placeholderRatio', 'referencePlaceholderRatio'),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return DBConfiguration.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        # obj.recordSize = form.fields.recordSize

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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return [  # 'cabinetNumberPerSystem',
                'applicationName',
                'backupAppNodeNumberPerSystem', 'spareAppNodeNumberPerSystem',
                'backupDBNodeNumberPerSystem', 'spareDBNodePairNumberPerSystem'
            ]
        return self.readonly_fields

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
            # '/static/js/db_configuration.js',
              )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return SystemConfiguration.objects.none()

        application_epay_list = ApplicationName.objects.all().filter(
            name='EPAY',
        )
        if application_epay_list.count() > 0:
            app_conf_list = SystemConfiguration.current_objects.all().filter(
                applicationName__name='EPAY',
            )

            if app_conf_list.count() == 0:
                SystemConfiguration.current_objects.create_system_configuration(
                    project=WorkingProject.objects.all()[0].project,
                    application_name=application_epay_list[0],
                    backup_app_node_number_per_system=0,
                    spare_app_node_number_per_system=0,
                    backup_db_node_number_per_system=0,
                    spare_db_node_pair_number_per_system=0,
                )

        return super(SystemConfigurationAdmin, self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                    ('backupAppNodeNumberPerSystem',),
                    ('spareAppNodeNumberPerSystem',),
                    ('backupDBNodeNumberPerSystem',),
                    ('spareDBNodePairNumberPerSystem',),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return SystemConfiguration.objects.none()

        obj.project = WorkingProject.objects.all()[0].project

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

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['applicationName', 'activeSubscriber', 'inactiveSubscriber',
                    'trafficTPS', 'deployOption'
                    ]
        return self.readonly_fields

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return ApplicationConfiguration.objects.none()

        traffic_information_list = TrafficInformation.current_objects.all()

        if traffic_information_list.count() > 0:
            app_epay_list = ApplicationName.objects.all().filter(
                name='EPAY',
            )

            # Insert one record for EPAY to ApplicationConfiguration if no EPAY record existed.
            if app_epay_list.count() > 0:
                app_config_epay_list = ApplicationConfiguration.current_objects.all().filter(
                    applicationName=app_epay_list[0],
                )
                if app_config_epay_list.count() == 0:
                    application_config = ApplicationConfiguration.current_objects.create_application_config(
                        project=WorkingProject.objects.all()[0].project,
                        application_name=app_epay_list[0],
                        deployOption='EPAY Node',
                    )
                    application_config.save()

            for traffic_information in traffic_information_list:
                if traffic_information.callType.type == 'Diameter':
                    app_epay_list = ApplicationName.objects.all().filter(
                        name='DRouter',
                    )

                    # Insert one record for DRouter to ApplicationConfiguration if no DRouter record existed
                    # when the traffic is diameter based.
                    if app_epay_list.count() > 0:
                        app_config_epay_list = ApplicationConfiguration.current_objects.all().filter(
                            applicationName=app_epay_list[0],
                        )
                        if app_config_epay_list.count() == 0:
                            application_config = ApplicationConfiguration.current_objects.create_application_config(
                                project=WorkingProject.objects.all()[0].project,
                                application_name=app_epay_list[0],
                                deployOption='DRouter Node',
                            )
                            application_config.save()
                    break

            feature_config_list = FeatureConfiguration.current_objects.all()
            for feature_config in feature_config_list:
                if feature_config.feature.name == 'Online Hierarchy':
                    if feature_config.colocateMemberGroup:
                        deploy_option = 'EPAY Node'
                    else:
                        deploy_option = 'Group Node'
                    app_epay_list = ApplicationName.objects.all().filter(
                        name='Group',
                    )

                    # Insert one record for Group to ApplicationConfiguration if no DRouter record existed
                    # when the traffic is diameter based.
                    if app_epay_list.count() > 0:
                        app_config_epay_list = ApplicationConfiguration.current_objects.all().filter(
                            applicationName=app_epay_list[0],
                        )
                        if app_config_epay_list.count() == 0:
                            application_config = ApplicationConfiguration.current_objects.create_application_config(
                                project=WorkingProject.objects.all()[0].project,
                                application_name=app_epay_list[0],
                                deployOption=deploy_option,
                            )
                            application_config.save()
                    break

        app_config_list = ApplicationConfiguration.current_objects.all()

        for app_config in app_config_list:
            if app_config.trafficTPS == 0:
                if app_config.applicationName.name == 'EPAY':
                    app_config.trafficTPS = app_config.get_tps_for_epay()
                elif app_config.applicationName.name == 'DRouter':
                    app_config.trafficTPS = app_config.get_tps_for_drouter()
                elif app_config.applicationName.name == 'EPPSM':
                    app_config.trafficTPS = app_config.get_tps_for_eppsm()
                elif app_config.applicationName.name == 'Group':
                    app_config.trafficTPS = app_config.get_tps_for_group()
                elif app_config.applicationName.name == 'eCTRL':
                    app_config.trafficTPS = app_config.get_tps_for_ectrl()

                app_config.trafficTPS = float('%.04f'%app_config.trafficTPS)
                app_config.save()

        return super(ApplicationConfigurationAdmin, self).get_queryset(request).filter(
            project=WorkingProject.objects.all()[0].project,
        ).exclude(Q(applicationName__name='EPAY')|Q(applicationName__name='Group'))


    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
                    ('trafficTPS',),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
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
    list_display = ('applicationName', 'calCPUAppNumber', 'calMemAppNumber', 'calDBNumber',
                    'calIONumber', 'appNodeNumber', 'dbNodeNumber', 'ioNodeNumber', 'boundType', )
    list_display_links = None
    # form = ApplicationConfigurationForm

    list_filter = ('applicationName',)

    search_fields = ('applicationName__name',)

    # change_list_template = "path/to/change_list.html"
    #@logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def has_change_permission(self, request, obj=None):
    #     return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_add_permission(self, request):
        return False
        # if CalculatedResult.objects.all().filter(project=WorkingProject.objects.all()[0].project).count() > 0:
        #     return False
        # else:
        #     return True

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_delete_permission(self, request, obj=None):
        return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['applicationName', 'appNodeNumber', 'dbNodeNumber',
                    'ioNodeNumber'
                    ]
        return self.readonly_fields

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CalculatedResult.objects.none()
        return super(CalculatedResultAdmin, self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('Application Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('applicationName',),
                ]}),
            ('Calculated Nodes Information', {
                'fields': [
                    ('calCPUAppNumber', 'calMemAppNumber', 'calDBNumber', 'calIONumber', 'appNodeNumber', 'dbNodeNumber',),
                    ('ioNodeNumber', 'boundType'),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CalculatedResult.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(CalculatedResultAdmin, self).save_model(request, obj, form, change)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [url(r'^project/calculatedresult/calculate/$', self.admin_site.admin_view(self.calculate)), ]

        return my_urls + urls

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def check_for_application(self, app_config, call_type_name):
        if app_config.trafficTPS <= 0:
            app_config.trafficTPS = app_config.get_tps_for_group()

            if app_config.trafficTPS <= 0:
                return None

        traffic_list = TrafficInformation.current_objects.all().filter(
            callType__name=call_type_name,
        )
        if traffic_list.count() <= 0:
            call_type_list = CallType.objects.all().filter(
                name=call_type_name,
            )
            if call_type_list.count() > 0:
                traffic_information = TrafficInformation.current_objects.create_traffic_information(
                    project=app_config.project,
                    call_type=call_type_list[0],
                    activeSubscriber=app_config.activeSubscriber,
                    inactiveSubscriber=app_config.inactiveSubscriber,
                    trafficBHTA=app_config.trafficBHTA,
                    trafficTPS=app_config.trafficTPS,
                    callHoldingTime=1,
                )
                traffic_information.save()
        else:
            traffic_list.update(
                activeSubscriber=app_config.activeSubscriber,
                inactiveSubscriber=app_config.inactiveSubscriber,
                trafficBHTA=app_config.trafficBHTA,
                trafficTPS=app_config.trafficTPS,
                callHoldingTime=1,
            )
            traffic_list[0].save()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate(self, request):
        # print('doing evil with', CalculatedResult.objects.get(pk=int(pk)))
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)

        CalculatedResult.current_objects.all().delete()

        app_config_list = ApplicationConfiguration.current_objects.all()

        for app_config in app_config_list:
            if app_config.activeSubscriber <= 0:
                if ApplicationConfiguration.current_objects.count() > 0:
                    app_config.project_information = ApplicationConfiguration.current_objects.all()[0]
                    app_config.activeSubscriber = app_config.project_information.activeSubscriber
                    app_config.inactiveSubscriber = app_config.project_information.inactiveSubscriber

            if app_config.trafficBHTA <= 0 and app_config.activeSubscriber > 0:
                app_config.trafficBHTA = app_config.trafficTPS * 3600 / app_config.activeSubscriber

            app_config.save()

            sll_application = 1
            if app_config.applicationName.name == 'EPAY':
                application_name_list = ApplicationName.objects.all().filter(name='EPAY')
            elif app_config.applicationName.name == 'Group':
                self.check_for_application(app_config, 'Group side transaction for OH')
                application_name_list = ApplicationName.objects.all().filter(name='Group')
            elif app_config.applicationName.name == 'DRouter':
                self.check_for_application(app_config, 'DRouter transaction')
                application_name_list = ApplicationName.objects.all().filter(name='DRouter')
            elif app_config.applicationName.name == 'EPPSM':
                self.check_for_application(app_config, 'EPPSM transaction')
                application_name_list = ApplicationName.objects.all().filter(name='EPPSM')
            elif app_config.applicationName.name == 'eCTRL':
                self.check_for_application(app_config, 'eCTRL call')
                application_name_list = ApplicationName.objects.all().filter(name='eCTRL')
            else:
                sll_application = 0

            if app_config.deployOption == 'EPAY Node':
                application_name_list = ApplicationName.objects.all().filter(name='EPAY')
            elif app_config.deployOption == 'DRouter Node':
                application_name_list = ApplicationName.objects.all().filter(name='DRouter')
            elif app_config.deployOption == 'Group Node':
                application_name_list = ApplicationName.objects.all().filter(name='Group')
            elif app_config.deployOption == 'eCTRL Node':
                application_name_list = ApplicationName.objects.all().filter(name='eCTRL')
            elif app_config.deployOption == 'EPPSM Node':
                application_name_list = ApplicationName.objects.all().filter(name='EPPSM')
            elif app_config.deployOption == 'CDR Pre-Processor Node':
                application_name_list = ApplicationName.objects.all().filter(name='CDRPP')
            elif app_config.deployOption == 'eCGS Node':
                application_name_list = ApplicationName.objects.all().filter(name='eCGS')
            elif app_config.deployOption == 'NTGW Node':
                application_name_list = ApplicationName.objects.all().filter(name='NTGW')
            elif app_config.deployOption == 'GRouter Node':
                application_name_list = ApplicationName.objects.all().filter(name='GRouter')

            if sll_application == 1:
                app_config.calculate_for_sll_application()
            else:
                app_config.calculate_for_non_sll_application()

            if application_name_list.count() > 0:
                calculated_result_list = CalculatedResult.current_objects.all().filter(
                    project=WorkingProject.objects.all()[0].project,
                    applicationName=application_name_list[0],
                )
                if calculated_result_list.count() > 0:
                    calculated_result_list.update(
                        calCPUAppNumber=app_config.cpuBaseNodeNumber+calculated_result_list[0].calCPUAppNumber,
                        calMemAppNumber=app_config.memoryBaseNodeNumber+calculated_result_list[0].calMemAppNumber,
                        calDBNumber=app_config.dbNodeNumberNeeded+calculated_result_list[0].calDBNumber,
                        calIONumber=app_config.ioNodeNumberNeeded+calculated_result_list[0].calIONumber,
                        appNodeNumber=app_config.nodeNumberNeeded + calculated_result_list[0].appNodeNumber,
                        dbNodeNumber=app_config.dbNodeNumberNeeded + calculated_result_list[0].dbNodeNumber,
                        ioNodeNumber=app_config.ioNodeNumberNeeded + calculated_result_list[0].ioNodeNumber,
                    )
                    calculated_result_list[0].save()
                else:
                    calculated_result = CalculatedResult.current_objects.create_calculated_result(
                        project=WorkingProject.objects.all()[0].project,
                        application_name=application_name_list[0],
                        cal_cpu_app_number=app_config.cpuBaseNodeNumber,
                        cal_mem_app_number=app_config.memoryBaseNodeNumber,
                        cal_db_number=app_config.dbNodeNumberNeeded,
                        cal_io_number=app_config.ioNodeNumberNeeded,
                        app_node_number=app_config.nodeNumberNeeded,
                        db_node_number=app_config.dbNodeNumberNeeded,
                        io_node_number=app_config.ioNodeNumberNeeded,
                    )
                    calculated_result.save()

        calculated_result_list = CalculatedResult.current_objects.all().filter(
            project=WorkingProject.objects.all()[0].project,
        )

        for calculated_result in calculated_result_list:
            calculated_result.appNodeNumber = math.ceil(
                max([calculated_result.calCPUAppNumber, calculated_result.calMemAppNumber]))

            if calculated_result.applicationName.name == 'EPAY':
                if calculated_result.calCPUAppNumber > calculated_result.calMemAppNumber:
                    calculated_result.boundType = 'CPU Bound'
                else:
                    calculated_result.boundType = 'Memory Bound'
            else:
                calculated_result.boundType = '-'


            calculated_result.ioNodeNumber = math.ceil(calculated_result.calIONumber)
            calculated_result.dbNodeNumber = math.ceil(calculated_result.calDBNumber)
            calculated_result.save()

        return redirect('/admin/project/calculatedresult/')

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/other_application_information.js',
              )


class DimensioningResultAdmin(admin.ModelAdmin):

    list_display = ('applicationName', 'systemNumber', 'pilotNodeNeededNumber', 'appNodeNeededNumber', 'dbNodeNeededNumber',
                    'ioNodeNeededNumber', 'mateNodeNeededNumber', 'totalNodeNeededNumber', )
    list_display_links = None
    # form = ApplicationConfigurationForm

    list_filter = ('applicationName',)

    search_fields = ('applicationName__name',)

    # change_list_template = "path/to/change_list.html"
    #@logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def has_change_permission(self, request, obj=None):
    #     return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_add_permission(self, request):
        return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def has_delete_permission(self, request, obj=None):
        return False

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_readonly_fields(self, request, obj=None):
        if WorkingProject.objects.count() == 0:
            return ['applicationName', 'systemNumber', 'appNodeNeededNumber', 'dbNodeNeededNumber',
                    'ioNodeNeededNumber', 'pilotNodeNeededNumber', 'mateNodeNeededNumber', 'totalNodeNeededNumber',
                    ]
        return self.readonly_fields

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_queryset(self, request):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return CalculatedResult.objects.none()
        return super(DimensioningResultAdmin, self).get_queryset(request). \
            filter(
            project=WorkingProject.objects.all()[0].project,
        )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_fieldsets(self, request, obj=None):
        addition_message = ''
        fields_row1 = ()
        if WorkingProject.objects.count() == 0:
            addition_message = ' -- Please set working project first!'
        return [
            ('Application Information' + addition_message, {
                'fields': [
                    fields_row1,
                    ('applicationName',),
                ]}),
            ('Calculated Nodes Information', {
                'fields': [
                    ('systemNumber', 'totalNodeNeededNumber',),
                    ('appNodeNeededNumber', 'dbNodeNeededNumber',),
                    ( 'pilotNodeNeededNumber', 'ioNodeNeededNumber', ),
                ]}),
        ]

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def save_model(self, request, obj, form, change):
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)
            return DimensioningResult.objects.none()
        obj.project = WorkingProject.objects.all()[0].project
        super(DimensioningResultAdmin, self).save_model(request, obj, form, change)

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [url(r'^project/dimensioningresult/calculate/$', self.admin_site.admin_view(self.calculate)), ]

        return my_urls + urls

    # @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    # def check_for_application(self, app_config, call_type_name):
    #     if app_config.trafficTPS <= 0:
    #         app_config.trafficTPS = app_config.get_tps_for_group()
    #
    #         if app_config.trafficTPS <= 0:
    #             return None
    #
    #     traffic_list = TrafficInformation.current_objects.all().filter(
    #         callType__name=call_type_name,
    #     )
    #     if traffic_list.count() <= 0:
    #         call_type_list = CallType.objects.all().filter(
    #             name=call_type_name,
    #         )
    #         if call_type_list.count() > 0:
    #             traffic_information = TrafficInformation.current_objects.create_traffic_information(
    #                 project=app_config.project,
    #                 call_type=call_type_list[0],
    #                 activeSubscriber=app_config.activeSubscriber,
    #                 inactiveSubscriber=app_config.inactiveSubscriber,
    #                 trafficBHTA=app_config.trafficBHTA,
    #                 trafficTPS=app_config.trafficTPS,
    #                 callHoldingTime=1,
    #             )
    #             traffic_information.save()
    #     else:
    #         traffic_list.update(
    #             activeSubscriber=app_config.activeSubscriber,
    #             inactiveSubscriber=app_config.inactiveSubscriber,
    #             trafficBHTA=app_config.trafficBHTA,
    #             trafficTPS=app_config.trafficTPS,
    #             callHoldingTime=1,
    #         )
    #         traffic_list[0].save()

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def calculate(self, request):
        # print('doing evil with', CalculatedResult.objects.get(pk=int(pk)))
        if WorkingProject.objects.count() == 0:
            self.message_user(request, 'Please set working project first!', level=messages.ERROR)

        DimensioningResult.current_objects.all().delete()

        calculated_result_list = CalculatedResult.current_objects.all()

        for calculated_result in calculated_result_list:
            dimensioning_result = DimensioningResult.current_objects.create_dimensioning_result(
                project=calculated_result.project,
                application_name=calculated_result.applicationName,
                calculated_app_node_number = calculated_result.appNodeNumber,
                calculated_db_node_number = calculated_result.dbNodeNumber,
                calculated_io_node_number = calculated_result.ioNodeNumber,
                calculated_system_number = calculated_result.systemNumber,
                bound_type = calculated_result.boundType,
            )
            if calculated_result.applicationName.name == 'EPAY' or \
                            calculated_result.applicationName.name == 'Group' or \
                            calculated_result.applicationName.name == 'DRouter' or \
                            calculated_result.applicationName.name == 'EPPSM' or \
                            calculated_result.applicationName.name == 'eCTRL':
                dimensioning_result.calculate_for_sll_application()
            else:
                dimensioning_result.calculate_for_non_sll_application()
        #     if app_config.activeSubscriber <= 0:
        #         if ApplicationConfiguration.current_objects.count() > 0:
        #             app_config.project_information = ApplicationConfiguration.current_objects.all()[0]
        #             app_config.activeSubscriber = app_config.project_information.activeSubscriber
        #             app_config.inactiveSubscriber = app_config.project_information.inactiveSubscriber
        #
        #     if app_config.trafficBHTA <= 0 and app_config.activeSubscriber > 0:
        #         app_config.trafficBHTA = app_config.trafficTPS * 3600 / app_config.activeSubscriber
        #
        #     app_config.save()
        #
        #     sll_application = 1
        #     if app_config.applicationName.name == 'EPAY':
        #         application_name_list = ApplicationName.objects.all().filter(name='EPAY')
        #     elif app_config.applicationName.name == 'Group':
        #         self.check_for_application(app_config, 'Group side transaction for OH')
        #         application_name_list = ApplicationName.objects.all().filter(name='Group')
        #     elif app_config.applicationName.name == 'DRouter':
        #         self.check_for_application(app_config, 'DRouter transaction')
        #         application_name_list = ApplicationName.objects.all().filter(name='DRouter')
        #     elif app_config.applicationName.name == 'EPPSM':
        #         self.check_for_application(app_config, 'EPPSM transaction')
        #         application_name_list = ApplicationName.objects.all().filter(name='EPPSM')
        #     elif app_config.applicationName.name == 'eCTRL':
        #         self.check_for_application(app_config, 'eCTRL call')
        #         application_name_list = ApplicationName.objects.all().filter(name='eCTRL')
        #     else:
        #         sll_application = 0
        #
        #     if app_config.deployOption == 'EPAY Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='EPAY')
        #     elif app_config.deployOption == 'DRouter Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='DRouter')
        #     elif app_config.deployOption == 'Group Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='Group')
        #     elif app_config.deployOption == 'eCTRL Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='eCTRL')
        #     elif app_config.deployOption == 'EPPSM Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='EPPSM')
        #     elif app_config.deployOption == 'CDR Pre-Processor Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='CDRPP')
        #     elif app_config.deployOption == 'eCGS Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='eCGS')
        #     elif app_config.deployOption == 'NTGW Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='NTGW')
        #     elif app_config.deployOption == 'GRouter Node':
        #         application_name_list = ApplicationName.objects.all().filter(name='GRouter')
        #
        #     if sll_application == 1:
        #         app_config.calculate_for_sll_application()
        #     else:
        #         app_config.calculate_for_non_sll_application()
        #
        #     if application_name_list.count() > 0:
        #         calculated_result_list = CalculatedResult.current_objects.all().filter(
        #             project=WorkingProject.objects.all()[0].project,
        #             applicationName=application_name_list[0],
        #         )
        #         if calculated_result_list.count() > 0:
        #             calculated_result_list.update(
        #                 calCPUAppNumber=app_config.cpuBaseNodeNumber+calculated_result_list[0].calCPUAppNumber,
        #                 calMemAppNumber=app_config.memoryBaseNodeNumber+calculated_result_list[0].calMemAppNumber,
        #                 calDBNumber=app_config.dbNodeNumberNeeded+calculated_result_list[0].calDBNumber,
        #                 calIONumber=app_config.ioNodeNumberNeeded+calculated_result_list[0].calIONumber,
        #                 appNodeNumber=app_config.nodeNumberNeeded + calculated_result_list[0].appNodeNumber,
        #                 dbNodeNumber=app_config.dbNodeNumberNeeded + calculated_result_list[0].dbNodeNumber,
        #                 ioNodeNumber=app_config.ioNodeNumberNeeded + calculated_result_list[0].ioNodeNumber,
        #             )
        #             calculated_result_list[0].save()
        #         else:
        #             calculated_result = CalculatedResult.current_objects.create_calculated_result(
        #                 project=WorkingProject.objects.all()[0].project,
        #                 application_name=application_name_list[0],
        #                 cal_cpu_app_number=app_config.cpuBaseNodeNumber,
        #                 cal_mem_app_number=app_config.memoryBaseNodeNumber,
        #                 cal_db_number=app_config.dbNodeNumberNeeded,
        #                 cal_io_number=app_config.ioNodeNumberNeeded,
        #                 app_node_number=app_config.nodeNumberNeeded,
        #                 db_node_number=app_config.dbNodeNumberNeeded,
        #                 io_node_number=app_config.ioNodeNumberNeeded,
        #             )
        #             calculated_result.save()
        #
        # calculated_result_list = CalculatedResult.current_objects.all().filter(
        #     project=WorkingProject.objects.all()[0].project,
        # )
        #
        # for calculated_result in calculated_result_list:
        #     calculated_result.appNodeNumber = math.ceil(
        #         max([calculated_result.calCPUAppNumber, calculated_result.calMemAppNumber]))
        #
        #     if calculated_result.applicationName.name == 'EPAY':
        #         if calculated_result.calCPUAppNumber > calculated_result.calMemAppNumber:
        #             calculated_result.boundType = 'CPU Bound'
        #         else:
        #             calculated_result.boundType = 'Memory Bound'
        #     else:
        #         calculated_result.boundType = '-'
        #
        #
        #     calculated_result.ioNodeNumber = math.ceil(calculated_result.calIONumber)
        #     calculated_result.dbNodeNumber = math.ceil(calculated_result.calDBNumber)
        #     calculated_result.save()
        #
        # return redirect('/admin/project/calculatedresult/')

    class Media:
        js = ('/static/jquery-2.1.1.min.js',
              '/static/js/other_application_information.js',
              )


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
admin.site.register(DimensioningResult, DimensioningResultAdmin)

