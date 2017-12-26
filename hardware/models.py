'''
    The file is used to define the tables related to hardware.
'''
from django.db import models
from common.models import DBMode

'''
    Define virtualization type.
'''
class VMType(models.Model):
    VM_TYPE_OPTION = (('Native', 'Native'), ('Openstack', 'Openstack'), ('VMWare', 'VMWare'), ('CBIS', 'CBIS'))
    type = models.CharField(max_length=16,choices=VM_TYPE_OPTION)

    capacity = models.FloatField(default=1)

    def __str__(self):
        return self.type

'''
    Define CPU information.
    
    Use ATCA Bono as the base CPU and the singleThreadCapacity means the relative capacity to single thread capacity of Bono.
    
    The overall capacity is the total capacity of one node (blade, VM) = singleThreadCapacity * client number. For example:
        The client number for one Bono blade is 12, the overall capacity: 1 * 12 = 12
        
    Add new CPU when hyperthread is OFF.
'''
class CPU(models.Model):
    name = models.CharField(max_length=16)
    virtualizationSupported = models.BooleanField(default=True)
    ndbSupported = models.BooleanField(default=True)
    coreNumber = models.IntegerField()
    overallCapacity = models.FloatField()
    singleThreadCapacity = models.FloatField()

    def __str__(self):
        return self.name


# class CPUClientList(models.Model):
#     cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
#     clientNumber = models.IntegerField()
#     capacityRatio = models.FloatField()
#
#     mateCapacityNDB = models.IntegerField()
#     dbCapacityNDB = models.IntegerField()
#
#     def __str__(self):
#         return self.cpu.name
#
#     def getOverallCapacity(self):
#         return self.capacityRatio * self.cpu.singleThreadCapacity * self.clientNumber



class HardwareType(models.Model):
    name = models.CharField(max_length=24)
    isVM = models.BooleanField(default=False)

    # cpus = models.ManyToManyField('CPU')

    def __str__(self):
        return self.name



class HardwareModel(models.Model):
    hardwareType = models.ForeignKey(HardwareType, on_delete=models.CASCADE)
    name = models.CharField(max_length=24)  # HardwareType + CPU
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)

    maxNodeNumber = models.IntegerField()
    maxSubscriberSupport = models.IntegerField()
    vmCapacityRatio = models.FloatField(default=0.8)
    reservedCoreNumberForVM = models.IntegerField(default=0)

    defaultCPUNumber = models.IntegerField()
    defaultClientNumber = models.IntegerField()
    defaultMemory = models.IntegerField()
    maxSIGTRANPerIONode = models.IntegerField()
    maxLDAPPerIONode = models.IntegerField()
    maxDiameterPerIONode = models.IntegerField()

    def __str__(self):
        return self.name


'''
    Define the client (Native) or vCPU (VM) list.
'''
class CPUList(models.Model):
    hardwareModel = models.ForeignKey(HardwareModel, on_delete=models.CASCADE)
    cpuNumber = models.IntegerField()   # For VM

    clientNumber = models.IntegerField()    # For native
    capacityRatio = models.FloatField()

    mateCapacityNDB = models.IntegerField()
    dbCapacityNDB = models.IntegerField()

    def getOverallCapacity(self):
        return self.capacityRatio * self.hardwareModel.cpu.singleThreadCapacity * self.clientNumber

    def __str__(self):
        return str(self.cpuNumber)

    @property
    def name(self):
        if self.cpuNumber > 0:
            return self.hardwareModel.name + '_' + str(self.cpuNumber)
        else:
            return self.hardwareModel.name + '_' + str(self.clientNumber)


class MemoryList(models.Model):
    hardwareModel = models.ForeignKey(HardwareModel, on_delete=models.CASCADE)
    memory = models.IntegerField()

    def __str__(self):
        return str(self.memory)

    @property
    def name(self):
        return self.hardwareModel.name + '_' + str(self.memory) + 'G'


class CPUTuning(models.Model):
    CPU_USAGE_OPTION = (('Simple', 'Simple'), ('Normal', 'Normal'), ('Aggressive', 'Aggressive'))

    dbMode = models.ForeignKey(DBMode, on_delete=models.CASCADE)
    hardwareType = models.ForeignKey(HardwareType, on_delete=models.CASCADE)
    tuningOption = models.CharField(max_length=16, choices=CPU_USAGE_OPTION, default='Normal')
    systemCPUUsage = models.FloatField()
    clientCPUUsage = models.FloatField()

    def __str__(self):
        return self.tuningOption

    @property
    def name(self):
        return self.dbMode.name + '_' + self.hardwareType.name + '_' + self.tuningOption


class MemoryUsageTuning(models.Model):
    MEMORY_USAGE_OPTION = (('Simple', 'Simple'), ('Normal', 'Normal'), ('Aggressive', 'Aggressive'))

    name = models.CharField(max_length=16, choices=MEMORY_USAGE_OPTION, default='Normal')
    memoryUsageTuning = models.FloatField()

    def __str__(self):
        return self.name





