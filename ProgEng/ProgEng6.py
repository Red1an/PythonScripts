import os
from dotenv import load_dotenv
from datetime import datetime
import clickhouse_connect


# Подключение
class DatabaseConnection:
    def __init__(self, host, port, username, password, database='furniture'):
        self.client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password
        )
        self.database = database

    def close(self):
        self.client.close()

    def clear_database(self):
        try:
            tables = self.client.query(f"SHOW TABLES FROM {self.database}").result_rows
            for table in tables:
                table_name = table[0]
                self.client.command(f"DROP TABLE {self.database}.{table_name}")
                print(f"Таблица {self.database}.{table_name} удалена.")
            print("База данных очищена.")
            return True
        except Exception as e:
            print(f"Ошибка при очистке БД: {e}")
            return False



# Классы таблиц
class Workshop:
    def __init__(self, connection):
        self.connection = connection
        self.table = f"{connection.database}.workshops"
        self._create_table()

    def _create_table(self):
        self.connection.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                workshop_id UInt32,
                workshopName String
            )
            ENGINE = MergeTree()
            PRIMARY KEY (workshop_id)
        """)

    def create(self, workshop_id, workshop_name):
        self.connection.client.command(f"""
            INSERT INTO {self.table} (workshop_id, workshopName)
            VALUES ({workshop_id}, '{workshop_name}')
        """)
        return workshop_id

    def get(self, workshop_id):
        result = self.connection.client.query(
            f"SELECT * FROM {self.table} WHERE workshop_id = {workshop_id}"
        ).result_rows
        return result[0] if result else None

    def get_all(self):
        return self.connection.client.query(f"SELECT * FROM {self.table}").result_rows

    def update(self, workshop_id, update_fields):
        set_clause = ", ".join([f"{k} = '{v}'" for k, v in update_fields.items()])
        self.connection.client.command(
            f"ALTER TABLE {self.table} UPDATE {set_clause} WHERE workshop_id = {workshop_id}"
        )

    def delete(self, workshop_id):
        self.connection.client.command(
            f"ALTER TABLE {self.table} DELETE WHERE workshop_id = {workshop_id}"
        )


class Assembler:
    def __init__(self, connection):
        self.connection = connection
        self.table = f"{connection.database}.assemblers"
        self._create_table()

    def _create_table(self):
        self.connection.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                assembler_id UInt32,
                assemblerName String,
                assemblerSurname String
            )
            ENGINE = MergeTree()
            PRIMARY KEY (assembler_id)
        """)

    def create(self, assembler_id, name, surname):
        self.connection.client.command(f"""
            INSERT INTO {self.table} (assembler_id, assemblerName, assemblerSurname)
            VALUES ({assembler_id}, '{name}', '{surname}')
        """)
        return assembler_id

    def get(self, assembler_id):
        result = self.connection.client.query(
            f"SELECT * FROM {self.table} WHERE assembler_id = {assembler_id}"
        ).result_rows
        return result[0] if result else None

    def get_all(self):
        return self.connection.client.query(f"SELECT * FROM {self.table}").result_rows

    def update(self, assembler_id, update_fields):
        set_clause = ", ".join([f"{k} = '{v}'" for k, v in update_fields.items()])
        self.connection.client.command(
            f"ALTER TABLE {self.table} UPDATE {set_clause} WHERE assembler_id = {assembler_id}"
        )

    def delete(self, assembler_id):
        self.connection.client.command(
            f"ALTER TABLE {self.table} DELETE WHERE assembler_id = {assembler_id}"
        )


