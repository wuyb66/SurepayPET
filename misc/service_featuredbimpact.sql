DROP TABLE IF EXISTS [service_featuredbimpact];
CREATE TABLE [service_featuredbimpact]([_rowid_] INTEGER, [rowid] integer, [id] integer, [groupImpactFactor] real, [dbName_id] integer, [featureName_id] integer, [memberImpactFactor] real);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(1, 1, 1, 0, 3, 1, 5);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(2, 2, 2, 0, 5, 2, 1);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(3, 3, 3, 0, 8, 12, 1);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(4, 4, 4, 0, 36, 10, 1);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(5, 5, 5, 0, 41, 11, 1);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(6, 6, 6, 1, 41, 15, 0);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(7, 7, 7, 0, 42, 11, 1);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(8, 8, 8, 1, 42, 15, 0);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(9, 9, 9, 0, 50, 10, 1);

INSERT INTO [service_featuredbimpact]([_rowid_], [rowid], [id], [groupImpactFactor], [dbName_id], [featureName_id], [memberImpactFactor])
VALUES(10, 10, 10, 0, 61, 12, 1);

