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

from django.core.urlresolvers import reverse_lazy
from django.forms import ChoiceField, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from clever_selects.form_fields import ChainedChoiceField, ChainedModelChoiceField
from clever_selects.forms import ChainedChoicesForm, ChainedChoicesModelForm

from django.contrib import messages


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

class ProjectForm1(ChainedChoicesModelForm):
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


    hardwareType = ModelChoiceField(queryset=HardwareType.objects.all(), required=True,
                                    empty_label=_(u'Select a hardware type'), label='Hardware Type')
    hardwareModel = ChainedModelChoiceField(parent_field='hardwareType', ajax_url=reverse_lazy('ajax_hardware_models'),
                                    empty_label=_(u'Select a CPU model'), model=HardwareModel, required=True,
                                    label='CPU Model')

    class Meta:
        model = Project
        fields = ['name', 'release', 'hardwareType', 'hardwareModel', 'customer', 'version', 'database_type', 'comment',]
        # fields = ['brand', 'model', ]


class ProjectInformationForm(forms.ModelForm):
    if WorkingProject.objects.count() > 0:
        vmType = forms.ModelChoiceField(
            VMType.objects.all(),
            empty_label=_(u'Select a VM Type'),
            # help_text=_(u'Select a VM Type'),
            label='VM Type',
            initial=VMType.objects.all().filter(type='CBIS')[0].pk
        )

        if CPUList.objects.all().filter(
                hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel,
                cpuNumber=WorkingProject.objects.all()[0].project.hardwareModel.defaultCPUNumber
        ).count() > 0:
            cpuNumber = forms.ModelChoiceField(
                CPUList.objects.all().filter(
                    hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel),
                empty_label=_(u'Select a CPU Number'),
                label='CPU Number',
                initial=CPUList.objects.all().filter(
                    hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel,
                    cpuNumber=WorkingProject.objects.all()[0].project.hardwareModel.defaultCPUNumber
                )[0].pk,
            )
        else:
            cpuNumber = forms.ModelChoiceField(
                CPUList.objects.all().filter(
                    hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel),
                empty_label=_(u'Select a CPU Number'),
                label='CPU Number',
                initial=CPUList.objects.none(),
            )

        memory = forms.ModelChoiceField(
            MemoryList.objects.all().filter(
                hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel),
            empty_label=_(u'Select a Memory'),
            label='Memory (G)',
            initial=MemoryList.objects.all().filter(
                hardwareModel=WorkingProject.objects.all()[0].project.hardwareModel,
                memory=WorkingProject.objects.all()[0].project.hardwareModel.defaultMemory
            )[0].pk,
        )

        clientNumber=forms.IntegerField(initial=WorkingProject.objects.all()[0].project.hardwareModel.defaultCPUNumber/2)
        cpuUsageTuning = forms.ModelChoiceField(
            CPUTuning.objects.all().filter(
                dbMode=WorkingProject.objects.all()[0].project.database_type,
                hardwareType=WorkingProject.objects.all()[0].project.hardwareType),
            empty_label=_(u'Select a CPU Usage Tuning Option'),
            label='CPU Usage Tuning',
            initial=CPUTuning.objects.all().filter(
                dbMode=WorkingProject.objects.all()[0].project.database_type,
                hardwareType=WorkingProject.objects.all()[0].project.hardwareType,
                tuningOption='Normal')[0].pk
        )

        memoryUsageTuning = forms.ModelChoiceField(
            MemoryUsageTuning.objects.all(),
            empty_label=_(u'Select a Memory Usage Tuning Option'),
            label='Memory Usage Tuning',
            initial=MemoryUsageTuning.objects.all().filter(name='Normal')[0].pk
        )
    else:
        cpuNumber = forms.ModelChoiceField(CPUList.objects.none())
        memory = forms.ModelChoiceField(MemoryList.objects.none())
        cpuUsageTuning = forms.ModelChoiceField(CPUTuning.objects.none())
        memoryUsageTuning = forms.ModelChoiceField(MemoryUsageTuning.objects.none())



    # cpuUsageTuning = models.ForeignKey(CPUTuning, on_delete=models.CASCADE, verbose_name='CPU Usage Tuning')
    # memoryUsageTuning = models.ForeignKey(MemoryUsageTuning, on_delete=models.CASCADE,
    #
    #                                       verbose_name='Memory Usage Tuning')

    class Meta:
        model = ProjectInformation
        fields = '__all__'


    def clean(self):
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



    # def is_valid(self):
    #     if WorkingProject.objects.count() == 0:
    #         self.add_error('project', 'Please set working project first!')
    #     return super(ProjectInformationForm, self).is_valid()

