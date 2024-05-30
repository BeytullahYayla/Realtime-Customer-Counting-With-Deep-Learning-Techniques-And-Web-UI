from database import CustomerCountingDatabase
def main():
    # Veritabanı bağlantı bilgileri
    host = "localhost"
    user = "root"
    password = "Beytullah.123"
    db_name = "person_count_database2"
    port = 3307  # Varsayılan MySQL bağlantı noktası

    # Veritabanı bağlantısı oluşturma
    db = CustomerCountingDatabase(host, user, password, db_name, port)

    # Mağaza bilgilerini güncelle
    store_name = "Example Store"
    db.update_store_info(store_name)

    # Ziyaretçi sayılarını güncelle
    man_count = 50
    woman_count = 30
    kid_count = 10
    staff_count = 5
    employee_count = 3
    total_count = man_count + woman_count + kid_count + staff_count + employee_count
    db.update_count_info(store_name, man_count, woman_count, kid_count, staff_count, employee_count, total_count)

    # Veritabanı bağlantısını kapat
    db.close()

if __name__ == "__main__":
    main()
