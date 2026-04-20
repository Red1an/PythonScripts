from PyQt6.QtWidgets import (
    QDialog, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QMessageBox, QGroupBox,
    QFormLayout, QSplitter, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush, QLinearGradient

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from database import Database


# ─── Цветовая схема ───────────────────────────────────────────────────────────

DARK_BG      = "#0f1117"
PANEL_BG     = "#181c27"
CARD_BG      = "#1e2333"
ACCENT       = "#4f8ef7"
ACCENT2      = "#7c5cbf"
SUCCESS      = "#3ecf8e"
WARNING      = "#f5a623"
DANGER       = "#e05c5c"
TEXT_PRIMARY = "#e8ecf4"
TEXT_MUTED   = "#7a8299"
BORDER       = "#2a2f42"

STYLESHEET = f"""
QMainWindow, QDialog {{
    background-color: {DARK_BG};
}}
QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
    font-size: 13px;
}}
QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    background-color: {PANEL_BG};
    top: -1px;
}}
QTabBar::tab {{
    background-color: {CARD_BG};
    color: {TEXT_MUTED};
    padding: 10px 24px;
    border: 1px solid {BORDER};
    border-bottom: none;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    margin-right: 3px;
    font-weight: 600;
    font-size: 13px;
}}
QTabBar::tab:selected {{
    background-color: {ACCENT};
    color: #ffffff;
    border-color: {ACCENT};
}}
QTabBar::tab:hover:!selected {{
    background-color: #252b3b;
    color: {TEXT_PRIMARY};
}}
QPushButton {{
    background-color: {ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 7px;
    padding: 9px 22px;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.3px;
}}
QPushButton:hover {{
    background-color: #6ba0ff;
}}
QPushButton:pressed {{
    background-color: #3a70d4;
}}
QPushButton#secondary {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
}}
QPushButton#secondary:hover {{
    background-color: #252b3b;
    border-color: {ACCENT};
}}
QPushButton#danger {{
    background-color: {DANGER};
}}
QPushButton#danger:hover {{
    background-color: #f07070;
}}
QLineEdit {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 9px 14px;
    font-size: 13px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus {{
    border-color: {ACCENT};
    background-color: #222840;
}}
QComboBox {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 9px 14px;
    font-size: 13px;
    min-width: 160px;
}}
QComboBox:focus {{
    border-color: {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {TEXT_MUTED};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    selection-background-color: {ACCENT};
    outline: none;
}}
QTableWidget {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
    gridline-color: {BORDER};
    selection-background-color: #2a3a6e;
    alternate-background-color: #1a1f2e;
    font-size: 12px;
}}
QTableWidget::item {{
    padding: 6px 10px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: #2a3a6e;
    color: {TEXT_PRIMARY};
}}
QHeaderView::section {{
    background-color: {CARD_BG};
    color: {ACCENT};
    padding: 9px 12px;
    border: none;
    border-bottom: 2px solid {ACCENT};
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 9px;
    margin-top: 14px;
    padding: 10px;
    background-color: {CARD_BG};
    font-weight: 700;
    color: {TEXT_MUTED};
    font-size: 12px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    left: 14px;
    top: -1px;
}}
QLabel {{
    color: {TEXT_PRIMARY};
    background: transparent;
}}
QLabel#muted {{
    color: {TEXT_MUTED};
    font-size: 12px;
}}
QLabel#title {{
    color: {TEXT_PRIMARY};
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
}}
QLabel#subtitle {{
    color: {TEXT_MUTED};
    font-size: 13px;
}}
QScrollBar:vertical {{
    background: {PANEL_BG};
    width: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {PANEL_BG};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""


# ─── Вспомогательные функции ──────────────────────────────────────────────────

def fill_table(widget: QTableWidget, columns: list, rows: list):
    widget.setRowCount(0)
    widget.setColumnCount(0)
    if not columns:
        return
    widget.setColumnCount(len(columns))
    widget.setHorizontalHeaderLabels([str(c).upper() for c in columns])
    widget.setRowCount(len(rows))
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            item = QTableWidgetItem(str(val) if val is not None else "")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            widget.setItem(r_idx, c_idx, item)
    widget.resizeColumnsToContents()
    widget.horizontalHeader().setStretchLastSection(True)
    widget.setAlternatingRowColors(True)


def make_card(title: str, widget: QWidget) -> QGroupBox:
    box = QGroupBox(title)
    layout = QVBoxLayout(box)
    layout.setContentsMargins(10, 14, 10, 10)
    layout.addWidget(widget)
    return box


def section_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase; background:transparent;")
    return lbl


# ─── Виджет Matplotlib ────────────────────────────────────────────────────────

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 4), dpi=96)
        self.fig.patch.set_facecolor(PANEL_BG)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.updateGeometry()

    def clear(self):
        self.fig.clear()
        self.draw()


# ─── Окно авторизации ─────────────────────────────────────────────────────────

class LoginDialog(QDialog):
    ROLES = ["administrator", "director", "agent", "customer"]

    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.role = None
        self.username = None
        self._build_ui()
        self.setStyleSheet(STYLESHEET)
        self.setFixedSize(420, 480)

    def _build_ui(self):
        self.setWindowTitle("Вход в систему")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        root = QVBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(0)

        # Логотип / заголовок
        logo = QLabel("📺")
        logo.setStyleSheet("font-size: 48px; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(logo)

        title = QLabel("AdTV System")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size:26px; font-weight:800; color:{TEXT_PRIMARY}; background:transparent; margin-bottom:4px;")
        root.addWidget(title)

        sub = QLabel("Информационная система рекламной компании")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px; background:transparent; margin-bottom:28px;")
        root.addWidget(sub)

        # Форма
        form = QWidget()
        form.setStyleSheet(f"background:{CARD_BG}; border-radius:12px;")
        fl = QVBoxLayout(form)
        fl.setContentsMargins(24, 24, 24, 24)
        fl.setSpacing(14)

        fl.addWidget(section_label("Логин"))
        self.inp_login = QLineEdit()
        self.inp_login.setPlaceholderText("Введите ваш логин")
        fl.addWidget(self.inp_login)

        fl.addWidget(section_label("Роль"))
        self.cmb_role = QComboBox()
        self.cmb_role.addItems(self.ROLES)
        fl.addWidget(self.cmb_role)

        root.addWidget(form)
        root.addSpacing(20)

        self.btn_login = QPushButton("  Войти в систему")
        self.btn_login.setFixedHeight(46)
        self.btn_login.clicked.connect(self._try_login)
        root.addWidget(self.btn_login)

        self.lbl_error = QLabel("")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setStyleSheet(f"color:{DANGER}; font-size:12px; background:transparent;")
        root.addWidget(self.lbl_error)

        root.addStretch()

        self.inp_login.returnPressed.connect(self._try_login)

    def _try_login(self):
        login = self.inp_login.text().strip()
        if not login:
            self.lbl_error.setText("Введите логин")
            return
        self.username = login
        self.role = self.cmb_role.currentText()
        self.accept()


# ─── Вкладка «Таблицы» ────────────────────────────────────────────────────────

class TablesTab(QWidget):
    TABLES = ["organizations", "agents", "ad_spots", "programs", "contracts", "contract_slots"]
    PROGRAMS_ONLY = ["programs"]

    def __init__(self, db: Database, role: str):
        super().__init__()
        self.db = db
        self.role = role
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Верхняя панель управления
        ctrl = QHBoxLayout()
        ctrl.setSpacing(10)

        ctrl.addWidget(section_label("Таблица:"))

        self.cmb_table = QComboBox()
        tables = self.PROGRAMS_ONLY if self.role == "customer" else self.TABLES
        self.cmb_table.addItems(tables)
        ctrl.addWidget(self.cmb_table)

        ctrl.addStretch()

        btn_refresh = QPushButton("↻  Обновить данные")
        btn_refresh.clicked.connect(self.load_table)
        ctrl.addWidget(btn_refresh)

        layout.addLayout(ctrl)

        # Таблица
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("muted")
        layout.addWidget(self.lbl_status)

        # Загрузить сразу
        self.load_table()

    def load_table(self):
        name = self.cmb_table.currentText()
        ok, cols, rows = self.db.get_table_data(name)
        if ok:
            fill_table(self.table, cols, rows)
            self.lbl_status.setText(f"Загружено строк: {len(rows)}")
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить таблицу:\n{rows}")


# ─── Вкладка «Процедуры» ─────────────────────────────────────────────────────

class ProceduresTab(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        main = QVBoxLayout(container)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(18)

        # ─ GetTotalAdDuration ─────────────────────────────────────────────────
        grp1 = QGroupBox("GetTotalAdDuration — суммарная длительность рекламы")
        g1 = QVBoxLayout(grp1)
        g1.setSpacing(10)

        f1 = QFormLayout()
        f1.setSpacing(8)
        self.inp_dur_org = QLineEdit()
        self.inp_dur_org.setPlaceholderText("Название организации")
        f1.addRow(section_label("Организация:"), self.inp_dur_org)
        g1.addLayout(f1)

        btn1 = QPushButton("▶  Выполнить")
        btn1.clicked.connect(self._run_total_duration)
        g1.addWidget(btn1)

        self.tbl_dur = QTableWidget()
        self.tbl_dur.setFixedHeight(140)
        g1.addWidget(self.tbl_dur)

        main.addWidget(grp1)

        # ─ GetAdsCountByTimeRange ─────────────────────────────────────────────
        grp2 = QGroupBox("GetAdsCountByTimeRange — количество реклам по временному диапазону")
        g2 = QVBoxLayout(grp2)
        g2.setSpacing(10)

        f2 = QFormLayout()
        f2.setSpacing(8)
        self.inp_time_start = QLineEdit()
        self.inp_time_start.setPlaceholderText("ЧЧ:ММ  (напр. 09:00)")
        self.inp_time_end = QLineEdit()
        self.inp_time_end.setPlaceholderText("ЧЧ:ММ  (напр. 21:00)")
        f2.addRow(section_label("Начало:"), self.inp_time_start)
        f2.addRow(section_label("Конец:"), self.inp_time_end)
        g2.addLayout(f2)

        btn2 = QPushButton("▶  Выполнить")
        btn2.clicked.connect(self._run_time_range)
        g2.addWidget(btn2)

        self.tbl_time = QTableWidget()
        self.tbl_time.setFixedHeight(140)
        g2.addWidget(self.tbl_time)

        main.addWidget(grp2)

        # ─ GetAvgAgentSalary ──────────────────────────────────────────────────
        grp3 = QGroupBox("GetAvgAgentSalary — средняя зарплата агентов")
        g3 = QVBoxLayout(grp3)
        g3.setSpacing(10)

        f3 = QFormLayout()
        f3.setSpacing(8)
        self.inp_sal_org = QLineEdit()
        self.inp_sal_org.setPlaceholderText("Название организации")
        f3.addRow(section_label("Организация:"), self.inp_sal_org)
        g3.addLayout(f3)

        btn3 = QPushButton("▶  Выполнить")
        btn3.clicked.connect(self._run_avg_salary)
        g3.addWidget(btn3)

        self.tbl_sal = QTableWidget()
        self.tbl_sal.setFixedHeight(140)
        g3.addWidget(self.tbl_sal)

        main.addWidget(grp3)
        main.addStretch()

        scroll.setWidget(container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    # ── Обработчики ──────────────────────────────────────────────────────────

    def _validate_nonempty(self, value: str, field: str) -> bool:
        if not value.strip():
            QMessageBox.warning(self, "Пустое поле", f"Поле «{field}» не может быть пустым.")
            return False
        return True

    def _validate_time(self, value: str) -> bool:
        from datetime import datetime
        try:
            datetime.strptime(value.strip(), "%H:%M")
            return True
        except ValueError:
            QMessageBox.warning(self, "Неверный формат", f"Время '{value}' не соответствует формату ЧЧ:ММ")
            return False

    def _run_total_duration(self):
        org = self.inp_dur_org.text()
        if not self._validate_nonempty(org, "Организация"):
            return
        ok, cols, rows = self.db.get_total_ad_duration(org.strip())
        if ok:
            fill_table(self.tbl_dur, cols, rows)
        else:
            QMessageBox.critical(self, "Ошибка процедуры", str(rows))

    def _run_time_range(self):
        start = self.inp_time_start.text()
        end = self.inp_time_end.text()
        if not self._validate_nonempty(start, "Начало"):
            return
        if not self._validate_nonempty(end, "Конец"):
            return
        if not self._validate_time(start):
            return
        if not self._validate_time(end):
            return
        ok, cols, rows = self.db.get_ads_count_by_time_range(start.strip(), end.strip())
        if ok:
            fill_table(self.tbl_time, cols, rows)
        else:
            QMessageBox.critical(self, "Ошибка процедуры", str(rows))

    def _run_avg_salary(self):
        org = self.inp_sal_org.text()
        if not self._validate_nonempty(org, "Организация"):
            return
        ok, cols, rows = self.db.get_avg_agent_salary(org.strip())
        if ok:
            fill_table(self.tbl_sal, cols, rows)
        else:
            QMessageBox.critical(self, "Ошибка процедуры", str(rows))


# ─── Вкладка «Аналитика» ─────────────────────────────────────────────────────

class AnalyticsTab(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._build_ui()
        self._load_charts()

    def _mpl_style(self, ax, title: str):
        ax.set_facecolor(CARD_BG)
        ax.set_title(title, color=TEXT_PRIMARY, fontsize=13, fontweight="bold", pad=12)
        ax.tick_params(colors=TEXT_MUTED, labelsize=10)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.title.set_fontfamily("DejaVu Sans")

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Кнопка обновить
        top = QHBoxLayout()
        top.addStretch()
        btn = QPushButton("↻  Обновить графики")
        btn.clicked.connect(self._load_charts)
        top.addWidget(btn)
        layout.addLayout(top)

        # График 1
        grp1 = QGroupBox("Динамика доходов по месяцам")
        g1l = QVBoxLayout(grp1)
        self.canvas1 = MplCanvas()
        g1l.addWidget(self.canvas1)
        layout.addWidget(grp1)

        # График 2
        grp2 = QGroupBox("Количество договоров по агентам")
        g2l = QVBoxLayout(grp2)
        self.canvas2 = MplCanvas()
        g2l.addWidget(self.canvas2)
        layout.addWidget(grp2)

        # График 3
        grp3 = QGroupBox("Распределение рекламных размещений по передачам")
        g3l = QVBoxLayout(grp3)
        self.canvas3 = MplCanvas()
        g3l.addWidget(self.canvas3)
        layout.addWidget(grp3)

        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _load_charts(self):
        self._draw_revenue()
        self._draw_contracts()
        self._draw_pie()

    # ── График 1: Линейный — доходы по месяцам ───────────────────────────────
    def _draw_revenue(self):
        months, revenue = self.db.get_revenue_by_month()
        self.canvas1.fig.clear()
        ax = self.canvas1.fig.add_subplot(111)
        self._mpl_style(ax, "")

        if months and revenue:
            x = range(len(months))
            ax.plot(x, revenue, color=ACCENT, linewidth=2.5, marker="o",
                    markersize=6, markerfacecolor=ACCENT2, markeredgecolor="white",
                    markeredgewidth=1.5, zorder=3)
            ax.fill_between(x, revenue, alpha=0.15, color=ACCENT)
            ax.set_xticks(list(x))
            ax.set_xticklabels(months, rotation=45, ha="right", color=TEXT_MUTED, fontsize=9)
            ax.set_ylabel("Доход (руб.)", color=TEXT_MUTED, fontsize=11)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
            ax.yaxis.label.set_color(TEXT_MUTED)
            ax.grid(axis="y", color=BORDER, linewidth=0.7, linestyle="--", alpha=0.7)
        else:
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    color=TEXT_MUTED, fontsize=14, transform=ax.transAxes)

        self.canvas1.fig.tight_layout(pad=1.5)
        self.canvas1.draw()

    # ── График 2: Столбчатый — договоры по агентам ───────────────────────────
    def _draw_contracts(self):
        agents, counts = self.db.get_contracts_by_agent()
        self.canvas2.fig.clear()
        ax = self.canvas2.fig.add_subplot(111)
        self._mpl_style(ax, "")

        if agents and counts:
            colors = [ACCENT if i % 2 == 0 else ACCENT2 for i in range(len(agents))]
            bars = ax.bar(range(len(agents)), counts, color=colors, width=0.6,
                          edgecolor="none", zorder=2)
            for bar, count in zip(bars, counts):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                        str(count), ha="center", va="bottom",
                        color=TEXT_PRIMARY, fontsize=9, fontweight="bold")
            ax.set_xticks(range(len(agents)))
            short_names = [n.split()[-1] if " " in n else n[:12] for n in agents]
            ax.set_xticklabels(short_names, rotation=35, ha="right",
                               color=TEXT_MUTED, fontsize=9)
            ax.set_ylabel("Кол-во договоров", color=TEXT_MUTED, fontsize=11)
            ax.yaxis.label.set_color(TEXT_MUTED)
            ax.grid(axis="y", color=BORDER, linewidth=0.7, linestyle="--", alpha=0.7)
            ax.set_ylim(0, max(counts) * 1.2 if counts else 5)
        else:
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    color=TEXT_MUTED, fontsize=14, transform=ax.transAxes)

        self.canvas2.fig.tight_layout(pad=1.5)
        self.canvas2.draw()

    # ── График 3: Круговой — размещения по передачам ─────────────────────────
    def _draw_pie(self):
        programs, counts = self.db.get_ad_slots_by_program()
        self.canvas3.fig.clear()
        ax = self.canvas3.fig.add_subplot(111)
        self._mpl_style(ax, "")

        if programs and counts:
            palette = [ACCENT, ACCENT2, SUCCESS, WARNING, DANGER,
                       "#56cfe1", "#ff9f1c", "#a8dadc", "#e63946", "#6a4c93"]
            colors = (palette * ((len(programs) // len(palette)) + 1))[:len(programs)]
            wedges, texts, autotexts = ax.pie(
                counts, labels=None, colors=colors,
                autopct="%1.1f%%", pctdistance=0.8,
                startangle=140, wedgeprops=dict(edgecolor=PANEL_BG, linewidth=2)
            )
            for at in autotexts:
                at.set_color("white")
                at.set_fontsize(9)
                at.set_fontweight("bold")
            ax.legend(
                wedges, programs, loc="center left",
                bbox_to_anchor=(1.02, 0.5),
                fontsize=9, labelcolor=TEXT_PRIMARY,
                framealpha=0, borderpad=0.5
            )
        else:
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    color=TEXT_MUTED, fontsize=14, transform=ax.transAxes)

        self.canvas3.fig.tight_layout(pad=1.5)
        self.canvas3.draw()


# ─── Главное окно ─────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    ROLE_TABS = {
        "administrator": {"tables": True, "procedures": True, "analytics": True},
        "director":      {"tables": True, "procedures": False, "analytics": True},
        "agent":         {"tables": False, "procedures": True, "analytics": False},
        "customer":      {"tables": True, "procedures": False, "analytics": False},
    }

    def __init__(self, db: Database, username: str, role: str):
        super().__init__()
        self.db = db
        self.username = username
        self.role = role
        self._build_ui()
        self.setStyleSheet(STYLESHEET)
        self.setMinimumSize(1100, 700)

    def _build_ui(self):
        self.setWindowTitle("AdTV — Информационная система рекламной компании")

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Шапка ──────────────────────────────────────────────────────────────
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet(f"background:{PANEL_BG}; border-bottom:1px solid {BORDER};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)

        logo = QLabel("📺  AdTV System")
        logo.setStyleSheet(f"font-size:17px; font-weight:800; color:{TEXT_PRIMARY}; background:transparent; letter-spacing:-0.3px;")
        hl.addWidget(logo)
        hl.addStretch()

        role_badge = QLabel(self.role.upper())
        role_badge.setStyleSheet(
            f"background:{ACCENT2}; color:white; padding:4px 12px; border-radius:5px; "
            f"font-size:11px; font-weight:700; letter-spacing:1px;"
        )
        hl.addWidget(role_badge)

        user_lbl = QLabel(f"  {self.username}")
        user_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:13px; background:transparent;")
        hl.addWidget(user_lbl)

        root.addWidget(header)

        # ── Вкладки ────────────────────────────────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background:{DARK_BG};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(16, 16, 16, 16)

        self.tabs = QTabWidget()
        permissions = self.ROLE_TABS.get(self.role, {})

        if permissions.get("tables"):
            self.tab_tables = TablesTab(self.db, self.role)
            self.tabs.addTab(self.tab_tables, "🗂  Таблицы")

        if permissions.get("procedures"):
            self.tab_procs = ProceduresTab(self.db)
            self.tabs.addTab(self.tab_procs, "⚙  Процедуры")

        if permissions.get("analytics"):
            self.tab_analytics = AnalyticsTab(self.db)
            self.tabs.addTab(self.tab_analytics, "📊  Аналитика")

        if self.tabs.count() == 0:
            placeholder = QLabel("Нет доступных разделов для вашей роли.")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet(f"color:{TEXT_MUTED}; font-size:15px;")
            bl.addWidget(placeholder)
        else:
            bl.addWidget(self.tabs)

        root.addWidget(body)

        # ── Статусная строка ───────────────────────────────────────────────────
        statusbar = self.statusBar()
        statusbar.setStyleSheet(f"background:{PANEL_BG}; color:{TEXT_MUTED}; border-top:1px solid {BORDER}; font-size:11px;")
        statusbar.showMessage(f"Подключено к advertising_company · Пользователь: {self.username} · Роль: {self.role}")