class TrafficInformationForm(forms.ModelForm):

    if WorkingProject.objects.count() > 0:
        callType = forms.ModelChoiceField(
            CallType.objects.all(),
            empty_label=_(u'Select a Call Type'),
            # help_text=_(u'Select a VM Type'),
            label='Call Type',
        )

        if ProjectInformation.objects.all().filter(project=WorkingProject.objects.all()[0].project).count() > 0:
            activeSubscriber = forms.IntegerField(
                localize = True,
                label='Active Subscribers',
                initial=ProjectInformation.objects.all().
                    filter(project=WorkingProject.objects.all()[0].project)[0].activeSubscriber
            )
            inactiveSubscriber = forms.IntegerField(
                localize = True,
                label='Inactive Subscribers',
                initial=ProjectInformation.objects.all().filter(
                    project=WorkingProject.objects.all()[0].project)[0].inactiveSubscriber,
            )
        else:
            activeSubscriber = forms.IntegerField(
                label='Active Subscribers',
                initial=0,
            )
            inactiveSubscriber = forms.IntegerField(
                label='Inactive Subscribers',
                initial=0,
            )



    else:
        callType = forms.ModelChoiceField(
            CallType.objects.none(),
        )
        activeSubscriber = forms.IntegerField(
            label='Active Subscribers',
            initial=0,
        )
        inactiveSubscriber = forms.IntegerField(
            label='Inactive Subscribers',
            initial=0,
        )

    callHoldingTime = forms.FloatField(
        label='Call Holding Time (s)',
        initial=0,
        widget=forms.NumberInput(attrs={'style': 'width:100px'}),
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
        label='Group Colocated with Member',
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
        CallType.objects.all(),
        label='Call Type',
        disabled=True,
        # widget={forms.Input}
    )
    averageBundleNumberPerSubscriber = forms.FloatField(
        label='Bundle Number',
        initial=0,
        widget=forms.NumberInput(attrs={'Style':'width:100px'}),
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
        # widget=forms.NumberInput(attrs={'style': 'width:100px'}),
    )

    class Meta:
        model = CallTypeCounterConfiguration
        fields = '__all__'


class DBConfigurationForm(forms.ModelForm):
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
    recordSize = forms.IntegerField(
        initial=0,
        label='Record Size',
        disabled=True,
    )
    placeholderRatio = forms.FloatField(
        initial=0,
        label='Placeholder Ratio (%)',
    )
    referencePlaceholderRatio = forms.FloatField(
        initial=0,
        label='Reference for Placeholder Ratio',
        disabled=True,
    )
    MEMBER_GROUP_OPTION = (('Member', 'Member'), ('Group', 'Group'))
    memberGroupOption = forms.ChoiceField(
        initial='Member',
        choices=MEMBER_GROUP_OPTION,
        label='DB Option'
    )
    subscriberNumber = forms.IntegerField(
        initial=0,
        label='Subscriber Number',
        disabled=True,
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
    backupAppNodeNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Backup App Node Per System',
    )
    spareAppNodeNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Spare App Node Per System',
    )
    backupDBNodeNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Backup DB Node Per System',
    )
    spareDBNodePairNumberPerSystem = forms.IntegerField(
        initial=0,
        label='Number of Spare DB Node Pair Per System'
    )

    class Meta:
        model = SystemConfiguration
        fields = '__all__'


class ApplicationConfigurationForm(forms.ModelForm):
    applicationName = forms.ModelChoiceField(
        ApplicationName.objects.all().filter(
            ~Q(name='EPAY'),
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
        label='Active Subscriber',
    )

    inactiveSubscriber = forms.IntegerField(
        initial=0,
        label='Inctive Subscriber',
    )

    trafficTPS = forms.FloatField(
        label='CPS/TPS',
        initial=0,
    )

    class Meta:
        model = ApplicationConfiguration
        fields = '__all__'

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

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if cleaned_data.get('email') == 'john@doe.com':
            raise forms.ValidationError('John, come on. You are blocked.')
