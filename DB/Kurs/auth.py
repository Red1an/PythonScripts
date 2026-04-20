# auth.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys


ROLES = ["administrator", "director", "agent", "customer"]


def do_login():
    username = entry_login.get().strip()
    role = combo_role.get()

    if not username:
        messagebox.showwarning("Внимание", "Введите логин")
        return

    root.destroy()
    subprocess.Popen([sys.executable, "main.py", username, role])


root = tk.Tk()
root.title("Авторизация — AdTV")
root.geometry("320x220")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Логин:").grid(row=0, column=0, sticky="w", pady=5)
entry_login = ttk.Entry(frame, width=25)
entry_login.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(frame, text="Роль:").grid(row=1, column=0, sticky="w", pady=5)
combo_role = ttk.Combobox(frame, values=ROLES, state="readonly", width=22)
combo_role.current(0)
combo_role.grid(row=1, column=1, pady=5, padx=5)

ttk.Button(frame, text="Войти", command=do_login).grid(
    row=2, column=0, columnspan=2, pady=15, ipadx=10
)

entry_login.bind("<Return>", lambda e: do_login())
root.mainloop()