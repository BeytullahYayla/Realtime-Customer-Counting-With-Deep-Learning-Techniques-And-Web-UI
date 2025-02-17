import mysql.connector
from datetime import datetime

class CustomerCountingDatabase:
    def __init__(self, host: str, user: str, password: str, db_name: str, port: int) -> None:
        self.conn = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=db_name,
            port=port
        )
        self.cursor = self.conn.cursor()
        print("----Connected To Database----")

    def __list_all_count_informations(self, store_name: str):
        query = "SELECT * FROM Counts WHERE StoreId = (SELECT Id FROM Stores WHERE Name = %s)"
        self.cursor.execute(query, (store_name,))
        record = self.cursor.fetchall()
        return record
    
    def __list_all_store_informations(self, store_name: str):
        query = "SELECT * FROM Stores WHERE Name = %s"
        self.cursor.execute(query, (store_name,))
        record = self.cursor.fetchall()
        return record

    def __list_count_informations(self, store_name: str, date: str):
        query = "SELECT * FROM Counts WHERE StoreId = (SELECT Id FROM Stores WHERE Name = %s) AND DATE(UpdatingDateTime) = %s;"
        self.cursor.execute(query, (store_name, date))
        record = self.cursor.fetchone()
        return record

    def __add_count_information(self, store_name: str, man_count: int, woman_count: int, kid_count: int, staff_count: int, employee_count: int, total_count: int):
        query = "INSERT INTO Counts (StoreId, ManCount, WomanCount, KidCount, StaffCount, EmployeeCount, TotalCount, CreatingDateTime, UpdatingDateTime) VALUES ((SELECT Id FROM Stores WHERE Name = %s), %s, %s, %s, %s, %s, %s, %s, %s)"
        now = datetime.now()
        self.cursor.execute(query, (store_name, man_count, woman_count, kid_count, staff_count, employee_count, total_count, now, now))
        self.conn.commit()
        print("Record inserted successfully.")
        
    def __add_store_information(self, name: str):
        query = "INSERT INTO Stores (Name) VALUES (%s)"
        self.cursor.execute(query, (name,))
        self.conn.commit()
        print("Store inserted successfully.")
        
    def __update_count_information(self, store_name: str, man_count: int, woman_count: int, kid_count: int, staff_count: int, employee_count: int, total_count: int):
        sql_update = "UPDATE Counts SET ManCount = %s, WomanCount = %s, KidCount = %s, StaffCount = %s, EmployeeCount = %s, TotalCount = %s, UpdatingDateTime = %s WHERE StoreId = (SELECT Id FROM Stores WHERE Name = %s) AND DATE(UpdatingDateTime) = %s;"
        val_update = (man_count, woman_count, kid_count, staff_count, employee_count, total_count, datetime.now(), store_name, str(datetime.now().date()))
        self.cursor.execute(sql_update, val_update)
        self.conn.commit()
        print("Record updated successfully.")
        
    def update_count_info(self, store_name: str, man_count: int, woman_count: int, kid_count: int, staff_count: int, employee_count: int, total_count: int):
        today_str = str(datetime.now().date())
        record = self.__list_count_informations(store_name, today_str)
        if record:
            self.__update_count_information(store_name, man_count, woman_count, kid_count, staff_count, employee_count, total_count)
        else:
            self.__add_count_information(store_name, man_count, woman_count, kid_count, staff_count, employee_count, total_count)
            
    def update_store_info(self, store_name: str):
        record = self.__list_all_store_informations(store_name)
        if record:
            print(f"There is already a store with the same name: {store_name}!")
        else:
            self.__add_store_information(store_name)

    def close(self):
        self.cursor.close()
        self.conn.close()
