import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

def create_table(connection, cursor):
    cursor.execute('''CREATE TABLE if not exists locations
    (location_id int PRIMARY KEY,
    city varchar(30),
    postal_code varchar(12)
    ); ''')

    cursor.execute("""
        INSERT INTO locations (location_id, city, postal_code)
        VALUES
            (1,  'Roma',                '00989'),
            (2,  'Venice',              '10934'),
            (3,  'Tokyo',               '1689'),
            (4,  'Hiroshima',           '6823'),
            (5,  'Southlake',           '26192'),
            (6,  'South San Francisco', '99236'),
            (7,  'South Brunswick',     '50090'),
            (8,  'Seattle',             '98199'),
            (9,  'Toronto',             'M5V 2L7'),
            (10, 'Whitehorse',          'YSW 9T2')
        ON CONFLICT (location_id) DO NOTHING;
    """)
    connection.commit()
    table_locations = pd.read_sql_query("SELECT * FROM locations", connection)
    print("Таблица locations:")
    print(table_locations, "\n")

    cursor.execute("ALTER TABLE employees ADD COLUMN location_id INT;")
    connection.commit()

    cursor.execute("""
        ALTER TABLE employees
        ADD CONSTRAINT fk_employees_location
        FOREIGN KEY (location_id) REFERENCES locations(location_id);
    """)
    connection.commit()

    cursor.execute("UPDATE employees SET location_id = (employee_id % 10) + 1;")
    connection.commit()

    df_emp = pd.read_sql_query(
        "SELECT employee_id, first_name, last_name, location_id FROM employees",
        connection
    )
    print("Таблица employees с location_id:")
    print(df_emp, "\n")

def requests(connection):
    df1 = pd.read_sql_query("""
        SELECT e.employee_id,
               e.first_name,
               e.last_name,
               e.salary,
               e.job_id,
               j.min_salary
        FROM employees e
        JOIN jobs j ON e.job_id = j.job_id
        WHERE e.salary = j.min_salary;
    """, connection)

    df2 = pd.read_sql_query("""
            SELECT first_name || ' ' || last_name AS worker,
                   salary
            FROM employees
            WHERE salary = (SELECT MIN(salary) FROM employees);
        """, connection)

    df3 = pd.read_sql_query("""
            SELECT e.first_name || ' ' || e.last_name AS worker,
                   e.salary,
                   e.job_id,
                   j.max_salary,
                   l.city
            FROM employees e
            JOIN jobs      j ON e.job_id      = j.job_id
            JOIN locations l ON e.location_id = l.location_id
            WHERE e.salary = j.max_salary
            ORDER BY l.city;
        """, connection)

    print("Запрос 1: Сотрудники с зарплатой = минимальной по должности")
    print(df1, "\n")

    print("Запрос 2: Сотрудник с минимальной зарплатой (колонка worker)")
    print(df2, "\n")

    print("Запрос 3: Сотрудники с мин. зарплатой по должности + город")
    print(df3, "\n")

def select_data(cursor):
    cursor.callproc('select_data', [20])
    result_proc = pd.DataFrame(cursor.fetchall())
    print("Вызов select_data(20)")
    print(result_proc, "\n")

def select_data1(connection, cursor):
    cursor.execute("""
        CREATE OR REPLACE FUNCTION select_data1(id_dept INT)
        RETURNS SETOF departments AS $$
            SELECT * FROM departments
            WHERE departments.department_id > id_dept;
        $$ LANGUAGE SQL;
    """)
    connection.commit()

    cursor.callproc('select_data1', [30])
    result_proc1 = pd.DataFrame(cursor.fetchall())
    print("Вызов select_data1(30):")
    print(result_proc1, "\n")

def person_function(connection, cursor):
    cursor.execute("""
        CREATE TYPE dept_salary_stat AS (
            department_name VARCHAR,
            emp_count       BIGINT,
            avg_salary      NUMERIC(10,2),
            min_salary      NUMERIC(10,2),
            max_salary      NUMERIC(10,2)
        );
    """)
    connection.commit()

    cursor.execute("""
        CREATE OR REPLACE FUNCTION get_dept_salary_stat(min_emp_count INT)
        RETURNS SETOF dept_salary_stat AS $$
            SELECT d.department_name,
                   COUNT(e.employee_id)      AS emp_count,
                   ROUND(AVG(e.salary), 2)   AS avg_salary,
                   MIN(e.salary)             AS min_salary,
                   MAX(e.salary)             AS max_salary
            FROM departments d
            JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_name
            HAVING COUNT(e.employee_id) > min_emp_count
            ORDER BY emp_count DESC;
        $$ LANGUAGE SQL;
    """)
    connection.commit()

    cursor.callproc('get_dept_salary_stat', [2])
    own_df = pd.DataFrame(
        cursor.fetchall(),
        columns=['department_name', 'emp_count', 'avg_salary', 'min_salary', 'max_salary']
    )
    print("Вызов get_dept_salary_stat(2) — отделы с более чем 2 сотрудниками:")
    print(own_df, "\n")

def main():
    load_dotenv(".env")

    connection = psycopg2.connect(database=os.getenv("PG_DATABASE"),
                                  user=os.getenv("PG_USER"),
                                  host=os.getenv("PG_HOST"),
                                  password=os.getenv("PG_PASSWORD"),
                                  port=os.getenv("PG_PORT"))

    cursor = connection.cursor()
    print(connection.get_dsn_parameters(), "\n")

    cursor.execute("SELECT version();")
    version_ps = cursor.fetchone()
    print("Вы подключены к - ", version_ps, "\n")

    #create_table(connection, cursor)
    #requests(connection)
    #select_data(cursor)
    #select_data1(connection, cursor)
    person_function(connection, cursor)
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()

