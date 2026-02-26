from models import Workshop, Assembler, Customer, Product, Order
from relationships import Relationships


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
        self.assembler.create("a1", "Иванов",   "Пётр")
        self.assembler.create("a2", "Смирнова", "Анна")
        self.assembler.create("a3", "Козлов",   "Дмитрий")
        self.assembler.create("a4", "Петрова",  "Ольга")
        self.assembler.create("a5", "Николаев", "Сергей")
        self.assembler.create("a6", "Фёдорова", "Мария")
        self.assembler.create("a7", "Орлов",    "Антон")
        self.assembler.create("a8", "Волкова",  "Наталья")


        # Покупатели
        self.customer.create("c1", "Белов",    "Алексей",    "+7-900-111-22-33")
        self.customer.create("c2", "Громова",   "Елена",      "+7-900-222-33-44")
        self.customer.create("c3", "Зайцев",    "Виктор",     "+7-900-333-44-55")
        self.customer.create("c4", "Морозова",  "Ирина",      "+7-900-444-55-66")
        self.customer.create("c5", "Соколов",   "Павел",      "+7-900-555-66-77")
        self.customer.create("c6", "Тарасова",  "Людмила",    "+7-900-666-77-88")
        self.customer.create("c7", "Уваров",    "Константин", "+7-900-777-88-99")
        self.customer.create("c8", "Щербина",   "Татьяна",    "+7-900-888-99-00")


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


    def show_all_data(self):
        self.workshop.show_all()
        self.assembler.show_all()
        self.customer.show_all()
        self.product.show_all()
        self.order.show_all()