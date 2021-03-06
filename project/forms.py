from django import forms
from django.forms import fields,TextInput,Textarea

from django.template import Template

from .models import Project, ProjectInformation, WorkingProject, TrafficInformation, \
    FeatureConfiguration, DBConfiguration, CounterConfiguration, \
    CallTypeCounterConfiguration, SystemConfiguration, ApplicationConfiguration, DEPLOY_OPTION
    # Address, Country
from hardware.models import HardwareType, HardwareModel, CPUTuning, MemoryUsageTuning, \
    CPUList, MemoryList, VMType
from service.models import Release, CallType, FeatureName, DBInformation, ApplicationName
from common.models import DBMode

from django.forms.models import ModelForm
from django.db.models import Q

from django.urls import reverse_lazy
from django.forms import ChoiceField, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from clever_selects.form_fields import ChainedChoiceField, ChainedModelChoiceField
from clever_selects.forms import ChainedChoicesForm, ChainedChoicesModelForm

from django.contrib import messages

from common import logger
from common.logger import logged
import sys
import os.path


# class AddressForm(forms.Form):
    # country = AutoCompleteSelectField('countries', required=True, help_text="")
    # state = AutoCompleteSelectField('states',required=True, help_text="")
    #city = AutoCompleteSelectField('cities',required=True,help_text="")

#     province = forms.ModelChoiceField(Province.objects.all())
#     city = forms.ModelChoiceField(City.objects.none())

#     def _raw_value(form, fieldname):
#         field = form.fields[fieldname]
#         prefix = form.add_prefix(fieldname)
#         return field.widget.value_from_datadict(form.data, form.files, prefix)

#     def __init__(self, *args, **kwargs):
#         forms.Form.__init__(self, *args, **kwargs)
#         provinces = Province.objects.all()
#         if len(provinces)==1:
#             self.fields['province'].initial=provinces[0].pk

#         province_id=self.fields['province'].initial or self.initial.get('province') \
#                   or self._raw_value('province')
#         if province_id:
            # parent is known. Now I can display the matching children.
#             cities = City.objects.filter(country__id=province_id)
#             self.fields['cities'].queryset=cities
#             if len(cities)==1:
#                 self.fields['cities'].initial=cities[0].pk



    # class Meta:
    #     model = SelectP
    #
    #     fields="__all__"

# class SelectForm(forms.ModelForm):
#     class Meta:
#         model = SelectP
#         fields = '__all__'


# class ProjectForm(forms.ModelForm):
#     # name = fields.CharField(widget=TextInput(attrs={'size': 19,}),required=False,label='name')
#     # comment = fields.CharField(widget=Textarea(attrs={'rows':3,'cols':85}),required=False,label= 'comment')
#     # hardwareType = fields.m(widget=)
#
#     class Meta:
#         model = Project
#         fields = '__all__'

class ProjectForm(ChainedChoicesModelForm):
    release = forms.ModelChoiceField(
        Release.objects.all().order_by('-sequence'),
        empty_label=_(u'Select a Release'),
        # help_text=_(u'Select a VM Type'),
        label='Release',
    )

    database_type = forms.ModelChoiceField(
        DBMode.objects.all(),
        empty_label=_(u'Select a Database Type'),
        # help_text=_(u'Select a VM Type'),
        label='Database Type',
        initial=DBMode.objects.all().filter(name='NDB')[0].pk,
    )

    hardwareType = ModelChoiceField(queryset=HardwareType.objects.all(),
                                    required=True,
                                    empty_label=_(u'Select a hardware type'),
                                    label='Hardware Type')
    hardwareModel = ChainedModelChoiceField(parent_field='hardwareType',
                                            ajax_url=reverse_lazy('ajax_hardware_models'),
                                            empty_label=_(u'Select a CPU model'),
                                            model=HardwareModel,
                                            required=True,
                                            label='CPU Model')

    class Meta:
        model = Project
        fields = ['name', 'release', 'hardwareType', 'hardwareModel', 'customer', 'version', 'database_type', 'comment',]

    # def __init__(self, data=None, *args, **kwargs):
    #     super(ProjectForm, self).__init__(*args, **kwargs)
    #
    #     project_list = Project.objects.all().filter(
    #         name=self.fields['name'],
    #     )
    #
    #     if project_list.count() > 0:
    #         self.initial['hardwareType'] = project_list[0].hardwareType
    #         self.initial['hardwareModel'] = project_list[0].hardwareModel
    # #
    #     project = WorkingProject.objects.all()[0].project
    #
    #     if project_information_list.count() > 0:
    #         a = project_information_list[0]
    #         b = a.cpuNumber
    #         self.initial['cpuNumber'] =project_information_list[0].cpuNumber
    #     else:
    #         self.initial['cpuNumber'] = CPUList.objects.all().filter(
    #             hardwareModel=project.hardwareModel,
    #             cpuNumber=project.hardwareModel.defaultCPUNumber
    #         )[0].pk