class Customer:
    def __init__(self, connection):
        self.connection = connection
        self.table = f"{connection.database}.customers"
        self._create_table()

    def _create_table(self):
        self.connection.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                customer_id UInt32,
                customerSurname String,
                customerAddress String
            )
            ENGINE = MergeTree()
            PRIMARY KEY (customer_id)
        """)

    def create(self, customer_id, surname, address):
        self.connection.client.command(f"""
            INSERT INTO {self.table} (customer_id, customerSurname, customerAddress)
            VALUES ({customer_id}, '{surname}', '{address}')
        """)
        return customer_id

    def get(self, customer_id):
        result = self.connection.client.query(
            f"SELECT * FROM {self.table} WHERE customer_id = {customer_id}"
        ).result_rows
        return result[0] if result else None

    def get_all(self):
        return self.connection.client.query(f"SELECT * FROM {self.table}").result_rows

    def update(self, customer_id, update_fields):
        set_clause = ", ".join([f"{k} = '{v}'" for k, v in update_fields.items()])
        self.connection.client.command(
            f"ALTER TABLE {self.table} UPDATE {set_clause} WHERE customer_id = {customer_id}"
        )

    def delete(self, customer_id):
        self.connection.client.command(
            f"ALTER TABLE {self.table} DELETE WHERE customer_id = {customer_id}"
        )

    def get_last_id(self):
        result = self.connection.client.query(f"SELECT max(customer_id) FROM {self.table}").result_rows
        return result[0][0] if result[0][0] else 0


class Product:
    def __init__(self, connection):
        self.connection = connection
        self.table = f"{connection.database}.products"
        self._create_table()

    def _create_table(self):
        self.connection.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                product_id UInt32,
                productName String,
                workshop_id UInt32,
                assembler_id UInt32,
                price UInt32
            )
            ENGINE = MergeTree()
            PRIMARY KEY (product_id)
        """)

    def create(self, product_id, name, workshop_id, assembler_id, price):
        self.connection.client.command(f"""
            INSERT INTO {self.table} (product_id, productName, workshop_id, assembler_id, price)
            VALUES ({product_id}, '{name}', {workshop_id}, {assembler_id}, {price})
        """)
        return product_id

    def get(self, product_id):
        result = self.connection.client.query(
            f"SELECT * FROM {self.table} WHERE product_id = {product_id}"
        ).result_rows
        return result[0] if result else None

    def get_all(self):
        return self.connection.client.query(f"SELECT * FROM {self.table}").result_rows

    def update(self, product_id, update_fields):
        set_clause = ", ".join([f"{k} = '{v}'" for k, v in update_fields.items()])
        self.connection.client.command(
            f"ALTER TABLE {self.table} UPDATE {set_clause} WHERE product_id = {product_id}"
        )

    def delete(self, product_id):
        self.connection.client.command(
            f"ALTER TABLE {self.table} DELETE WHERE product_id = {product_id}"
        )

    def get_last_id(self):
        result = self.connection.client.query(f"SELECT max(product_id) FROM {self.table}").result_rows
        return result[0][0] if result[0][0] else 0


