import tkinter as tk
from tkinter import messagebox
from database import connect_database

def register():
    username = username_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_entry.get()

    # Check if all fields are filled
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        connection.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        confirm_entry.delete(0, tk.END)

    except Exception:
        messagebox.showerror("Error", "Username already exists!")

    finally:
        connection.close()

# ===============================
# Main Window
# ===============================

window = tk.Tk()
window.title("Expense Tracker - Register")
window.geometry("400x350")
window.resizable(False, False)

# Heading
title = tk.Label(
    window,
    text="Expense Tracker",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

# Username
username_label = tk.Label(window, text="Username")
username_label.pack()

username_entry = tk.Entry(window, width=30)
username_entry.pack(pady=5)

# Password
password_label = tk.Label(window, text="Password")
password_label.pack()

password_entry = tk.Entry(window, width=30, show="*")
password_entry.pack(pady=5)

# Confirm Password
confirm_label = tk.Label(window, text="Confirm Password")
confirm_label.pack()

confirm_entry = tk.Entry(window, width=30, show="*")
confirm_entry.pack(pady=5)

# Register Button
register_button = tk.Button(
    window,
    text="Register",
    width=15,
    command=register
)
register_button.pack(pady=20)

window.mainloop()
