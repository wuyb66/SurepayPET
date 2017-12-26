from django.contrib import admin

from .models import GlobalConfiguration, DBMode, NetworkInfo

class GlobalConfigurationAdmin(admin.ModelAdmin):
    list_display = ('maintananceWindowHour', 'trafficPercentageUnderMaitananceWindow', 'releaseCPUImpact',
                    'releaseAppMemoryImpact', 'releaseDBMemoryImpact', 'releaseCountCPUImpact',
                    'reservedCPURatio')

class NetworkInfoAdmin(admin.ModelAdmin):
    list_display = ('defaultSIGTRANLinkSpeed', 'defaultSIGTRANLinkNumber', 'maxSIGTRANPortUtil')

admin.site.register(GlobalConfiguration, GlobalConfigurationAdmin)
admin.site.register(DBMode)
admin.site.register(NetworkInfo, NetworkInfoAdmin)

