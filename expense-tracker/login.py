import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from database import connect_database

def login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        messagebox.showinfo("Success", "Login Successful!")

        window.destroy()

        # We'll create dashboard.py next
        subprocess.run([sys.executable, "dashboard.py"])

    else:
        messagebox.showerror("Error", "Invalid Username or Password!")


def open_register():
    subprocess.run([sys.executable, "register.py"])


# ---------------- Window ----------------
window = tk.Tk()
window.title("Expense Tracker - Login")
window.geometry("400x300")
window.resizable(False, False)

title = tk.Label(window, text="Expense Tracker", font=("Arial", 18, "bold"))
title.pack(pady=20)

tk.Label(window, text="Username").pack()
username_entry = tk.Entry(window, width=30)
username_entry.pack(pady=5)

tk.Label(window, text="Password").pack()
password_entry = tk.Entry(window, width=30, show="*")
password_entry.pack(pady=5)

login_btn = tk.Button(window, text="Login", width=15, command=login)
login_btn.pack(pady=10)

register_btn = tk.Button(window, text="Register", width=15, command=open_register)
register_btn.pack()

window.mainloop()
