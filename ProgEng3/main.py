from connection import Neo4jConnection, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from database import DatabaseService
from queries import Queries


def main():
    try:
        with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD) as connection:
            db_service = DatabaseService(connection)
            queries = Queries(connection)

            # Очистка и заполнение БД
            db_service.clear_database()
            db_service.create_sample_data()

            # Просмотр всех данных
            db_service.show_all_data()

            # Выполнение всех запросов
            queries.run_all()

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()