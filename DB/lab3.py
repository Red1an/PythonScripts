import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker




connection = psycopg2.connect(
    database="students",
    user="postgres",
    password="1lomalsteklo",
    host="127.0.0.1",
    port="5433"
)




df1 = pd.read_sql_query("""
    SELECT d.department_name, COUNT(e.employee_id) AS emp_count
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.department_name
    ORDER BY emp_count DESC
""", connection)

plt.figure(figsize=(12, 6))
plt.bar(df1['department_name'], df1['emp_count'],
        color='steelblue', edgecolor='black')

plt.xlabel('Название отдела')
plt.ylabel('Количество сотрудников')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graph1.png')
plt.show()




df2 = pd.read_sql_query("""
    SELECT
        CASE
            WHEN j.job_title ILIKE '%Manager%'   THEN 'Manager'
            WHEN j.job_title ILIKE '%Clerk%'     THEN 'Clerk'
            WHEN j.job_title ILIKE '%President%' THEN 'President'
            ELSE 'Other'
        END AS job_group,
        AVG(e.salary) AS avg_salary
    FROM employees e
    JOIN jobs j ON e.job_id = j.job_id
    GROUP BY job_group
    ORDER BY avg_salary DESC
""", connection)

plt.figure(figsize=(8, 5))

plt.bar(df2['job_group'], df2['avg_salary'],
        color=colors[:len(df2)], edgecolor='black')

plt.xlabel('Должность')
plt.ylabel('Средняя зарплата')
plt.tight_layout()
plt.savefig('graph2.png')
plt.show()





df3 = pd.read_sql_query("""
    SELECT d.department_name, COUNT(e.employee_id) AS emp_count
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.department_name
    HAVING COUNT(e.employee_id) BETWEEN 3 AND 10
    ORDER BY emp_count DESC
""", connection)

plt.figure(figsize=(10, 6))
plt.barh(df3['department_name'], df3['emp_count'],
         color='coral', edgecolor='black')
plt.title('Отделы с числом сотрудников от 3 до 10 (горизонтальная)')
plt.xlabel('Количество сотрудников')
plt.ylabel('Название отдела')
plt.tight_layout()
plt.savefig('graph3.png')
plt.show()





df4 = pd.read_sql_query("""
    SELECT
        CASE
            WHEN j.job_title ILIKE '%Manager%'   THEN 'Manager'
            WHEN j.job_title ILIKE '%Clerk%'     THEN 'Clerk'
            WHEN j.job_title ILIKE '%President%' THEN 'President'
            ELSE 'Other'
        END AS job_group,
        AVG(e.salary) AS avg_salary
    FROM employees e
    JOIN jobs j ON e.job_id = j.job_id
    GROUP BY job_group
    HAVING AVG(e.salary) BETWEEN 5000 AND 12000
    ORDER BY avg_salary DESC
""", connection)

plt.figure(figsize=(8, 5))
plt.barh(df4['job_group'], df4['avg_salary'],
         color='mediumseagreen', edgecolor='black')

plt.xlabel('Средняя зарплата')
plt.ylabel('Должность')
plt.tight_layout()
plt.savefig('graph4.png')
plt.show()





df5 = pd.read_sql_query("""
    SELECT l.city, COUNT(e.employee_id) AS emp_count
    FROM employees e
    JOIN locations l ON e.location_id = l.location_id
    GROUP BY l.city
    ORDER BY emp_count DESC
""", connection)

plt.figure(figsize=(10, 5))
plt.bar(df5['city'], df5['emp_count'],
        color='mediumpurple', edgecolor='black')

plt.xlabel('Город')
plt.ylabel('Количество сотрудников')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('graph5_locations.png')
plt.show()






def plot_filtered(emp_min: int, emp_max: int,
                  salary_min: float, salary_max: float):
    """
    Строит два горизонтальных графика:
      - отделы, где количество сотрудников в [emp_min, emp_max]
      - группы должностей, где средняя зарплата в [salary_min, salary_max]
    """

    dfA = pd.read_sql_query(f"""
        SELECT d.department_name, COUNT(e.employee_id) AS emp_count
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        GROUP BY d.department_name
        HAVING COUNT(e.employee_id) BETWEEN {emp_min} AND {emp_max}
        ORDER BY emp_count DESC
    """, connection)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    if dfA.empty:
        axes[0].text(0.5, 0.5, 'Нет данных', ha='center', va='center')
    else:
        axes[0].barh(dfA['department_name'], dfA['emp_count'],
                     color='tomato', edgecolor='black')
        axes[0].set_title(f'Отделы: сотрудников от {emp_min} до {emp_max}')
        axes[0].set_xlabel('Количество сотрудников')
        axes[0].set_ylabel('Отдел')


    dfB = pd.read_sql_query(f"""
        SELECT
            CASE
                WHEN j.job_title ILIKE '%Manager%'   THEN 'Manager'
                WHEN j.job_title ILIKE '%Clerk%'     THEN 'Clerk'
                WHEN j.job_title ILIKE '%President%' THEN 'President'
                ELSE 'Other'
            END AS job_group,
            AVG(e.salary) AS avg_salary
        FROM employees e
        JOIN jobs j ON e.job_id = j.job_id
        GROUP BY job_group
        HAVING AVG(e.salary) BETWEEN {salary_min} AND {salary_max}
        ORDER BY avg_salary DESC
    """, connection)

    if dfB.empty:
        axes[1].text(0.5, 0.5, 'Нет данных', ha='center', va='center')
    else:
        axes[1].barh(dfB['job_group'], dfB['avg_salary'],
                     color='cornflowerblue', edgecolor='black')
        axes[1].set_title(
            f'Группы должностей: ср. зп от {salary_min} до {salary_max}')
        axes[1].set_xlabel('Средняя зарплата')
        axes[1].set_ylabel('Должность')

    plt.tight_layout()
    plt.savefig(f'graph_func_{emp_min}_{emp_max}.png')
    plt.show()



plot_filtered(emp_min=2, emp_max=8, salary_min=4000, salary_max=15000)


connection.close()