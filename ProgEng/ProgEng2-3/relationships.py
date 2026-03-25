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