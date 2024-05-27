SELECT * FROM Counts WHERE StoreId = (SELECT Id FROM Stores WHERE Name = 'City Market') AND DATE(UpdatingDateTime) ='2024-05-09';
