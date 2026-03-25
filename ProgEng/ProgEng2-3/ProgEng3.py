import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from prettytable import PrettyTable

load_dotenv(".env")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DBNAME = os.getenv("NEO4J_DBNAME")


class Neo4jConnection:
    def __init__(self, uri, username, password):
        self._uri = uri
        self._username = username
        self._password = password
        self._driver = None

    def __enter__(self):
        self._driver = GraphDatabase.driver(
            self._uri, auth=(self._username, self._password)
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._driver:
            self._driver.close()

    def execute_query(self, query, parameters=None):
        with self._driver.session(database=NEO4J_DBNAME) as session:
            result = session.run(query, parameters or {})
            return [record for record in result]


class Workshop:
    def __init__(self, connection):
        self.connection = connection

    def clear(self):
        self.connection.execute_query("MATCH (n:Workshop) DETACH DELETE n")

    def create(self, id, name):
        query = "CREATE (:Workshop {id: $id, name: $name})"
        self.connection.execute_query(query, {"id": id, "name": name})

    def get_all(self):
        query = "MATCH (w:Workshop) RETURN w.id AS id, w.name AS name"
        return self.connection.execute_query(query)

    def show_all(self):
        workshops = self.get_all()
        table = PrettyTable()
        table.field_names = ["ID", "Название цеха"]
        for w in workshops:
            table.add_row([w["id"], w["name"]])
        print("\nВсе цеха:")
        print(table)

class Assembler:
    def __init__(self, connection):
        self.connection = connection

    def clear(self):
        self.connection.execute_query("MATCH (n:Assembler) DETACH DELETE n")

    def create(self, id, last_name, first_name):
        query = """
        CREATE (:Assembler {id: $id, last_name: $last_name, first_name: $first_name})
        """
        self.connection.execute_query(
            query, {"id": id, "last_name": last_name, "first_name": first_name}
        )

    def get_all(self):
        query = """
        MATCH (a:Assembler)
        RETURN a.id AS id, a.last_name AS last_name, a.first_name AS first_name
        """
        return self.connection.execute_query(query)

class Customer:
    def __init__(self, connection):
        self.connection = connection

    def clear(self):
        self.connection.execute_query("MATCH (n:Customer) DETACH DELETE n")

    def create(self, id, last_name, first_name, phone):
        query = """
        CREATE (:Customer {id: $id, last_name: $last_name,
                           first_name: $first_name, phone: $phone})
        """
        self.connection.execute_query(
            query,
            {
                "id": id,
                "last_name": last_name,
                "first_name": first_name,
                "phone": phone,
            },
        )

    def get_all(self):
        query = """
        MATCH (c:Customer)
        RETURN c.id AS id, c.last_name AS last_name,
               c.first_name AS first_name, c.phone AS phone
        """
        return self.connection.execute_query(query)

class Product:
    def __init__(self, connection):
        self.connection = connection

    def clear(self):
        self.connection.execute_query("MATCH (n:Product) DETACH DELETE n")

    def create(self, id, name, category, price):
        query = """
        CREATE (:Product {id: $id, name: $name, category: $category, price: $price})
        """
        self.connection.execute_query(
            query,
            {"id": id, "name": name, "category": category, "price": price},
        )

    def get_all(self):
        query = """
        MATCH (p:Product)
        RETURN p.id AS id, p.name AS name, p.category AS category, p.price AS price
        """
        return self.connection.execute_query(query)

class Order:
    def __init__(self, connection):
        self.connection = connection

    def clear(self):
        self.connection.execute_query("MATCH (n:Order) DETACH DELETE n")

    def create(self, id, number, order_date, completion_date):
        query = """
        CREATE (:Order {id: $id, number: $number,
                        order_date: date($order_date),
                        completion_date: date($completion_date)})
        """
        self.connection.execute_query(
            query,
            {
                "id": id,
                "number": number,
                "order_date": order_date,
                "completion_date": completion_date,
            },
        )

    def get_all(self):
        query = """
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
        RETURN o.number AS number, c.last_name AS customer,
               o.order_date AS order_date, o.completion_date AS completion_date,
               collect(p.name) AS products
        ORDER BY o.number
        """
        return self.connection.execute_query(query)

class Relationships:
    def __init__(self, connection):
        self.connection = connection

    def customer_placed_order(self, customer_id, order_id):
        query = """
        MATCH (c:Customer {id: $customer_id}), (o:Order {id: $order_id})
        MERGE (c)-[:PLACED]->(o)
        """
        self.connection.execute_query(
            query, {"customer_id": customer_id, "order_id": order_id}
        )

    def order_contains_product(self, order_id, product_id):
        query = """
        MATCH (o:Order {id: $order_id}), (p:Product {id: $product_id})
        MERGE (o)-[:CONTAINS]->(p)
        """
        self.connection.execute_query(
            query, {"order_id": order_id, "product_id": product_id}
        )

    def product_made_in_workshop(self, product_id, workshop_id):
        query = """
        MATCH (p:Product {id: $product_id}), (w:Workshop {id: $workshop_id})
        MERGE (p)-[:MADE_IN]->(w)
        """
        self.connection.execute_query(
            query, {"product_id": product_id, "workshop_id": workshop_id}
        )

    def assembler_assembled_product(self, assembler_id, product_id):
        query = """
        MATCH (a:Assembler {id: $assembler_id}), (p:Product {id: $product_id})
        MERGE (a)-[:ASSEMBLED]->(p)
        """
        self.connection.execute_query(
            query, {"assembler_id": assembler_id, "product_id": product_id}
        )

class DatabaseService:
    def __init__(self, connection):
        self.connection = connection
        self.workshop = Workshop(connection)
        self.assembler = Assembler(connection)
        self.customer = Customer(connection)
        self.product = Product(connection)
        self.order = Order(connection)
        self.rel = Relationships(connection)

    def clear_database(self):
        self.connection.execute_query("MATCH (n) DETACH DELETE n")


    def create_sample_data(self):
        # Цеха
        self.workshop.create("w1", "Кухонный цех")
        self.workshop.create("w2", "Цех спален")
        self.workshop.create("w3", "Цех гостиных")
        self.workshop.create("w4", "Детский цех")
        self.workshop.create("w5", "Цех гостевых спален")

        # Сборщики
        self.assembler.create("a1", "Иванов", "Пётр")
        self.assembler.create("a2", "Смирнова", "Анна")
        self.assembler.create("a3", "Козлов", "Дмитрий")
        self.assembler.create("a4", "Петрова", "Ольга")
        self.assembler.create("a5", "Николаев", "Сергей")
        self.assembler.create("a6", "Фёдорова", "Мария")
        self.assembler.create("a7", "Орлов", "Антон")
        self.assembler.create("a8", "Волкова", "Наталья")


        # Покупатели
        self.customer.create("c1", "Беловы",    "Алексей",    "+7-900-111-22-33")
        self.customer.create("c2", "Громовы",   "Елена",      "+7-900-222-33-44")
        self.customer.create("c3", "Зайцев",    "Виктор",     "+7-900-333-44-55")
        self.customer.create("c4", "Морозова",  "Ирина",      "+7-900-444-55-66")
        self.customer.create("c5", "Соколов",   "Павел",      "+7-900-555-66-77")
        self.customer.create("c6", "Тарасова",  "Людмила",    "+7-900-666-77-88")
        self.customer.create("c7", "Уваров",    "Константин", "+7-900-777-88-99")
        self.customer.create("c8", "Щербины",   "Татьяна",    "+7-900-888-99-00")


        # Изделия
        self.product.create("p1",  'Кухонный гарнитур "Классика"', "кухонная",         85000)
        self.product.create("p2",  "Обеденный стол",                "кухонная",         25000)
        self.product.create("p3",  'Кровать двуспальная "Люкс"',   "спальня",          60000)
        self.product.create("p4",  "Шкаф-купе 3-дверный",          "спальня",          45000)
        self.product.create("p5",  'Диван угловой "Комфорт"',      "гостиная",         70000)
        self.product.create("p6",  "Журнальный столик",             "гостиная",         15000)
        self.product.create("p7",  'Стенка "Гостиная Модерн"',     "гостиная",         95000)
        self.product.create("p8",  "Кровать односпальная детская",  "детская",          30000)
        self.product.create("p9",  "Письменный стол детский",       "детская",          22000)
        self.product.create("p10", "Кровать гостевая",              "гостевая спальня", 35000)

        # Заказы
        self.order.create("o1", "2024-001", "2024-01-10", "2024-01-25")
        self.order.create("o2", "2024-002", "2024-02-03", "2024-02-20")
        self.order.create("o3", "2024-003", "2024-03-15", "2024-04-01")
        self.order.create("o4", "2024-004", "2024-04-05", "2024-04-20")
        self.order.create("o5", "2024-005", "2024-05-01", "2024-05-18")
        self.order.create("o6", "2024-006", "2024-06-12", "2024-06-30")
        self.order.create("o7", "2024-007", "2024-07-08", "2024-07-25")
        self.order.create("o8", "2024-008", "2024-08-19", "2024-09-05")
        self.order.create("o9", "2024-009", "2024-09-22", "2024-10-10")

        # Связи: Customer PLACED Order
        self.rel.customer_placed_order("c1", "o1")
        self.rel.customer_placed_order("c2", "o2")
        self.rel.customer_placed_order("c3", "o3")
        self.rel.customer_placed_order("c4", "o4")
        self.rel.customer_placed_order("c5", "o5")
        self.rel.customer_placed_order("c6", "o6")
        self.rel.customer_placed_order("c7", "o7")
        self.rel.customer_placed_order("c8", "o8")
        self.rel.customer_placed_order("c3", "o9")

        # Связи: Order CONTAINS Product
        self.rel.order_contains_product("o1", "p1")
        self.rel.order_contains_product("o1", "p2")
        self.rel.order_contains_product("o2", "p3")
        self.rel.order_contains_product("o2", "p4")
        self.rel.order_contains_product("o3", "p5")
        self.rel.order_contains_product("o3", "p6")
        self.rel.order_contains_product("o4", "p7")
        self.rel.order_contains_product("o5", "p8")
        self.rel.order_contains_product("o5", "p9")
        self.rel.order_contains_product("o6", "p10")
        self.rel.order_contains_product("o7", "p1")
        self.rel.order_contains_product("o7", "p5")
        self.rel.order_contains_product("o8", "p3")
        self.rel.order_contains_product("o8", "p6")
        self.rel.order_contains_product("o9", "p2")
        self.rel.order_contains_product("o9", "p8")

        # Связи: Product MADE_IN Workshop
        self.rel.product_made_in_workshop("p1",  "w1")
        self.rel.product_made_in_workshop("p2",  "w1")
        self.rel.product_made_in_workshop("p3",  "w2")
        self.rel.product_made_in_workshop("p4",  "w2")
        self.rel.product_made_in_workshop("p5",  "w3")
        self.rel.product_made_in_workshop("p6",  "w3")
        self.rel.product_made_in_workshop("p7",  "w3")
        self.rel.product_made_in_workshop("p8",  "w4")
        self.rel.product_made_in_workshop("p9",  "w4")
        self.rel.product_made_in_workshop("p10", "w5")

        # Связи: Assembler ASSEMBLED Product
        self.rel.assembler_assembled_product("a1", "p1")
        self.rel.assembler_assembled_product("a2", "p2")
        self.rel.assembler_assembled_product("a3", "p3")
        self.rel.assembler_assembled_product("a4", "p4")
        self.rel.assembler_assembled_product("a5", "p5")
        self.rel.assembler_assembled_product("a6", "p6")
        self.rel.assembler_assembled_product("a7", "p7")
        self.rel.assembler_assembled_product("a8", "p8")
        self.rel.assembler_assembled_product("a1", "p9")
        self.rel.assembler_assembled_product("a3", "p10")


class Queries:
    def __init__(self, connection):
        self.connection = connection

    # Запрос 1 (рис. 16) — Информация о всех клиентах
    def query1_all_customers(self):
        query = """
        MATCH (c:Customer)
        RETURN c.last_name, c.first_name, c.phone
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Фамилия", "Имя", "Телефон"]
        for r in results:
            table.add_row([r["c.last_name"], r["c.first_name"], r["c.phone"]])
        print("\nЗапрос 1 — Информация о всех клиентах:")
        print(table)

    # Запрос 2 (рис. 17) — Стоимость изделий из категории «гостиная»
    def query2_living_room_products(self):
        query = """
        MATCH (p:Product)
        WHERE p.category = 'гостиная'
        RETURN p.name, p.price
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Название", "Цена"]
        for r in results:
            table.add_row([r["p.name"], r["p.price"]])
        print("\nЗапрос 2 — Стоимость изделий из категории «гостиная»:")
        print(table)

    # Запрос 3 (рис. 18) — Вывод заказов по каждому клиенту
    def query3_orders_by_customer(self):
        query = """
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
        RETURN c.last_name, o.number, o.order_date, collect(p.name) AS products
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Покупатель", "Номер заказа", "Дата заказа", "Изделия"]
        for r in results:
            table.add_row([
                r["c.last_name"],
                r["o.number"],
                r["o.order_date"],
                ", ".join(r["products"]),
            ])
        print("\nЗапрос 3 — Вывод заказов по каждому клиенту:")
        print(table)

    # Запрос 4 — Количество изделий и сумма по каждому заказу
    def query4_order_totals(self):
        query = """
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
        WITH c, o, count(p) AS item_count, sum(p.price) AS total
        RETURN c.last_name, o.number, item_count, total
        ORDER BY total DESC
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Покупатель", "Номер заказа", "Кол-во изделий", "Сумма (руб.)"]
        for r in results:
            table.add_row([r["c.last_name"], r["o.number"], r["item_count"], r["total"]])
        print("\nЗапрос 4 — Сумма по заказам:")
        print(table)

    # Запрос 5 (рис. 20) — Граф со связями по всем данным
    def query5_full_graph(self):
        query = """
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)-[:MADE_IN]->(w:Workshop)
        RETURN c.last_name, o.number, p.name, w.name
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Покупатель", "Заказ", "Изделие", "Цех"]
        for r in results:
            table.add_row([r["c.last_name"], r["o.number"], r["p.name"], r["w.name"]])
        print("\nЗапрос 5 — Полный граф связей:")
        print(table)

    # Запрос 6 (рис. 21) — Цех с наибольшим количеством произведённых товаров
    def query6_busiest_workshop(self):
        query = """
        MATCH (p:Product)-[:MADE_IN]->(w:Workshop)
        WITH w, count(p) AS product_count
        ORDER BY product_count DESC
        LIMIT 1
        RETURN w.name, product_count
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Цех", "Количество изделий"]
        for r in results:
            table.add_row([r["w.name"], r["product_count"]])
        print("\nЗапрос 6 — Цех с наибольшим количеством товаров:")
        print(table)

    # Запрос 7 (рис. 22) — Информация по времени выполнения каждого заказа
    def query7_order_duration(self):
        query = """
        MATCH (c:Customer)-[:PLACED]->(o:Order)
        WITH c, o, duration.between(o.order_date, o.completion_date).days AS days
        RETURN c.last_name, o.number, o.order_date, o.completion_date, days
        ORDER BY days DESC
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Покупатель", "Номер заказа", "Дата заказа", "Дата выполнения", "Дней"]
        for r in results:
            table.add_row([
                r["c.last_name"],
                r["o.number"],
                r["o.order_date"],
                r["o.completion_date"],
                r["days"],
            ])
        print("\nЗапрос 7 — Время выполнения каждого заказа:")
        print(table)

    # Запрос 8 (рис. 23) — Клиенты, заказавшие мебель из детской категории
    def query8_children_furniture_customers(self):
        query = """
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
        WHERE p.category = 'детская'
        RETURN DISTINCT c.last_name, c.phone, o.number
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Покупатель", "Телефон", "Номер заказа"]
        for r in results:
            table.add_row([r["c.last_name"], r["c.phone"], r["o.number"]])
        print("\nЗапрос 8 — Клиенты, заказавшие детскую мебель:")
        print(table)

    # Запрос 9 (рис. 24) — Вывод всех цехов
    def query9_all_workshops(self):
        query = """
        MATCH (w:Workshop)
        RETURN w.name
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Название цеха"]
        for r in results:
            table.add_row([r["w.name"]])
        print("\nЗапрос 9 — Все цеха:")
        print(table)

    # Запрос 10 (рис. 25) — Количество собранных изделий по каждому сборщику
    def query10_assembler_rating(self):
        query = """
        MATCH (a:Assembler)-[:ASSEMBLED]->(p:Product)
        WITH a, count(p) AS assembled_count
        RETURN a.last_name, a.first_name, assembled_count
        ORDER BY assembled_count DESC
        """
        results = self.connection.execute_query(query)
        table = PrettyTable()
        table.field_names = ["Фамилия", "Имя", "Собрано изделий"]
        for r in results:
            table.add_row([r["a.last_name"], r["a.first_name"], r["assembled_count"]])
        print("\nЗапрос 10 — Количество изделий по каждому сборщику:")
        print(table)

    def run_all(self):
        self.query1_all_customers()
        self.query2_living_room_products()
        self.query3_orders_by_customer()
        self.query4_order_totals()
        self.query5_full_graph()
        self.query6_busiest_workshop()
        self.query7_order_duration()
        self.query8_children_furniture_customers()
        self.query9_all_workshops()
        self.query10_assembler_rating()

def main():
    try:
        with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD) as connection:
            db_service = DatabaseService(connection)
            queries = Queries(connection)

            # Очистка и заполнение БД
            db_service.clear_database()
            db_service.create_sample_data()

            # Выполнение всех запросов
            queries.run_all()

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()