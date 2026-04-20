import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

from database import Database
from ui import LoginDialog, MainWindow, STYLESHEET


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    # ── Подключение к БД ──────────────────────────────────────────────────────
    db = Database()
    ok, err = db.connect()
    if not ok:
        QMessageBox.critical(
            None,
            "Ошибка подключения",
            f"Не удалось подключиться к базе данных PostgreSQL.\n\n"
            f"Убедитесь, что сервер запущен и параметры верны:\n"
            f"  host=localhost  port=5432\n"
            f"  dbname=advertising_company  user=postgres\n\n"
            f"Детали: {err}"
        )
        sys.exit(1)

    # ── Авторизация ───────────────────────────────────────────────────────────
    login_dlg = LoginDialog(db)
    if login_dlg.exec() != LoginDialog.DialogCode.Accepted:
        db.disconnect()
        sys.exit(0)

    username = login_dlg.username
    role = login_dlg.role

    # ── Главное окно ──────────────────────────────────────────────────────────
    window = MainWindow(db, username, role)
    window.show()

    exit_code = app.exec()
    db.disconnect()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()