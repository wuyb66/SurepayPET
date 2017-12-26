DROP TABLE IF EXISTS [Service_featurename];
CREATE TABLE [Service_featurename]([rowid] integer, [id] integer, [name] varchar(64), [impactDB] varchar(64), [comment] varchar(255));

INSERT INTO [Service_featurename]([rowid], [id], [name], [impactDB], [comment])
VALUES(1, 1, 'Service History', 'SH RTDB, 100% means 5 records per subscriber. ', 'Save call information into SH RTDB');

