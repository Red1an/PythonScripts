from prettytable import PrettyTable


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