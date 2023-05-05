import sqlite3


def connect_db():
    db_connection = None
    try:
        db_connection = sqlite3.connect('Store.sqlite')
    except sqlite3.Error as e:
        print(e)
    return db_connection


def select_wish_list_item(conn, client_id, Product_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Wish_list WHERE client_id = ? AND Product_id = ?", (client_id, str(Product_id)))
    item = c.fetchall()
    return item


def select_cart_list_item(conn, client_id, Product_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Cart_list WHERE client_id = ? AND Product_id = ?", (client_id, Product_id))
    item = c.fetchall()
    return item


def select_wish_list_items(conn, client_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Wish_list WHERE client_id = ?", str(client_id))
    items = c.fetchall()
    return items


def select_cart_list_items(conn, client_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Cart_list WHERE client_id = ?", client_id)
    items = c.fetchall()
    return items


def select_reservations(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Reservation")
    reservations = c.fetchall()
    return reservations


def select_client_reservations(conn, client_id, status_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Reservation WHERE client_id = ? and status_id = ?", (client_id, status_id,))
    items = c.fetchall()
    return items


def select_Product(conn, Product_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Product WHERE id = ?", (str(Product_id),))
    Product = c.fetchall()
    return Product


def select_client(conn, login, password):
    c = conn.cursor()
    c.execute("SELECT * FROM Client WHERE client_login = ? AND client_password = ?", (login, password))
    client = c.fetchall()
    return client


def select_client_by_id(conn, client_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Client WHERE id = ?", (client_id,))
    client = c.fetchall()
    return client[0]


def select_worker(conn, login, password):
    c = conn.cursor()
    c.execute("SELECT * FROM Worker WHERE worker_login = ? AND worker_password = ?", (login, password))
    worker = c.fetchall()
    return worker


def select_companies(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Company")
    companies = c.fetchall()
    return companies


def select_Products(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Product")
    Products = c.fetchall()
    return Products


def select_Product_types(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Company")
    companies = c.fetchall()
    return companies


def insert_client(conn, name, phone, login, password) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Client (client_name, client_phone, client_login, client_password) VALUES (?,?,?,?)",
              (name, phone, login, password,))
    conn.commit()
    return True


def insert_wish_list_item(conn, client_id, Product_id) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Wish_list (client_id, Product_id) VALUES (?,?)",
              (client_id, Product_id,))
    conn.commit()
    return True


def insert_cart_list_item(conn, client_id, Product_id) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Cart_list (client_id, Product_id) VALUES (?,?)",
              (client_id, Product_id))
    conn.commit()
    return True


def insert_reservation(conn, client_id, Product_id, status_id) -> bool:
    c = conn.cursor()
    c.execute("INSERT INTO Reservation (client_id, Product_id, status_id) VALUES (?,?,?)",
              (client_id, Product_id, status_id,))
    conn.commit()
    return True


def set_reservation_status(conn, reservation_id, status_id):
    c = conn.cursor()
    c.execute("UPDATE Reservation SET status_id = ? WHERE id = ?",
              (status_id, reservation_id,))
    conn.commit()
    return True


def insert_worker(conn, worker_name, worker_login, worker_password, worker_phone, role_id):
    c = conn.cursor()
    c.execute("INSERT INTO Worker (worker_name, worker_login, worker_password, worker_phone, role_id) "
              "VALUES (?,?,?,?,?)",
              (worker_name, worker_login, worker_password, worker_phone, role_id,))
    conn.commit()


def set_reservation_worker(conn, reservation_id, worker_id):
    c = conn.cursor()
    c.execute("UPDATE Reservation SET worker_id = ? WHERE id = ?",
              (worker_id, reservation_id,))
    conn.commit()
    return True


def select_remainder(conn, Product_id):
    c = conn.cursor()
    c.execute("SELECT remainder FROM Product WHERE Product_id = ?", (Product_id,))
    remainder = c.fetchall()
    return remainder[0]


def set_Product_remainder(conn, remainder, Product_id):
    c = conn.cursor()
    c.execute("UPDATE Product SET remainder = ? WHERE id = ?",
              (remainder, Product_id,))
    conn.commit()
    return True


def delete_Product(conn, Product_id) -> bool:
    c = conn.cursor()
    c.execute("DELETE FROM Product WHERE id = ?",
              (Product_id,))
    conn.commit()
    return True


def delete_wish_list_item(conn, client_id, Product_id) -> bool:
    c = conn.cursor()
    c.execute("DELETE FROM Wish_list WHERE client_id = ? AND Product_id = ?",
              (client_id, Product_id,))
    conn.commit()
    return True


def delete_cart_list_item(conn, client_id, Product_id) -> bool:
    c = conn.cursor()
    c.execute("DELETE FROM Cart_list WHERE client_id = ? AND Product_id = ?",
              (client_id, Product_id,))
    conn.commit()
    return True


def delete_reservation(conn, reservation_id):
    c = conn.cursor()
    c.execute("DELETE FROM Reservation WHERE id = ?",
              (reservation_id,))
    conn.commit()
    return True


def create_tables(conn):
    create_table_country(conn)
    create_table_company(conn)
    create_table_Product_type(conn)
    create_table_Product(conn)
    create_table_client(conn)
    create_table_wish_list(conn)
    create_table_worker_role(conn)
    create_table_worker(conn)
    create_table_reservation_status(conn)
    create_table_reservation(conn)
    create_table_cart_list(conn)


def create_table_country(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Country ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "country_name TEXT"
              ")")


def create_table_company(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Company ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "company_name TEXT, "
              "country_id INTEGER"
              ")")


def create_table_Product_type(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Product_type ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "Product_type_name TEXT"
              ")")


def create_table_Product(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Product ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "Product_name TEXT, "
              "Product_type_id INTEGER, "
              "company_id INTEGER"
              ")")


def create_table_client(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Client ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_name TEXT, "
              "client_login TEXT, "
              "client_password TEXT, "
              "client_phone TEXT"
              ")")


def create_table_reservation_status(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Reservation_status ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "status_name TEXT"
              ")")


def create_table_worker_role(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Worker_role ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "role_name TEXT"
              ")")


def create_table_worker(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Worker ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "worker_name TEXT, "
              "worker_login TEXT, "
              "worker_password TEXT, "
              "worker_phone TEXT, "
              "role_id INTEGER"
              ")")


def create_table_wish_list(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Wish_list ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "Product_id INTEGER"
              ")")


def create_table_reservation(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Reservation ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "Product_id INTEGER, "
              "status_id INTEGER, "
              "worker_id INTEGER"
              ")")


def create_table_cart_list(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Cart_list ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "Product_id INTEGER"
              ")")

