from sys import argv

if __name__ == '__main__':
    inputFile = open(argv[1], 'r')
    outFile = open(argv[1] + '.sql', 'w')

    dbSequence = 0
    rowID = 0
    line_number = 0

    if argv[2] == "dbinfo":
        outFile2 = open(argv[1] + '_db_name.sql', 'w')
        outFile.write('DELETE FROM [Service_dbinformation];\n\n')
        outFile2.write('DELETE FROM [Service_dbname];\n\n')

        for line in inputFile.readlines():
            line_number += 1

            if line_number > 2:
                dbSequence += 1
                line=line.strip('\n')
                a = line.split(',')
                if a[0] == 'SIM' or a[0] == 'AI' or a[0] == 'ACM':
                    is_include_inactive_subscriber = 1
                else:
                    is_include_inactive_subscriber = 0
                outFile2.write('INSERT INTO [Service_dbname]([rowid], [id], [name], [ndbRefPlaceholderRatio], [isPrefixTable], [prefixTableIndexNumber], [rtdbOverhead], [todoLogSize], [mateLogSize], [updateTimes], [defaultMemberFactor], [defaultGroupFactor], [defaultMemberCounterFactor], [defaultGroupCounterFactor], [isIncludeInactiveSubscriber])\n')
                outFile2.write('VALUES(%d, %d, \'%s\', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d);\n\n'%(dbSequence, dbSequence, a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], is_include_inactive_subscriber))
                for i in range(18, 35):
                    rowID += 1
                    if i >= 29:
                        release = 12 + (i - 29) / 2
                        mode_id = i % 2
                        if mode_id == 0:
                            mode_id = 2
                    else:
                        release = i -17
                        mode_id = 1
                    if a[i] != '':
                        outFile.write('INSERT INTO [Service_dbinformation]([rowid], [id], [recordSize], [db_id], [mode_id], [release_id])\n')
                        outFile.write('VALUES(%d, %d, %s, %d, %d, %d);\n\n'%(rowID, rowID, a[i], dbSequence, mode_id, release))

    if argv[2] == "featuredbimpact":
        for line in inputFile.readlines():
            dbSequence += 1

            line=line.strip('\n')
            a = line.split(',')

            if dbSequence == 1:
                a1 = a
            if dbSequence == 2:
                a2 = a
            if dbSequence > 3:
                for i in range(2, 20):
                    if int(a[i]) > 0:
                        rowID += 1
                        outFile.write('INSERT INTO [Service_featuredbimpact]([rowid], [id], [memberImpactFactor], [groupImpactFactor], [dbName_id], [featureName_id])\n')
                        if a1[i] == 'M':
                            outFile.write('VALUES(%d, %d, %s, %s, %d, %s);\n\n'%(rowID, rowID, a[i], '0', dbSequence - 3, a2[i]))
                        else:
                            outFile.write('VALUES(%d, %d, %s, %s, %d, %s);\n\n'%(rowID, rowID, '0', a[i], dbSequence - 3, a2[i]))

    if argv[2] == "featurecpuimpact":
        for line in inputFile.readlines():
            dbSequence += 1

            line=line.strip('\n')
            a = line.split(',')

            if dbSequence > 1:
                rowID += 1

                outFile.write('INSERT INTO [Service_featurecpuimpact]([rowid], [id], [ccImpactCPUTime], [ccImpactCPUPercentage], [ss7In], [ss7Out], [reImpactCPUTime], [reImpactCPUPercentage], [ldapMessageSize], [diameterMessageSize], [featureName_id])\n')
                outFile.write('VALUES(%d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %d);\n\n'%(rowID, rowID, a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], rowID))

    if argv[2] == "cpu":
        for line in inputFile.readlines():
            dbSequence += 1

            line=line.strip('\n')
            a = line.split(',')

            if dbSequence > 1:
                rowID += 1

                outFile.write('INSERT INTO [Hardware_cpu]([rowid], [id], [name], [coreNumber], [overallCapacity], [singleThreadCapacity], [htCapacityRatio], [vmCapacityRatio], [defaultClientNumber], [hyperthreadEnabled], [virtualization], [maxDiameterPerIONode], [maxLDAPPerIONode], [maxSIGTRANPerIONode])\n')
                outFile.write('VALUES(%d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %d);\n\n'%(rowID, rowID, a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], rowID))

    if argv[2] == "callcost":
        for line in inputFile.readlines():
            dbSequence += 1

            line=line.strip('\n')
            a = line.split(',')

            if dbSequence > 1:
                for i in range(1, 13):
                    rowID += 1
                    outFile.write('INSERT INTO [Service_callcost]([rowid], [id], [callCost], [callType_id], [release_id], [hardwareModel_id], [dbMode_id])\n')
                    outFile.write('VALUES(%d, %d, %s, %d, %d, %d, %d);\n\n'%(rowID, rowID, a[i], dbSequence - 1, i, 1, 1))

    if argv[2] == "featurecalltype":
        outFile.write('DELETE FROM [service_featurecalltypeconfiguration];\n\n');

        call_type_id = 0
        for line in inputFile.readlines():
            call_type_id += 1

            line=line.strip('\n')
            a = line.split(',')

            featureName_id = 0
            for i in range(0, 18):
                rowID += 1
                featureName_id += 1
                outFile.write('INSERT INTO [service_featurecalltypeconfiguration]([rowid], [id], [callType_id], [featureName_id], [featureApplicable])\n')
                outFile.write('VALUES(%d, %d, %d, %d, %s);\n\n'%(rowID, rowID, call_type_id, featureName_id, a[i]))
