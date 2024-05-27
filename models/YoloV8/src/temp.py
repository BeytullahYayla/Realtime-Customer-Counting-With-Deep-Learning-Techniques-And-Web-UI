from database import CustomerCountingDatabase


db = CustomerCountingDatabase(
    host="localhost",      # Docker konteyneri localhost üzerinden erişilebiliyorsa
    user="root",
    password="Beytullah.123",
    db_name="person_count_database2",
    port=3306              # MySQL'in çalıştığı port
    )

print(db.list_all_store_informations("Ankara"))