import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="person-count-database"
)
cursor = conn.cursor()


TodayDate = datetime.now().date()
StoreName = "City Market"
ManCount = 1
WomanCount = 2
KidCount = 3
StaffCount = 4
EmployeeCount = 5
TotalCount = ManCount + WomanCount + KidCount + StaffCount + EmployeeCount


sql_check = "SELECT * FROM Counts WHERE StoreId = (SELECT Id FROM Stores WHERE Name = %s) AND DATE(UpdatingDateTime) = %s;"
val_check = (StoreName, TodayDate)
cursor.execute(sql_check, val_check)
existing_record = cursor.fetchone()

if existing_record:
    sql_update = "UPDATE Counts SET ManCount = %s, WomanCount = %s, KidCount = %s, StaffCount = %s, EmployeeCount = %s, TotalCount = %s WHERE StoreId = (SELECT Id FROM Stores WHERE Name = %s) AND DATE(UpdatingDateTime) = %s;"
    val_update = (ManCount, WomanCount, KidCount, StaffCount, EmployeeCount, TotalCount, StoreName, TodayDate)
    cursor.execute(sql_update, val_update)
else:
    sql_insert = "INSERT INTO Counts (StoreId, ManCount, WomanCount, KidCount, StaffCount, EmployeeCount, TotalCount) VALUES ((SELECT Id FROM Stores WHERE Name = %s), %s, %s, %s, %s, %s, %s);"
    val_insert = (StoreName, ManCount, WomanCount, KidCount, StaffCount, EmployeeCount, TotalCount)
    cursor.execute(sql_insert, val_insert)


conn.commit()
conn.close()
