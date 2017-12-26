DELETE FROM [Service_release];

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(1, 1, 'SP29.11', 1, 300000, 6500, 5200, 6300);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(2, 2, 'SP29.12', 2, 315000, 7200, 5800, 7000);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(3, 3, 'SP29.13', 3, 360000, 7600, 6100, 7300);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(4, 4, 'SP29.14', 4, 430000, 9000, 8000, 8600);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(5, 5, 'SP29.15', 5, 441000, 9500, 8500, 9000);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(6, 6, 'SP29.16', 6, 460000,10500, 9500,10000);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(7, 7, 'SP29.17', 7, 510000,11000,10000,10500);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(8, 8, 'SP29.18', 8, 540000,11500,10500,11000);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(9, 9, 'SP29.19', 9, 570000,12100,11000,12100);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(10, 10, 'SP31.1', 10, 570000, 9300, 8700,17000);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(11, 11, 'SP31.2', 11, 600000, 9600, 9000,17500);

INSERT INTO [Service_release]([rowid], [id], [name], [sequence], [callRecordSize], [ldapCIPSize], [sessionCIPSize], [otherCIPSize])
VALUES(12, 12, 'SP17.3', 12, 600000,10000, 9500,18500);

DELETE FROM [Service_featurename];

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(1, 1, 'Service History', 'SH RTDB, 100% means 5 records per subscriber. Factor: 5', 'Save call information into SH RTDB');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(2, 2, 'Friend & Family', 'SSD or SFF RTDB, Factor: 1. Determined by the flag SIMSD RTDB for FF Special Number in feature configuration table. ', 'Need SSD or SFF RTDB');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(3, 3, 'SplitCharging For IC call (VFI)', 'N/A', 'Currently for VFI only');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(4, 4, 'M2M Number Translations', 'N/A', 'N/A');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(5, 5, 'CS1 Calls with ACR', 'N/A', 'N/A');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(6, 6, 'Announcement', 'N/A', 'N/A');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(7, 7, 'Call with SMS notification', 'N/A', 'N/A');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(8, 8, 'Dual Tarrif/Usage Split', 'N/A', 'N/A');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(9, 9, 'Number Portability Query', 'N/A', 'MAP SRI Message will be sent out');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(10, 10, 'Self learning', 'GPRSSIM factor: 1, ID2MDN factor: 1', 'Index server');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(11, 11, 'Session Failover (Member Side)', 'Session factor: 1, SIMIDX factor: 1. The factor depends on the average category number per session. The factor should be 2 if category number > 1.', 'Session Failover for member side');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(12, 12, 'Online Hierarchy', 'AI factor: 1, GPRSSIM factor: 1', 'Online Hierarchy');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(13, 13, 'HPUAS', 'N/A', 'High performance usage allowance sharing');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(14, 14, 'EU Roaming', 'N/A', ' EU roaming (77439)');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(15, 15, 'Session Failover (Group Side)', 'Session factor: 1, SIMIDX factor: 1.', 'Session Failover for group side');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(16, 16, 'Uncorrelated CCR-U/T Handling', 'N/A', 'Uncorrelated CCR-U/T Handling and Keep Session Active (74936)');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(17, 17, 'Multiple Apply Charging', 'N/A', 'Multiple Apply Charging Report (73690)');

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(18, 18, 'Versioning Table', 'N/A', 'Full Table Versioning via Tariff Admin Tool (75083)');