class Order:
    def __init__(self, connection):
        self.connection = connection
        self.table = f"{connection.database}.orders"
        self._create_table()

    def _create_table(self):
        self.connection.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                order_id UInt32,
                customer_id UInt32,
                orderDate Date,
                completionDate Date
            )
            ENGINE = MergeTree()
            PRIMARY KEY (order_id, orderDate)
        """)

    def create(self, order_id, customer_id, order_date, completion_date):
        self.connection.client.command(f"""
            INSERT INTO {self.table} (order_id, customer_id, orderDate, completionDate)
            VALUES ({order_id}, {customer_id}, '{order_date}', '{completion_date}')
        """)
        return order_id

    def get(self, order_id):
        result = self.connection.client.query(
            f"SELECT * FROM {self.table} WHERE order_id = {order_id}"
        ).result_rows
        return result[0] if result else None

    def get_all(self):
        return self.connection.client.query(f"SELECT * FROM {self.table}").result_rows

    def update(self, order_id, update_fields):
        set_clause = ", ".join([f"{k} = '{v}'" for k, v in update_fields.items()])
        self.connection.client.command(
            f"ALTER TABLE {self.table} UPDATE {set_clause} WHERE order_id = {order_id}"
        )

    def delete(self, order_id):
        self.connection.client.command(
            f"ALTER TABLE {self.table} DELETE WHERE order_id = {order_id}"
        )

    def get_last_id(self):
        result = self.connection.client.query(f"SELECT max(order_id) FROM {self.table}").result_rows
        return result[0][0] if result[0][0] else 0


class OrderItem:
    def __init__(self, connection):
        self.connection = connection
        self.table = f"{connection.database}.order_items"
        self._create_table()

    def _create_table(self):
        self.connection.client.command(f"""
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                item_id UInt32,
                order_id UInt32,
                product_id UInt32,
                quantity UInt32
            )
            ENGINE = MergeTree()
            PRIMARY KEY (item_id, order_id)
        """)

    def create(self, item_id, order_id, product_id, quantity):
        self.connection.client.command(f"""
            INSERT INTO {self.table} (item_id, order_id, product_id, quantity)
            VALUES ({item_id}, {order_id}, {product_id}, {quantity})
        """)
        return item_id

    def get_all(self):
        return self.connection.client.query(f"SELECT * FROM {self.table}").result_rows



# Сервис — заполнение и запросы
class DatabaseService:
    def __init__(self, connection):
        self.connection = connection
        self.workshop_model   = Workshop(connection)
        self.assembler_model  = Assembler(connection)
        self.customer_model   = Customer(connection)
        self.product_model    = Product(connection)
        self.order_model      = Order(connection)
        self.order_item_model = OrderItem(connection)

    def create_sample_data(self):
        # Цеха
        workshops = [
            (1, 'Кухонный'),
            (2, 'Для хозяйской спальни'),
            (3, 'Для гостевых спален'),
            (4, 'Гостиная'),
            (5, 'Детская'),
        ]
        for w in workshops:
            self.workshop_model.create(*w)
        print("Цеха созданы.")

        assemblers = [
            (1, 'Иван',    'Кузнецов'),
            (2, 'Мария',   'Соколова'),
            (3, 'Алексей', 'Попов'),
            (4, 'Елена',   'Новикова'),
            (5, 'Дмитрий', 'Морозов'),
        ]
        for a in assemblers:
            self.assembler_model.create(*a)
        print("Сборщики созданы.")

        customers = [
            (1, 'Петров',   'ул. Ленина, д. 5'),
            (2, 'Сидорова', 'ул. Мира, д. 12'),
            (3, 'Захаров',  'пр. Победы, д. 3'),
            (4, 'Орлова',   'ул. Садовая, д. 8'),
            (5, 'Фёдоров',  'ул. Цветочная, д. 1'),
            (6, 'Макарова', 'пр. Гагарина, д. 7'),
            (7, 'Тихонов',  'ул. Советская, д. 15'),
        ]
        for c in customers:
            self.customer_model.create(*c)
        print("Покупатели созданы.")

        products = [
            (1,  'Кухонный стол',        1, 1, 500),
            (2,  'Кухонный гарнитур',    1, 2, 1500),
            (3,  'Двуспальная кровать',  2, 3, 1200),
            (4,  'Шкаф-купе',            2, 1, 900),
            (5,  'Односпальная кровать', 3, 4, 700),
            (6,  'Тумбочка гостевая',   3, 2, 300),
            (7,  'Диван',               4, 5, 1100),
            (8,  'Журнальный столик',   4, 3, 400),
            (9,  'Детская кровать',     5, 4, 650),
            (10, 'Детский стол',        5, 5, 450),
        ]
        for p in products:
            self.product_model.create(*p)
        print("Изделия созданы.")

        orders = [
            (1, 1, '2024-01-10', '2024-01-20'),
            (2, 2, '2024-02-05', '2024-02-18'),
            (3, 3, '2024-02-14', '2024-03-01'),
            (4, 4, '2024-03-03', '2024-03-15'),
            (5, 5, '2024-04-07', '2024-04-20'),
            (6, 6, '2024-05-11', '2024-05-25'),
            (7, 7, '2024-06-01', '2024-06-14'),
            (8, 1, '2024-07-08', '2024-07-22'),
            (9, 3, '2024-08-15', '2024-08-30'),
        ]
        for o in orders:
            self.order_model.create(*o)
        print("Заказы созданы.")

        items = [
            (1,  1, 1,  1),
            (2,  1, 2,  1),
            (3,  2, 3,  1),
            (4,  2, 4,  1),
            (5,  3, 7,  1),
            (6,  3, 8,  2),
            (7,  4, 9,  1),
            (8,  4, 10, 1),
            (9,  5, 5,  2),
            (10, 5, 6,  2),
            (11, 6, 2,  1),
            (12, 6, 1,  1),
            (13, 7, 3,  1),
            (14, 7, 7,  1),
            (15, 8, 4,  1),
            (16, 9, 9,  1),
            (17, 9, 10, 1),
        ]
        for i in items:
            self.order_item_model.create(*i)
        print("Состав заказов создан.")

    # Запросы
    def query_1_orders_by_customer_surname(self, surname):
        #1. Все заказы конкретного покупателя по фамилии
        result = self.connection.client.query(f"""
            SELECT o.order_id, o.orderDate, o.completionDate
            FROM furniture.orders o
            INNER JOIN furniture.customers c ON o.customer_id = c.customer_id
            WHERE c.customerSurname = '{surname}'
        """).result_rows
        print(f"\n[Запрос 1] Заказы покупателя {surname}:")
        for row in result:
            print(row)

    def query_2_order_items(self, order_id):
        #2. Список изделий в заказе
        result = self.connection.client.query(f"""
            SELECT p.productName, oi.quantity, p.price
            FROM furniture.order_items oi
            INNER JOIN furniture.products p ON oi.product_id = p.product_id
            WHERE oi.order_id = {order_id}
        """).result_rows
        print(f"\n[Запрос 2] Состав заказа №{order_id}:")
        for row in result:
            print(row)

    def query_3_orders_count_per_customer(self):
        #3. Количество заказов по каждому покупателю
        result = self.connection.client.query("""
            SELECT c.customerSurname, COUNT(o.order_id) AS order_count
            FROM furniture.customers c
            INNER JOIN furniture.orders o ON c.customer_id = o.customer_id
            GROUP BY c.customerSurname
            ORDER BY order_count DESC
        """).result_rows
        print("\n[Запрос 3] Количество заказов по покупателям:")
        for row in result:
            print(row)

    def query_4_products_by_workshop(self, workshop_name):
        #4. Все изделия из указанного цеха
        result = self.connection.client.query(f"""
            SELECT p.productName, p.price
            FROM furniture.products p
            INNER JOIN furniture.workshops w ON p.workshop_id = w.workshop_id
            WHERE w.workshopName = '{workshop_name}'
        """).result_rows
        print(f"\n[Запрос 4] Изделия цеха '{workshop_name}':")
        for row in result:
            print(row)

    def query_5_assemblers_productivity(self):
        #5. Сборщики и количество собранных изделий
        result = self.connection.client.query("""
            SELECT a.assemblerSurname, a.assemblerName, COUNT(p.product_id) AS products_count
            FROM furniture.assemblers a
            INNER JOIN furniture.products p ON a.assembler_id = p.assembler_id
            GROUP BY a.assembler_id, a.assemblerSurname, a.assemblerName
            ORDER BY products_count DESC
        """).result_rows
        print("\n[Запрос 5] Продуктивность сборщиков:")
        for row in result:
            print(row)

    def query_6_orders_by_completion_month(self, date_from, date_to):
        #6. Заказы, выполненные в указанный период
        result = self.connection.client.query(f"""
            SELECT o.order_id, c.customerSurname, o.orderDate, o.completionDate
            FROM furniture.orders o
            INNER JOIN furniture.customers c ON o.customer_id = c.customer_id
            WHERE completionDate BETWEEN toDate('{date_from}') AND toDate('{date_to}')
        """).result_rows
        print(f"\n[Запрос 6] Заказы, выполненные с {date_from} по {date_to}:")
        for row in result:
            print(row)

    def query_7_total_cost_per_order(self):
        #7. Суммарная стоимость каждого заказа
        result = self.connection.client.query("""
            SELECT oi.order_id, c.customerSurname, SUM(p.price * oi.quantity) AS totalCost
            FROM furniture.order_items oi
            INNER JOIN furniture.products p ON oi.product_id = p.product_id
            INNER JOIN furniture.orders o ON oi.order_id = o.order_id
            INNER JOIN furniture.customers c ON o.customer_id = c.customer_id
            GROUP BY oi.order_id, c.customerSurname
            ORDER BY oi.order_id
        """).result_rows
        print("\n[Запрос 7] Суммарная стоимость заказов:")
        for row in result:
            print(row)

    def query_8_days_to_complete(self):
        #8. Срок выполнения каждого заказа в днях
        result = self.connection.client.query("""
            SELECT o.order_id, c.customerSurname, o.orderDate, o.completionDate,
                   dateDiff('day', o.orderDate, o.completionDate) AS days_to_complete
            FROM furniture.orders o
            INNER JOIN furniture.customers c ON o.customer_id = c.customer_id
            ORDER BY days_to_complete DESC
        """).result_rows
        print("\n[Запрос 8] Срок выполнения заказов (дней):")
        for row in result:
            print(row)

    def show_all_data(self):
        print("\n     ВСЕ ДАННЫЕ В БД    ")

        print("\nЦеха:")
        for row in self.workshop_model.get_all():
            print(row)

        print("\nСборщики:")
        for row in self.assembler_model.get_all():
            print(row)

        print("\nПокупатели:")
        for row in self.customer_model.get_all():
            print(row)

        print("\nИзделия:")
        for row in self.product_model.get_all():
            print(row)

        print("\nЗаказы:")
        for row in self.order_model.get_all():
            print(row)

        print("\nСостав заказов:")
        for row in self.order_item_model.get_all():
            print(row)


# main
def main():
    load_dotenv(".env")

    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", 18123))
    username = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "0000")

    connection = DatabaseConnection(host, port, username, password)
    connection.clear_database()
    db = DatabaseService(connection)
    db.create_sample_data()
    db.show_all_data()

    db.customer_model.update(1, {"customerSurname": "Петров"})

    last_id = db.customer_model.get_last_id()
    db.customer_model.create(last_id + 1, "Новиков", "ул. Новая, д. 1")
    print("Добавлен новый покупатель:", db.customer_model.get(last_id + 1))

    db.customer_model.delete(last_id + 1)
    print(f"Покупатель {last_id + 1} удалён.")

    # Выполнение запросов
    print("\n    ЗАПРОСЫ    ")
    db.query_1_orders_by_customer_surname("Петров")
    db.query_2_order_items(1)
    db.query_3_orders_count_per_customer()
    db.query_4_products_by_workshop("Детская")
    db.query_5_assemblers_productivity()
    db.query_6_orders_by_completion_month("2024-02-01", "2024-02-28")
    db.query_7_total_cost_per_order()
    db.query_8_days_to_complete()

    connection.close()


if __name__ == "__main__":
    main()