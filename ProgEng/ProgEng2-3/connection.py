import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

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