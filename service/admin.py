from django.contrib import admin
from django.forms import ModelForm, TextInput, NumberInput
from suit.widgets import EnclosedInput, HTML5Input
from .models import Release, ApplicationName, ApplicationInformation, DBName, DBInformation, FeatureName, \
    FeatureCPUImpact, FeatureDBImpact, CallCost, CallType, CounterCost, CounterCostName, OtherApplicationInformation, \
    CurrentRelease, FeatureCallTypeConfiguration


class ReleaseForm(ModelForm):
    class Meta:
        widgets = {
            'name': TextInput(attrs={'class': 'input-mini'}),
            'sequence': NumberInput(attrs={'class': 'input-mini'}),
            #'sequence': HTML5Input(input_type='color'),
            'callRecordSize': EnclosedInput(append='byte'),
            'ldapCIPSize': EnclosedInput(append='byte'),
            'sessionCIPSize': EnclosedInput(append='byte'),
            'otherCIPSize': EnclosedInput(append='byte'),
            'cpuCostForNormalAMA': EnclosedInput(append='ms'),
            'cPUCostForMultipleAMA': EnclosedInput(append='ms'),
            'amaSizePerBlock': EnclosedInput(append='byte'),

        }


class ReleaseAdmin(admin.ModelAdmin):
    form = ReleaseForm
    list_display = ('name', 'sequence', 'callRecordSize', 'ldapCIPSize', 'sessionCIPSize', 'otherCIPSize',
                    'cpuCostForNormalAMA', 'cPUCostForMultipleAMA', 'amaSizePerBlock', 'amaNumberPerGroupCall',
                    'counterNumberPerRecord')


class CurrentReleaseAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ApplicationInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'callRecordSize', 'textSize', 'initialDataSize', 'ldapCIPSize',
                    'sessionCIPSize', 'otherCIPSize', 'callCost', 'cpuCostForServer')
    list_filter = ('release', 'application')
    search_fields = ('release__name', 'application__name')


class OtherApplicationInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'maxTrafficPerNode', 'clientNumber', 'minClient', 'maxNodePerSystem')
    list_filter = ('application', 'hardwareModel')
    search_fields = ('application__name', 'hardwareModel__hardwareType__name',
                     'hardwareModel__cpu__name')


class DBInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'recordSize',)
    list_filter = ('db', 'mode', 'release')
    search_fields = ('db__name', 'mode__name', 'release__name')


class FeatureNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'impactDB', 'comment')


class FeatureDBImpactAdmin(admin.ModelAdmin):
    list_display = ('name', 'memberImpactFactor', 'groupImpactFactor')
    list_filter = ('dbName', 'featureName')
    search_fields = ('dbName__name', 'featureName__name')


class FeatureCPUImpactAdmin(admin.ModelAdmin):
    list_display = ('name', 'ccImpactCPUTime', 'ccImpactCPUPercentage', 'ss7In', 'ss7Out',
                    'reImpactCPUTime', 'reImpactCPUPercentage', 'ldapMessageSize', 'diameterMessageSize')


class CallTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'ss7InSize', 'ss7OutSize', 'ss7Number', 'tcpipSize', 'tcpipNumber', 'diameterSize',
                    'diameterNumber', 'mateUpdateNumber', 'ndbCPUUsageLimitation')


class CallCostAdmin(admin.ModelAdmin):
    list_display = ('name', 'callCost')
    list_filter = ('callType', 'release', 'hardwareModel', 'dbMode')
    search_fields = ('callType__name', 'release__name', 'hardwareModel__hardwareType__name',
                     'hardwareModel__cpu__name', 'dbMode__name')


class CounterCostAdmin(admin.ModelAdmin):
    list_display = ('name', 'counterNumberPerRecord', 'costDBReadUpdatePerRecord', 'costPerAppliedBucket',
                    'costPerAppliedUBD', 'costPerUnappliedBucket', 'costPerUnappliedUBD',
                    'costPerUnappliedCounterWithBasicCriteria', 'costTurnOnbucket', 'costTurnOnUBD',
                    'costTurnOnUnappliedCounter', 'costCounterNumberImpact', 'percentageCounterNumberImpact',
                    'costGroupDBReadUpdatePerRecord', 'costTurnOnGroupBucket', 'costPerGroupSideBucket',
                    'costBundlePerRecord', 'costPer24hBundle',
                    )
    list_filter = ('release', 'hardwareModel')
    search_fields = ('release__name', 'hardwareModel__hardwareType__name',
                     'hardwareModel__cpu__name')


admin.site.register(Release, ReleaseAdmin)
admin.site.register(CurrentRelease, CurrentReleaseAdmin)
admin.site.register(ApplicationName)
admin.site.register(ApplicationInformation, ApplicationInformationAdmin)
admin.site.register(OtherApplicationInformation, OtherApplicationInformationAdmin)
admin.site.register(DBName)
admin.site.register(DBInformation, DBInformationAdmin)
admin.site.register(FeatureName, FeatureNameAdmin)
admin.site.register(FeatureCPUImpact, FeatureCPUImpactAdmin)
admin.site.register(FeatureDBImpact, FeatureDBImpactAdmin)
admin.site.register(CallCost, CallCostAdmin)
admin.site.register(CallType, CallTypeAdmin)
admin.site.register(CounterCost, CounterCostAdmin)
admin.site.register(CounterCostName)
admin.site.register(FeatureCallTypeConfiguration)
