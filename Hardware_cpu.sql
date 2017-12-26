DROP TABLE IF EXISTS [Hardware_cpu];
CREATE TABLE [Hardware_cpu]([rowid] integer, [id] integer, [name] varchar(16), [coreNumber] integer, [overallCapacity] real, [singleThreadCapacity] real, [htCapacityRatio] real, [vmCapacityRatio] real, [defaultClientNumber] integer, [hyperthreadEnabled] bool, [virtualization] bool, [maxDiameterPerIONode] integer, [maxLDAPPerIONode] integer, [maxSIGTRANPerIONode] integer);

INSERT INTO [Hardware_cpu]([rowid], [id], [name], [coreNumber], [overallCapacity], [singleThreadCapacity], [htCapacityRatio], [vmCapacityRatio], [defaultClientNumber], [hyperthreadEnabled], [virtualization], [maxDiameterPerIONode], [maxLDAPPerIONode], [maxSIGTRANPerIONode])
VALUES(1, 1, 'VM-HP-G8', 16, 1.8, 1.35, 1, 1, 12, 1, 1, 120000, 160000, 40000);

INSERT INTO [Hardware_cpu]([rowid], [id], [name], [coreNumber], [overallCapacity], [singleThreadCapacity], [htCapacityRatio], [vmCapacityRatio], [defaultClientNumber], [hyperthreadEnabled], [virtualization], [maxDiameterPerIONode], [maxLDAPPerIONode], [maxSIGTRANPerIONode])
VALUES(2, 2, 'VM-HP-G9', 24, 2.82, 1.41, 1, 1, 20, 1, 1, 120000, 160000, 40000);

INSERT INTO [Hardware_cpu]([rowid], [id], [name], [coreNumber], [overallCapacity], [singleThreadCapacity], [htCapacityRatio], [vmCapacityRatio], [defaultClientNumber], [hyperthreadEnabled], [virtualization], [maxDiameterPerIONode], [maxLDAPPerIONode], [maxSIGTRANPerIONode])
VALUES(3, 3, 'Bono', 12, 1, 1, 1, 1, 12, 1, 0, 120000, 160000, 40000);

INSERT INTO [Hardware_cpu]([rowid], [id], [name], [coreNumber], [overallCapacity], [singleThreadCapacity], [htCapacityRatio], [vmCapacityRatio], [defaultClientNumber], [hyperthreadEnabled], [virtualization], [maxDiameterPerIONode], [maxLDAPPerIONode], [maxSIGTRANPerIONode])
VALUES(4, 4, 'HP-G9', 24, 2.82, 1.41, 1, 1, 24, 1, 0, 120000, 160000, 40000);

INSERT INTO [Hardware_cpu]([rowid], [id], [name], [coreNumber], [overallCapacity], [singleThreadCapacity], [htCapacityRatio], [vmCapacityRatio], [defaultClientNumber], [hyperthreadEnabled], [virtualization], [maxDiameterPerIONode], [maxLDAPPerIONode], [maxSIGTRANPerIONode])
VALUES(5, 5, 'HP-G8', 16, 1.8, 1.35, 1, 1, 16, 1, 0, 120000, 160000, 40000);