DELETE FROM [Service_dbname];

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(1, 1, 'SIM');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(2, 2, 'ACM');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(3, 3, 'SH');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(4, 4, 'SFF');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(5, 5, 'SSD');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(6, 6, 'UA');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(7, 7, 'ROAMER');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(8, 8, 'SGLRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(9, 9, 'MNPRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(10, 10, 'RE');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(11, 11, 'CTRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(12, 12, 'TID');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(13, 13, 'TOKENRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(14, 14, 'AI');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(15, 15, 'DP');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(16, 16, 'DV');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(17, 17, 'EZSMDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(18, 18, 'EZSZDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(19, 19, 'EZZNDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(20, 20, 'DSC');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(21, 21, 'HM');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(22, 22, 'SSR');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(23, 23, 'VSIMDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(24, 24, 'CDZADB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(25, 25, 'VTXDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(26, 26, 'SSIDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(27, 27, 'PHSSCR');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(28, 28, 'PDSIM');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(29, 29, 'PDCIR');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(30, 30, 'PDSSTL');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(31, 31, 'PROMDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(32, 32, 'PSCDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(33, 33, 'RCNRDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(34, 34, 'SCRRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(35, 35, 'SUCRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(36, 36, 'GPRSSIM');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(37, 37, 'SSTL');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(38, 38, 'CIR');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(39, 39, 'SMSRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(40, 40, 'XBRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(41, 41, 'SIMIDX');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(42, 42, 'Session');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(43, 43, 'SIME');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(44, 44, 'GNMDNDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(45, 45, 'GNRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(46, 46, 'GTMDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(47, 47, 'FSNRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(48, 48, 'CLIINFO');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(49, 49, 'CUIRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(50, 50, 'ID2MDN');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(51, 51, 'HOC');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(52, 52, 'GCUPL');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(53, 53, 'HTID');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(54, 54, 'MDNCLI');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(55, 55, 'GCIPL');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(56, 56, 'HTRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(57, 57, 'HTSIDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(58, 58, 'NGTMDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(59, 59, 'SYDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(60, 60, 'UIRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(61, 61, 'CDBRTDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(62, 62, 'NGCUPL');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(63, 63, 'PMOUDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(64, 64, 'GCURDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(65, 65, 'AECIDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(66, 66, 'EMSLDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(67, 67, 'PMSL');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(68, 68, 'ODCDB');

INSERT INTO [Service_dbname]([rowid], [id], [name])
VALUES(69, 69, 'SCAPDB');

DELETE FROM [Service_calltype];
INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(1,1,'CS1 Voice Call',750,750,3,1024,3,0.6,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(2,2,'CS1 Voice Call (Postpaid)',750,750,3,1024,3,0.6,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(3,3,'CS1 Voice unanswered call',750,750,3,1024,3,0.6,0,0,2);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(4,4,'CS1 Voice unanswered call (Postpaid)',750,750,3,1024,3,0.6,0,0,2);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(5,5,'CS1/CAP real time SMS',500,500,2,1024,2,0.4,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(6,6,'Originated USSD',500,500,2,1024,2,0.4,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(7,7,'CAP2 Voice call',1000,870,4,1024,4,0.6,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(8,8,'CAP2 Voice call (Postpaid)',1000,870,4,1024,4,0.6,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(9,9,'CAP2 Voice unanswered call',1000,740,4,1024,4,0.6,0,0,2);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(10,10,'CAP2 Voice unanswered call (Postpaid)',1000,740,4,1024,4,0.6,0,0,2);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(11,11,'IS826 Voice call',1060,720,4,1024,4,0.6,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(12,12,'IS826 Voice call (Postpaid)',1060,720,4,1024,4,0.6,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(13,13,'IS826 Voice unanswered call',915,720,4,1024,4,0.6,0,0,2);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(14,14,'IS826 Voice unanswered call (Postpaid)',915,720,4,1024,4,0.6,0,0,2);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(15,15,'Diameter Event Based Charging (ECUR)',0,0,0,0,1,0.4,1,1500,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(16,16,'Diameter Event Based Charging',0,0,0,0,1,0.4,1,1500,4);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(17,17,'PCRF Query',0,0,0,0,1,0.4,1,1500,4);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(18,18,'LDAP transaction (eCommerce Recharge)',0,0,0,400,1,0.3,0,1500,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(19,19,'Sy Session Contribution',0,0,0,400,1,0.4,1,1500,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(20,20,'ECOMMERCE Contribution',0,0,0,400,1,0.3,0,0,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(21,21,'GPRS/Diameter Session Contribution',0,0,0,0,1,0.6,1,1500,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(22,22,'Package Data Contribution',0,0,0,400,1,0.6,1,1500,3);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(23,23,'Group side transaction for OH',0,0,0,1024,1,0.3,0,0,3);

