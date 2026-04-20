# main.py
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import psycopg2
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_CONFIG = dict(dbname="advertising_company", user="postgres",
                 password="1lomalsteklo", host="localhost", port="5433")

ALL_TABLES    = ["organizations", "agents", "ad_spots", "programs", "contracts", "contract_slots"]
CUSTOMER_TABS = ["programs"]

ROLE_ACCESS = {
    "administrator": (True, True,  True),
    "director":      (True, False, True),
    "agent":         (False, True, False),
    "customer":      (True,  False, False),
}


def fill_tree(tree, columns, rows):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    tree["show"] = "headings"
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120, minwidth=60)
    for row in rows:
        tree.insert("", "end", values=[str(v) if v is not None else "" for v in row])


def make_tree(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=8, pady=4)
    tree = ttk.Treeview(frame, show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    return tree


class App:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.conn = None

        self.root.title(f"AdTV — {username} ({role})")
        self.root.geometry("1200x750")

        style = ttk.Style()
        style.theme_use("clam")
        acc = "#4a6fa5"
        hi  = "#6b8cae"
        style.configure(".",              background="#f4f4f4", foreground="#222")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"),
                        padding=(14, 5), background="#ddd")
        style.map("TNotebook.Tab",
                  background=[("selected", acc)], foreground=[("selected", "white")])
        style.configure("TButton",       font=("Segoe UI", 10),
                        background=acc, foreground="white", padding=5)
        style.map("TButton",             background=[("active", hi)])
        style.configure("Treeview",      background="white", fieldbackground="white",
                        rowheight=24,    font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                        background=acc, foreground="white")
        style.map("Treeview",            background=[("selected", hi)])

        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
        except Exception as e:
            messagebox.showerror("Ошибка подключения",
                                 f"Не удалось подключиться к базе данных:\n{e}")
            root.destroy()
            return

        hdr = tk.Frame(root, bg=acc, height=42)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  AdTV System  |  {username}  |  {role}",
                 bg=acc, fg="white", font=("Segoe UI", 11, "bold")).pack(side="left", pady=10, padx=10)

        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        has_t, has_p, has_a = ROLE_ACCESS.get(role, (False, False, False))
        if has_t: self._tab_tables(nb)
        if has_p: self._tab_procedures(nb)
        if has_a: self._tab_analytics(nb)

    def _q(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description:
                cols = [d[0] for d in cur.description]
                return cols, cur.fetchall()
            self.conn.commit()
            return [], []

    # ── Таблицы ──────────────────────────────────────────────────────────────

    def _tab_tables(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  Таблицы")

        ctrl = ttk.Frame(tab)
        ctrl.pack(fill="x", padx=8, pady=8)

        tables = CUSTOMER_TABS if self.role == "customer" else ALL_TABLES
        ttk.Label(ctrl, text="Таблица:").pack(side="left", padx=4)
        self.cmb_table = ttk.Combobox(ctrl, values=tables, state="readonly", width=22)
        self.cmb_table.current(0)
        self.cmb_table.pack(side="left", padx=4)
        ttk.Button(ctrl, text="Показать",   command=self._load_table).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Обновить",   command=self._load_table).pack(side="left", padx=4)

        self.tree_tables = make_tree(tab)
        self._load_table()

    def _load_table(self):
        try:
            cols, rows = self._q(f"SELECT * FROM {self.cmb_table.get()} ORDER BY 1")
            fill_tree(self.tree_tables, cols, rows)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ── Процедуры ────────────────────────────────────────────────────────────

    def _tab_procedures(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  Процедуры")

        g1 = ttk.LabelFrame(tab, text="GetTotalAdDuration — суммарная длительность рекламы", padding=8)
        g1.pack(fill="x", padx=8, pady=6)
        r1 = ttk.Frame(g1)
        r1.pack(fill="x")
        ttk.Label(r1, text="Организация:").pack(side="left")
        self.e_dur = ttk.Entry(r1, width=28); self.e_dur.pack(side="left", padx=6)
        ttk.Button(r1, text="Выполнить", command=self._run_dur).pack(side="left")
        self.tree_dur = make_tree(g1)
        self.tree_dur.master.configure(height=90)

        g2 = ttk.LabelFrame(tab, text="GetAdsCountByTimeRange — количество реклам по диапазону времени", padding=8)
        g2.pack(fill="x", padx=8, pady=6)
        r2 = ttk.Frame(g2)
        r2.pack(fill="x")
        ttk.Label(r2, text="Начало (ЧЧ:ММ):").pack(side="left")
        self.e_ts = ttk.Entry(r2, width=8); self.e_ts.pack(side="left", padx=4)
        ttk.Label(r2, text="Конец (ЧЧ:ММ):").pack(side="left", padx=(8, 0))
        self.e_te = ttk.Entry(r2, width=8); self.e_te.pack(side="left", padx=4)
        ttk.Button(r2, text="Выполнить", command=self._run_time).pack(side="left", padx=6)
        self.tree_time = make_tree(g2)
        self.tree_time.master.configure(height=90)

        g3 = ttk.LabelFrame(tab, text="GetAvgAgentSalary — средняя зарплата агентов", padding=8)
        g3.pack(fill="x", padx=8, pady=6)
        r3 = ttk.Frame(g3)
        r3.pack(fill="x")
        ttk.Label(r3, text="Организация:").pack(side="left")
        self.e_sal = ttk.Entry(r3, width=28); self.e_sal.pack(side="left", padx=6)
        ttk.Button(r3, text="Выполнить", command=self._run_sal).pack(side="left")
        self.tree_sal = make_tree(g3)
        self.tree_sal.master.configure(height=90)

    def _run_dur(self):
        org = self.e_dur.get().strip()
        if not org:
            messagebox.showwarning("Пустое поле", "Введите название организации"); return
        try:
            cols, rows = self._q("SELECT * FROM GetTotalAdDuration(%s)", (org,))
            fill_tree(self.tree_dur, cols, rows)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _run_time(self):
        s, e = self.e_ts.get().strip(), self.e_te.get().strip()
        if not s or not e:
            messagebox.showwarning("Пустое поле", "Заполните оба поля времени"); return
        for v in (s, e):
            try: datetime.strptime(v, "%H:%M")
            except ValueError:
                messagebox.showerror("Неверный формат", f"'{v}' — ожидается ЧЧ:ММ"); return
        try:
            cols, rows = self._q(
                "SELECT * FROM GetAdsCountByTimeRange(%s::time, %s::time)", (s, e))
            fill_tree(self.tree_time, cols, rows)
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))

    def _run_sal(self):
        org = self.e_sal.get().strip()
        if not org:
            messagebox.showwarning("Пустое поле", "Введите название организации"); return
        try:
            cols, rows = self._q("SELECT * FROM GetAvgAgentSalary(%s)", (org,))
            fill_tree(self.tree_sal, cols, rows)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ── Аналитика ─────────────────────────────────────────────────────────────

    def _tab_analytics(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="  Аналитика")

        ctrl = ttk.Frame(tab)
        ctrl.pack(fill="x", padx=8, pady=8)
        charts = ["Динамика доходов по месяцам",
                  "Количество договоров по агентам",
                  "Распределение размещений по передачам"]
        ttk.Label(ctrl, text="График:").pack(side="left", padx=4)
        self.cmb_chart = ttk.Combobox(ctrl, values=charts, state="readonly", width=36)
        self.cmb_chart.current(0)
        self.cmb_chart.pack(side="left", padx=4)
        self.cmb_chart.bind("<<ComboboxSelected>>", self._draw)
        ttk.Button(ctrl, text="Обновить", command=self._draw).pack(side="left", padx=4)

        self.chart_frame = ttk.Frame(tab)
        self.chart_frame.pack(fill="both", expand=True, padx=8, pady=4)
        self._draw()

    def _draw(self, event=None):
        for w in self.chart_frame.winfo_children():
            w.destroy()
        ch = self.cmb_chart.get()
        if ch == "Динамика доходов по месяцам":       self._c_revenue()
        elif ch == "Количество договоров по агентам": self._c_contracts()
        else:                                          self._c_pie()

    def _embed(self, fig):
        FigureCanvasTkAgg(fig, master=self.chart_frame).get_tk_widget().pack(fill="both", expand=True)

    def _c_revenue(self):
        try:
            _, rows = self._q("""
                SELECT TO_CHAR(c.contract_date,'YYYY-MM'), SUM(cs.slot_cost)
                FROM contract_slots cs
                JOIN contracts c ON cs.contract_id = c.contract_id
                GROUP BY 1 ORDER BY 1
            """)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); return
        months  = [r[0] for r in rows]
        revenue = [float(r[1]) if r[1] else 0 for r in rows]
        fig = Figure(figsize=(9, 4), dpi=96)
        ax  = fig.add_subplot(111)
        if months:
            ax.plot(range(len(months)), revenue, color="#4a6fa5", marker="o", linewidth=2)
            ax.fill_between(range(len(months)), revenue, alpha=0.12, color="#4a6fa5")
            ax.set_xticks(range(len(months)))
            ax.set_xticklabels(months, rotation=45, ha="right", fontsize=8)
        ax.set_title("Динамика доходов по месяцам")
        ax.set_ylabel("Сумма (руб.)")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        fig.tight_layout()
        self._embed(fig)

    def _c_contracts(self):
        try:
            _, rows = self._q("""
                SELECT a.full_name, COUNT(c.contract_id)
                FROM agents a
                LEFT JOIN contracts c ON a.agent_id = c.agent_id
                GROUP BY a.agent_id, a.full_name
                ORDER BY 2 DESC LIMIT 15
            """)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); return
        names  = [r[0].split()[-1] if r[0] else "?" for r in rows]
        counts = [int(r[1]) for r in rows]
        fig = Figure(figsize=(9, 4), dpi=96)
        ax  = fig.add_subplot(111)
        if names:
            bars = ax.bar(range(len(names)), counts, color="#4a6fa5", width=0.6)
            for bar, val in zip(bars, counts):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(val), ha="center", va="bottom", fontsize=8)
            ax.set_xticks(range(len(names)))
            ax.set_xticklabels(names, rotation=35, ha="right", fontsize=8)
        ax.set_title("Количество договоров по агентам")
        ax.set_ylabel("Договоры")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        fig.tight_layout()
        self._embed(fig)

    def _c_pie(self):
        try:
            _, rows = self._q("""
                SELECT p.program_name, COUNT(cs.slot_id)
                FROM programs p
                LEFT JOIN ad_spots ads ON p.program_id = ads.program_id
                LEFT JOIN contract_slots cs ON ads.spot_id = cs.spot_id
                GROUP BY p.program_id, p.program_name
                HAVING COUNT(cs.slot_id) > 0
                ORDER BY 2 DESC LIMIT 10
            """)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); return
        labels = [r[0] for r in rows]
        values = [int(r[1]) for r in rows]
        fig = Figure(figsize=(9, 4), dpi=96)
        ax  = fig.add_subplot(111)
        if labels:
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("Распределение рекламных размещений по передачам")
        fig.tight_layout()
        self._embed(fig)


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "user"
    role     = sys.argv[2] if len(sys.argv) > 2 else "administrator"
    root = tk.Tk()
    App(root, username, role)
    root.mainloop()