class ProjectInformationForm(forms.ModelForm):

    if WorkingProject.objects.count() > 0:
        project = WorkingProject.objects.all()[0].project

        if project.hardwareType.isVM:
        # if 1:
            vmType = forms.ModelChoiceField(
                queryset=VMType.objects.all().filter(
                    ~Q(type='Native'),
                ),
                empty_label=_(u'Select a VM Type'),
                # help_text=_(u'Select a VM Type'),
                label='VM Type',
                initial=VMType.objects.all().filter(type='CBIS')[0].pk
            )

            if CPUList.objects.all().filter(
                    hardwareModel=project.hardwareModel,
                    cpuNumber=project.hardwareModel.defaultCPUNumber
            ).count() > 0:
                cpuNumber = forms.ModelChoiceField(
                    queryset=CPUList.objects.all().filter(
                        hardwareModel=project.hardwareModel
                    ),
                    empty_label=_(u'Select a CPU Number'),
                    label='CPU Number',
                    initial=CPUList.objects.all().filter(
                        hardwareModel=project.hardwareModel,
                        cpuNumber=project.hardwareModel.defaultCPUNumber
                    )[0].pk,
                )

            else:
                cpuNumber = forms.ModelChoiceField(
                    queryset=CPUList.objects.all().filter(
                        hardwareModel=project.hardwareModel
                    ),
                    empty_label=_(u'Select a CPU Number'),
                    label='CPU Number',
                    initial=CPUList.objects.none(),
                )

            clientNumber = forms.IntegerField(
                label='Client Number',
                initial=project.hardwareModel.defaultClientNumber,
            )

        else:
            vmType = VMType.objects.all().filter(type='Native')[0].pk
            if CPUList.objects.all().filter(
                    hardwareModel=project.hardwareModel,
                    cpuNumber=project.hardwareModel.defaultCPUNumber
            ).count() > 0:
                cpuNumber = forms.ModelChoiceField(
                    queryset=CPUList.objects.all().filter(
                        hardwareModel=project.hardwareModel
                    ),
                    empty_label=_(u'Select a client Number'),
                    label='Client Number',
                    initial=CPUList.objects.all().filter(
                        hardwareModel=project.hardwareModel,
                        cpuNumber=project.hardwareModel.defaultCPUNumber
                    )[0].pk,
                )

            else:
                cpuNumber = forms.ModelChoiceField(
                    queryset=CPUList.objects.all().filter(
                        hardwareModel=project.hardwareModel
                    ),
                    empty_label=_(u'Select a client Number'),
                    label='Client Number',
                    initial=CPUList.objects.none(),
                )

        memory = forms.ModelChoiceField(
            queryset=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a Memory'),
            label='Memory (G)',
            initial=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                memory=project.hardwareModel.defaultMemory
            )[0].pk,
        )

        dbMemory = forms.ModelChoiceField(
            queryset=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a Memory for DB Node'),
            label='DB Memory (G)',
            required=False,
            initial=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                memory=project.hardwareModel.defaultMemory
            )[0].pk,
        )

        dbCPUNumber = forms.ModelChoiceField(
            queryset=CPUList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a CPU Number for DB Node'),
            label='DB CPU Number',
            required=False,
            initial=CPUList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                cpuNumber=project.hardwareModel.defaultCPUNumber
            )[0].pk,
        )

        pilotMemory = forms.ModelChoiceField(
            queryset=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a Memory for Pilot Node'),
            label='Pilot Memory (G)',
            required=False,
            initial=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                memory=project.hardwareModel.defaultPilotMemory,
            )[0].pk,
        )

        pilotCPUNumber = forms.ModelChoiceField(
            queryset=CPUList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a CPU Number for Pilot Node'),
            label='Pilot CPU Number',
            required=False,
            initial=CPUList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                cpuNumber=project.hardwareModel.defaultPilotCPUNumber,
            )[0].pk,
        )

        ioMemory = forms.ModelChoiceField(
            queryset=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a Memory for IO Node'),
            label='IO Memory (G)',
            required=False,
            initial=MemoryList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                memory=project.hardwareModel.defaultIOMemory,
            )[0].pk,
        )

        ioCPUNumber = forms.ModelChoiceField(
            queryset=CPUList.objects.all().filter(
                hardwareModel=project.hardwareModel
            ),
            empty_label=_(u'Select a CPU Number for IO Node'),
            label='IO CPU Number',
            required=False,
            initial=CPUList.objects.all().filter(
                hardwareModel=project.hardwareModel,
                cpuNumber=project.hardwareModel.defaultIOCPUNumber,
            )[0].pk,
        )



        cpuUsageTuning = forms.ModelChoiceField(
            CPUTuning.objects.all().filter(
                dbMode=project.database_type,
                hardwareType=project.hardwareType
            ),
            empty_label=_(u'Select a CPU Usage Tuning Option'),
            label='CPU Usage Tuning',

            initial=CPUTuning.objects.all().filter(
                dbMode=project.database_type,
                hardwareType=project.hardwareType,
                tuningOption='Normal'
            )[0].pk
        )

        memoryUsageTuning = forms.ModelChoiceField(
            MemoryUsageTuning.objects.all(),
            empty_label=_(u'Select a Memory Usage Tuning Option'),
            label='Memory Usage Tuning',
            initial=MemoryUsageTuning.objects.all().filter(
                name='Normal'
            )[0].pk
        )
        activeSubscriber = forms.IntegerField(
            localize = True,
            label='Active Subscribers',
        )

        inactiveSubscriber = forms.IntegerField(
            localize = True,
            label='Inactive Subscribers',
        )

        groupAccountNumber = forms.IntegerField(
            localize = True,
            label='Number of Group Account',
        )

        # sigtranLinkSpeed = forms.IntegerField(initial=10000)
        # sigtranLinkNumber = forms.IntegerField(initial=1)
        # sigtranPortUtil = forms.FloatField(initial=0.3)
    else:
        cpuNumber = forms.ModelChoiceField(CPUList.objects.none())
        memory = forms.ModelChoiceField(MemoryList.objects.none())
        dbCPUNumber = forms.ModelChoiceField(CPUList.objects.none())
        dbMemory = forms.ModelChoiceField(MemoryList.objects.none())
        cpuUsageTuning = forms.ModelChoiceField(CPUTuning.objects.none())
        memoryUsageTuning = forms.ModelChoiceField(MemoryUsageTuning.objects.none())

    class Meta:
        model = ProjectInformation
        fields = '__all__'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        # if 'cpuNumber' not in self.cleaned_data:
        #     self.cleaned_data['cpuNumber'] = self.data['cpuNumber']
        #
        # if 'memory' not in self.cleaned_data:
        #     self.cleaned_data['memory'] = self.data['memory']

        if 'dbCPUNumber' not in self.cleaned_data:
            self.cleaned_data['dbCPUNumber'] = self.cleaned_data['cpuNumber']
            self.cleaned_data['dbMemory'] = self.cleaned_data['memory']

        cleaned_data = super(ProjectInformationForm, self).clean()

        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )


    # def __init__(self, data=None, *args, **kwargs):
    #     super(ProjectInformationForm, self).__init__(*args, **kwargs)
    #
    #     if WorkingProject.objects.count() == 0:
    #         raise forms.ValidationError(
    #             "Please set working project first!"
    #         )
    #
    #     project_information_list = ProjectInformation.current_objects.all()
    #
    #     project = WorkingProject.objects.all()[0].project
    #
    #     if project_information_list.count() > 0:
    #         a = project_information_list[0]
    #         b = a.cpuNumber
    #         self.initial['cpuNumber'] =project_information_list[0].cpuNumber
    #     else:
    #         self.initial['cpuNumber'] = CPUList.objects.all().filter(
    #             hardwareModel=project.hardwareModel,
    #             cpuNumber=project.hardwareModel.defaultCPUNumber
    #         )[0].pk







    # def is_valid(self):
    #     if WorkingProject.objects.count() == 0:
    #         self.add_error('project', 'Please set working project first!')
    #     return super(ProjectInformationForm, self).is_valid()

