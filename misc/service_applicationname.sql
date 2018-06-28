DROP TABLE IF EXISTS [service_applicationname];
CREATE TABLE [service_applicationname]([rowid] integer, [id] integer, [name] varchar(20), [needConfigDB] bool);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(1, 1, 'EPAY', 1);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(3, 3, 'DRouter', 1);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(4, 4, 'CDRPP', 0);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(5, 5, 'eCGS', 0);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(6, 6, 'EPPSM', 1);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(7, 7, 'eCTRL', 1);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(8, 8, 'GRouter', 0);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(9, 9, 'Group', 0);

INSERT INTO [service_applicationname]([rowid], [id], [name], [needConfigDB])
VALUES(10, 10, 'NTGW', 0);

