import psycopg2
import psycopg2.extras
import pandas as pd
from datetime import datetime


DB_CONFIG = {
    "dbname": "advertising_company",
    "user": "postgres",
    "password": "1lomalsteklo",
    "host": "localhost",
    "port": "5433"
}


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            return True, None
        except psycopg2.OperationalError as e:
            return False, str(e)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if self.cursor.description:
                rows = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                return True, columns, [list(row.values()) for row in rows]
            self.conn.commit()
            return True, [], []
        except Exception as e:
            self.conn.rollback()
            return False, [], str(e)

    def get_table_data(self, table_name):
        allowed = ["organizations", "agents", "ad_spots", "programs", "contracts", "contract_slots"]
        if table_name not in allowed:
            return False, [], "Недопустимое имя таблицы"
        return self.execute_query(f'SELECT * FROM {table_name} ORDER BY 1')

    def get_programs_data(self):
        return self.execute_query("SELECT * FROM programs ORDER BY 1")

    # ─── Процедуры ──────────────────────────────────────────────────────────────

    def get_total_ad_duration(self, org_name: str):
        try:
            self.cursor.execute("SELECT * FROM GetTotalAdDuration(%s)", (org_name,))
            rows = self.cursor.fetchall()
            if rows:
                columns = list(rows[0].keys())
                return True, columns, [list(r.values()) for r in rows]
            return True, ["result"], [["Нет данных"]]
        except Exception as e:
            self.conn.rollback()
            return False, [], str(e)

    def get_ads_count_by_time_range(self, start_time: str, end_time: str):
        try:
            self.cursor.execute(
                "SELECT * FROM GetAdsCountByTimeRange(%s::time, %s::time)",
                (start_time, end_time)
            )
            rows = self.cursor.fetchall()
            if rows:
                columns = list(rows[0].keys())
                return True, columns, [list(r.values()) for r in rows]
            return True, ["result"], [["Нет данных"]]
        except Exception as e:
            self.conn.rollback()
            return False, [], str(e)

    def get_avg_agent_salary(self, org_name: str):
        try:
            self.cursor.execute("SELECT * FROM GetAvgAgentSalary(%s)", (org_name,))
            rows = self.cursor.fetchall()
            if rows:
                columns = list(rows[0].keys())
                return True, columns, [list(r.values()) for r in rows]
            return True, ["result"], [["Нет данных"]]
        except Exception as e:
            self.conn.rollback()
            return False, [], str(e)

    # ─── Данные для графиков ─────────────────────────────────────────────────────

    def get_revenue_by_month(self):
        """Динамика доходов по месяцам (из contract_slots.slot_cost)"""
        query = """
            SELECT
                TO_CHAR(c.contract_date, 'YYYY-MM') AS month,
                SUM(cs.slot_cost) AS total_revenue
            FROM contract_slots cs
            JOIN contracts c ON cs.contract_id = c.contract_id
            GROUP BY TO_CHAR(c.contract_date, 'YYYY-MM')
            ORDER BY month
        """
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            months = [r["month"] for r in rows]
            revenue = [float(r["total_revenue"]) if r["total_revenue"] else 0 for r in rows]
            return months, revenue
        except Exception as e:
            self.conn.rollback()
            return [], []

    def get_contracts_by_agent(self):
        """Количество договоров по агентам"""
        query = """
            SELECT
                a.full_name AS agent,
                COUNT(c.contract_id) AS contracts_count
            FROM agents a
            LEFT JOIN contracts c ON a.agent_id = c.agent_id
            GROUP BY a.agent_id, a.full_name
            ORDER BY contracts_count DESC
            LIMIT 15
        """
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            agents = [r["agent"] for r in rows]
            counts = [int(r["contracts_count"]) for r in rows]
            return agents, counts
        except Exception as e:
            self.conn.rollback()
            return [], []

    def get_ad_slots_by_program(self):
        """Распределение рекламных размещений по передачам"""
        query = """
            SELECT
                p.program_name AS program,
                COUNT(cs.slot_id) AS slots_count
            FROM programs p
            LEFT JOIN ad_spots ads ON p.program_id = ads.program_id
            LEFT JOIN contract_slots cs ON ads.spot_id = cs.spot_id
            GROUP BY p.program_id, p.program_name
            HAVING COUNT(cs.slot_id) > 0
            ORDER BY slots_count DESC
            LIMIT 10
        """
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            programs = [r["program"] for r in rows]
            counts = [int(r["slots_count"]) for r in rows]
            return programs, counts
        except Exception as e:
            self.conn.rollback()
            return [], []