class TrafficInformationForm(forms.ModelForm):
    if WorkingProject.objects.count() > 0:
        callType = forms.ModelChoiceField(
            queryset= CallType.objects.all().filter(
                isShow=True,
            ),
            empty_label=_(u'Select a Call Type'),
            label='Call Type',
        )

        if ProjectInformation.objects.all().filter(project=WorkingProject.objects.all()[0].project).count() > 0:
            activeSubscriber = forms.IntegerField(
                localize = True,
                label='Active Subscribers',
                # initial=ProjectInformation.objects.all().filter(
                    # project=WorkingProject.objects.all()[0].project
                # )[0].activeSubscriber
            )
            inactiveSubscriber = forms.IntegerField(
                localize = True,
                label='Inactive Subscribers',
                # initial=ProjectInformation.objects.all().filter(
                #     project=WorkingProject.objects.all()[0].project)[0].inactiveSubscriber,
            )
        else:
            activeSubscriber = forms.IntegerField(
                label='Active Subscribers',
                initial=0,
                localize = True,
            )
            inactiveSubscriber = forms.IntegerField(
                label='Inactive Subscribers',
                initial=0,
                localize = True,
            )
    else:
        callType = forms.ModelChoiceField(
            CallType.objects.none(),
        )
        activeSubscriber = forms.IntegerField(
            label='Active Subscribers',
            initial=0,
            localize = True,
        )
        inactiveSubscriber = forms.IntegerField(
            label='Inactive Subscribers',
            initial=0,
            localize = True,
        )

    callHoldingTime = forms.FloatField(
        label='Call Holding Time (s)',
        initial=0,
        localize = True,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    averageActiveSessionPerSubscriber = forms.FloatField(
        label='Average Active Session Number per Subscriber',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    averageCategoryPerCCR = forms.FloatField(
        label='Average Category Number per CCR',
        initial=1,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    averageCategoryPerSession = forms.FloatField(
        label='Average Category Number per Session         ',
        initial=1,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    volumeCCRiBHTA = forms.FloatField(
        label='Volume: CCRi BHTA',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    volumeCCRuBHTA = forms.FloatField(
        label='CCRu BHTA',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    volumeCCRtBHTA = forms.FloatField(
        label='CCRt BHTA',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    timeCCRiBHTA = forms.FloatField(
        label='Time: CCRi BHTA',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    timeCCRuBHTA = forms.FloatField(
        label='CCRu BHTA',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    timeCCRtBHTA = forms.FloatField(
        label='CCRt BHTA',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    class Meta:
        model = TrafficInformation

        fields = '__all__'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(TrafficInformationForm, self).clean()
        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )

        callType = self.cleaned_data.get("callType")

        callHoldingTime = self.cleaned_data.get("callHoldingTime")

        averageActiveSessionPerSubscriber = self.cleaned_data.get("averageActiveSessionPerSubscriber")

        if (callType.name.find("Diameter Session") != -1):
            if ((callHoldingTime == 0) and (averageActiveSessionPerSubscriber ==0)):
                raise forms.ValidationError(
                    _('Call Holding Time or Average Active Session Number per Subscriber should be > 0!'))

        # if (TrafficInformation.objects.all().count() > 0):
        #     if TrafficInformation.objects.all().filter(
        #         project=WorkingProject.objects.all()[0].project,
        #         callType=callType,).count() > 0:
        #         raise forms.ValidationError(
        #             _('Call Type: %s existed!')%callType)

class FeatureConfigurationForm(forms.ModelForm):

    if WorkingProject.objects.count() > 0:
        feature = forms.ModelChoiceField(
            FeatureName.objects.all(),
            empty_label=_(u'Select a Feature Name'),
            # help_text=_(u'Select a VM Type'),
            label='Feature Name',
        )
    else:
        feature = forms.ModelChoiceField(
            FeatureName.objects.none(),
            empty_label=_(u'Select a Feature Name'),
            # help_text=_(u'Select a VM Type'),
            label='Feature Name',
        )

    featurePenetration = forms.FloatField(
        label='Feature Penetration (%)',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    colocateMemberGroup = forms.BooleanField(
        label='Group Collocated with Member',
        initial=True,
        required=False,
    )

    rtdbSolution = forms.BooleanField(
        label='RTDB Solution',
        initial=True,
        required=False,
    )

    groupNumber = forms.FloatField(
        label='Group Number',
        initial=1,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    ratioOfLevel1 = forms.FloatField(
        label='Ratio of One Level',
        initial=1,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    class Meta:
        model = FeatureConfiguration

        fields = '__all__'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(FeatureConfigurationForm, self).clean()
        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )

        feature = self.cleaned_data.get("feature")
        featurePenetration = self.cleaned_data.get("featurePenetration")

        if featurePenetration <= 0:
            raise forms.ValidationError(
                _('Feature Penetration should be > 0!'))

        if featurePenetration >100:
            raise forms.ValidationError(
                _('Feature Penetration should be <= 100!'))

        # if (FeatureConfiguration.objects.all().count() > 0):
        #     if FeatureConfiguration.objects.all().filter(
        #             project=WorkingProject.objects.all()[0].project,
        #             feature=feature,).count() > 0:
        #         raise forms.ValidationError(
        #             _('Feature: %s existed!')%feature)

class CounterConfigurationForm(forms.ModelForm):
    averageBundleNumberPerSubscriber = forms.FloatField(
        label='Average Bundle Number Per Subscriber',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    average24hBundleNumberPerSubscriber = forms.FloatField(
        label='Average 24h Bundle Number Per Subscriber',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )
    turnOnBasicCriteriaCheck = forms.BooleanField(
        label='Enable Basic Criteria Check',
        initial=False,
        required=False,
        # widget=forms.CheckboxInput(attrs={'style': 'width:100px, align:left'}),
    )

    generateMultipleAMAForCounter = forms.BooleanField(
        label='Generate Multiple AMA For Counter',
        initial=False,
        required=False,
        # widget=forms.CheckboxInput(attrs={'style': 'width:100px, align:left'}),
    )

    configureForCallType = forms.BooleanField(
        label='Configure Counter For Call Types',
        initial=False,
        required=False,
        # widget=forms.CheckboxInput(attrs={'style': 'width:100px', 'align':'left'}),
    )


    nonAppliedBucketNumber = forms.FloatField(
        label='Non Applied Bucket Number',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    totalCounterNumber = forms.FloatField(
        label='Total Counter Number',
        initial=0,
        disabled=True,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    nonAppliedUBDNumber = forms.FloatField(
        label='Non Applied UBD Number',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    appliedBucketNumber = forms.FloatField(
        label='Applied Bucket Number',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    appliedUBDNumber = forms.FloatField(
        label='Applied UBD Number',
        initial=0,
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    groupBundleNumber = forms.FloatField(
        initial=0,
        label='Number of Group Bundle',
    )
    groupBucketNumber = forms.FloatField(
        initial=0,
        label='Group Bucket Number',
    )

    class Meta:
        model = CounterConfiguration
        fields = '__all__'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(CounterConfigurationForm, self).clean()
        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )

        averageBundleNumberPerSubscriber = self.cleaned_data.get("averageBundleNumberPerSubscriber")
        average24hBundleNumberPerSubscriber = self.cleaned_data.get("average24hBundleNumberPerSubscriber")
        totalCounterNumber = self.cleaned_data.get("totalCounterNumber")

        if average24hBundleNumberPerSubscriber + averageBundleNumberPerSubscriber + totalCounterNumber <= 0:
            raise forms.ValidationError(
                _('Please configure bundle/counter number!'))

            # if (FeatureConfiguration.objects.all().count() > 0):
            #     if FeatureConfiguration.objects.all().filter(
            #             project=WorkingProject.objects.all()[0].project,
            #             feature=feature,).count() > 0:
            #         raise forms.ValidationError(
            #             _('Feature: %s existed!')%feature)


class CallTypeCounterConfigurationForm(forms.ModelForm):
    callType = forms.ModelChoiceField(
        CallType.objects.all().filter(
            isShow=True,
        ),
        label='Call Type',
        disabled=True,
        # widget={forms.Input}
    )
    averageBundleNumberPerSubscriber = forms.FloatField(
        label='Bundle Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    average24hBundleNumberPerSubscriber = forms.FloatField(
        label='24h Bundle Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    nonAppliedBucketNumber = forms.FloatField(
        label='Non Applied Bucket Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    nonAppliedUBDNumber = forms.FloatField(
        label='Non Applied UBD Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    appliedBucketNumber = forms.FloatField(
        label='Applied Bucket Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    appliedUBDNumber = forms.FloatField(
        label='Applied UBD Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    totalCounterNumber = forms.FloatField(
        label='Total Counter Number',
        initial=0,
        disabled=True,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    class Meta:
        model = CallTypeCounterConfiguration
        fields = '__all__'


class DBConfigurationForm(forms.ModelForm):
    application = forms.ModelChoiceField(
        ApplicationName.objects.all().filter(
            needConfigDB=True,
        ),
        empty_label=_(u'Select a Application Name'),
        label='Application Name',
    )
    if WorkingProject.objects.count() > 0:
        dbInfo = forms.ModelChoiceField(
            DBInformation.objects.all().filter(
                release=WorkingProject.objects.all()[0].project.release,
                mode=WorkingProject.objects.all()[0].project.database_type
            ),
            empty_label=_(u'Select a DB Name'),
            label='DB Name',
        )
    else:
        dbInfo = forms.ModelChoiceField(
            DBInformation.objects.none(),
            empty_label=_(u'Select a DB Name'),
            label='DB Name',
        )
    dbFactor = forms.FloatField(
        initial=0,
        label='DB Factor',
    )
    referenceDBFactor = forms.FloatField(
        initial=0,
        label='Reference for DB Factor',
        #disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'width:129px'}),
    )
    recordSize = forms.IntegerField(
        initial=0,
        localize = True,
        label='Record Size',
        #disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    placeholderRatio = forms.FloatField(
        initial=0,
        label='Placeholder Ratio (%)',
    )
    referencePlaceholderRatio = forms.FloatField(
        initial=0,
        label='Reference for Placeholder Ratio',
        disabled=True,
        #widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'width:88px'}),
    )

    MEMBER_GROUP_OPTION = (('Member', 'Member'), ('Group', 'Group'))
    memberGroupOption = forms.ChoiceField(
        initial='Member',
        choices=MEMBER_GROUP_OPTION,
        label='DB Location'
    )
    subscriberNumber = forms.IntegerField(
        initial=0,
        label='Subscriber Number',
        localize = True,
        #disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'width:155px'}),
    )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(DBConfigurationForm, self).clean()
        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )



    class Meta:
        model = DBConfiguration
        fields = '__all__'


class SystemConfigurationForm(forms.ModelForm):
    cabinetNumberPerSystem = forms.IntegerField(
        initial=1,
        label='Number of Cabinet Per System',
        disabled=True,
    )
    applicationName = forms.ModelChoiceField(
        ApplicationName.objects.all(),
        empty_label=_(u'Select an Application Name'),
        label='Application Name'
    )
    backupAppNodeNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Backup App Node Per System',
        # widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    spareAppNodeNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Spare App Node Per System',
        # widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    backupDBNodeNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Backup DB Node Per System',
        # widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )
    spareDBNodePairNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Spare DB Node Pair Per System',
        # widget=forms.NumberInput(attrs={'Style': 'width:100px'}),
    )

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(SystemConfigurationForm, self).clean()
        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )

        application_name = self.cleaned_data.get("applicationName")
        app_conf_list = ApplicationConfiguration.current_objects.all().filter(
            applicationName=application_name,
        )

        if (application_name.name != 'EPAY') and (app_conf_list.count() == 0):
            raise forms.ValidationError(
                _('Application %s has not been configured, please configure first!'%application_name))

        if not self.instance.pk:
            if SystemConfiguration.current_objects.all().filter(
                applicationName=application_name,
            ).count() > 0:
                raise forms.ValidationError(
                    _('Application: %s existed!')%application_name)

    class Meta:
        model = SystemConfiguration
        fields = '__all__'


class ApplicationConfigurationForm(forms.ModelForm):
    applicationName = forms.ModelChoiceField(
        ApplicationName.objects.all().filter(
            ~Q(name__contains='EPAY') & ~Q(name__contains='Group'),
        ),
        empty_label=_(u'Select an Application Name'),
        label='Application Name'
    )

    deployOption = forms.ChoiceField(
        # empty_label=_(u'Select a Deploy Option'),
        choices=DEPLOY_OPTION,
        label='Deploy Option',
    )

    activeSubscriber = forms.IntegerField(
        initial=0,
        localize=True,
        label='Active Subscriber',
    )

    inactiveSubscriber = forms.IntegerField(
        initial=0,
        localize=True,
        label='Inactive Subscriber',
    )

    trafficTPS = forms.FloatField(
        label='CPS/TPS',
        localize=True,
        initial=0,
    )

    class Meta:
        model = ApplicationConfiguration
        fields = '__all__'

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(ApplicationConfigurationForm, self).clean()
        if WorkingProject.objects.count() == 0:
            raise forms.ValidationError(
                "Please set working project first!"
            )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    keep_logged = forms.BooleanField(required=False, label="Keep me logged in")

    # template = Template("""
    # {% form %}
    #     {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
    #     {% part form.password prefix %}<i class="material-icons prefix">lock</i>{% endpart %}
    #     {% attr form.keep_logged 'group' class append %}right-align{% endattr %}
    # {% endform %}
    # """)

    buttons = Template("""
        <button class="waves-effect waves-teal btn-flat">Register</button>
        <button class="waves-effect waves-light btn" type="submit">Login</button>
    """)

    title = "Login form"

    @logged('info', '%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if cleaned_data.get('email') == 'john@doe.com':
            raise forms.ValidationError('John, come on. You are blocked.')
