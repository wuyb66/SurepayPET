DROP TABLE IF EXISTS [project_dbconfiguration];
CREATE TABLE [project_dbconfiguration]([_rowid_] INTEGER, [rowid] integer, [id] integer, [dbFactor] real, [placeholderRatio] real, [memberGroupOption] varchar(10), [recordSize] integer, [subscriberNumber] integer, [recordNumber] integer, [cacheSize] integer, [todoLogSize] integer, [mateLogSize] integer, [referencePlaceholderRatio] integer, [referenceDBFactor] integer, [dbInfo_id] integer, [project_id] integer, [application_id] integer);

INSERT INTO [project_dbconfiguration]([_rowid_], [rowid], [id], [dbFactor], [placeholderRatio], [memberGroupOption], [recordSize], [subscriberNumber], [recordNumber], [cacheSize], [todoLogSize], [mateLogSize], [referencePlaceholderRatio], [referenceDBFactor], [dbInfo_id], [project_id], [application_id])
VALUES(1, 2, 2, 1, 0, 'Member', 14677, 10000000, 10000000, 144581, 0, 0, 0, 1, 13, 3, 1);

INSERT INTO [project_dbconfiguration]([_rowid_], [rowid], [id], [dbFactor], [placeholderRatio], [memberGroupOption], [recordSize], [subscriberNumber], [recordNumber], [cacheSize], [todoLogSize], [mateLogSize], [referencePlaceholderRatio], [referenceDBFactor], [dbInfo_id], [project_id], [application_id])
VALUES(2, 3, 3, 1, 0, 'Group', 864, 1000000, 1000000, 969, 0, 0, 0, 1, 166, 3, 1);

INSERT INTO [project_dbconfiguration]([_rowid_], [rowid], [id], [dbFactor], [placeholderRatio], [memberGroupOption], [recordSize], [subscriberNumber], [recordNumber], [cacheSize], [todoLogSize], [mateLogSize], [referencePlaceholderRatio], [referenceDBFactor], [dbInfo_id], [project_id], [application_id])
VALUES(3, 4, 4, 2, 0, 'Member', 653, 11000000, 22000000, 16780, 0, 0, 0, 0, 132, 3, 1);

INSERT INTO [project_dbconfiguration]([_rowid_], [rowid], [id], [dbFactor], [placeholderRatio], [memberGroupOption], [recordSize], [subscriberNumber], [recordNumber], [cacheSize], [todoLogSize], [mateLogSize], [referencePlaceholderRatio], [referenceDBFactor], [dbInfo_id], [project_id], [application_id])
VALUES(4, 5, 5, 1, 0, 'Member', 188, 12100000, 12100000, 3735, 0, 0, 0, 1, 438, 3, 3);

