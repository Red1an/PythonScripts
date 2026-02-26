from prettytable import PrettyTable


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
        table = PrettyTable()
        table.field_names = ["ID", "Название цеха"]
        for w in self.get_all():
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

    def show_all(self):
        table = PrettyTable()
        table.field_names = ["ID", "Фамилия", "Имя"]
        for a in self.get_all():
            table.add_row([a["id"], a["last_name"], a["first_name"]])
        print("\nВсе сборщики:")
        print(table)


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
            {"id": id, "last_name": last_name, "first_name": first_name, "phone": phone},
        )

    def get_all(self):
        query = """
        MATCH (c:Customer)
        RETURN c.id AS id, c.last_name AS last_name,
               c.first_name AS first_name, c.phone AS phone
        """
        return self.connection.execute_query(query)

    def show_all(self):
        table = PrettyTable()
        table.field_names = ["ID", "Фамилия", "Имя", "Телефон"]
        for c in self.get_all():
            table.add_row([c["id"], c["last_name"], c["first_name"], c["phone"]])
        print("\nВсе покупатели:")
        print(table)


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
            query, {"id": id, "name": name, "category": category, "price": price}
        )

    def get_all(self):
        query = """
        MATCH (p:Product)
        RETURN p.id AS id, p.name AS name, p.category AS category, p.price AS price
        """
        return self.connection.execute_query(query)

    def show_all(self):
        table = PrettyTable()
        table.field_names = ["ID", "Название", "Категория", "Цена"]
        for p in self.get_all():
            table.add_row([p["id"], p["name"], p["category"], p["price"]])
        print("\nВсе изделия:")
        print(table)


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

    def show_all(self):
        table = PrettyTable()
        table.field_names = ["Номер", "Покупатель", "Дата заказа", "Дата выполнения", "Изделия"]
        for o in self.get_all():
            table.add_row([
                o["number"],
                o["customer"],
                o["order_date"],
                o["completion_date"],
                ", ".join(o["products"]),
            ])
        print("\nВсе заказы:")
        print(table)