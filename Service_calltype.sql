DROP TABLE IF EXISTS [Service_calltype];
CREATE TABLE [Service_calltype]([rowid] integer, [id] integer, [name] varchar(64), [ss7InSize] integer, [ss7OutSize] integer, [ss7Number] integer, [tcpipSize] integer, [tcpipNumber] integer, [ndbCPUUsageLimitation] real, [diameterNumber] integer, [diameterSize] integer, [mateUpdateNumber] integer);

INSERT INTO [Service_calltype]([rowid], [id], [name], [ss7InSize], [ss7OutSize], [ss7Number], [tcpipSize], [tcpipNumber], [ndbCPUUsageLimitation], [diameterNumber], [diameterSize], [mateUpdateNumber])
VALUES(1, 1, 'CS1 Voice Call', 750, 750, 3, 1024, 3, 0.6, 0, 0, 0);

