from django.contrib import admin

from .models import CPU, CPUList, MemoryList, HardwareModel, HardwareType, VMType, CPUTuning, MemoryUsageTuning

class VMTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'capacity')

class CPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'virtualizationSupported', 'ndbSupported', 'coreNumber', 'overallCapacity', 'singleThreadCapacity')
    list_filter = ('virtualizationSupported', 'ndbSupported', 'coreNumber')


class HardwareModelInline(admin.TabularInline):
    model = HardwareModel
    fk_name = 'hardwareType'
    fields = ('hardwareType', 'cpu')

class HardwareTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'isVM')
    inlines = [HardwareModelInline, ]


class HardwareModelAdmin(admin.ModelAdmin):
    list_display = ('hardwareType', 'name', 'cpu', 'maxNodeNumber', 'maxSubscriberSupport', 'vmCapacityRatio', 'reservedCoreNumberForVM',
                    'defaultClientNumber', 'maxSIGTRANPerIONode', 'maxLDAPPerIONode', 'maxDiameterPerIONode')
    list_filter = ('hardwareType', 'cpu', 'defaultClientNumber', )
    search_fields =('hardwareType__name', 'cpu__name')

class CPUListAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpuNumber', 'clientNumber', 'capacityRatio', 'mateCapacityNDB', 'dbCapacityNDB')

class MemoryListAdmin(admin.ModelAdmin):
    list_display = ('name', 'memory')

class CPUTuningAdmin(admin.ModelAdmin):
    list_display = ('name', 'systemCPUUsage', 'clientCPUUsage')
    list_display_links = ('name', 'systemCPUUsage')

class MemoryUsageTuningAdmin(admin.ModelAdmin):
    list_display = ('name', 'memoryUsageTuning')

admin.site.register(CPU, CPUAdmin)
admin.site.register(CPUList, CPUListAdmin)
admin.site.register(MemoryList, MemoryListAdmin)
admin.site.register(HardwareType, HardwareTypeAdmin)
admin.site.register(HardwareModel, HardwareModelAdmin)
admin.site.register(VMType, VMTypeAdmin)
admin.site.register(CPUTuning, CPUTuningAdmin)
admin.site.register(MemoryUsageTuning, MemoryUsageTuningAdmin)


