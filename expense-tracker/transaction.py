import sys
print("Python being used:", sys.executable)

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import connect_database

def save_transaction():
    date = date_entry.get()
    trans_type = type_combo.get()
    category = category_combo.get()
    amount = amount_entry.get().strip()
    description = description_entry.get().strip()

    # Validation
    if amount == "":
        messagebox.showerror("Error", "Amount is required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    connection = connect_database()
    cursor = connection.cursor()

    # Temporary user_id = 1
    # Later we'll use the logged-in user's ID
    cursor.execute("""
        INSERT INTO transactions
        (user_id, date, type, category, amount, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (1, date, trans_type, category, amount, description))

    connection.commit()
    connection.close()

    messagebox.showinfo("Success", "Transaction Added Successfully!")

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)


window = tk.Tk()
window.title("Add Transaction")
window.geometry("450x450")
window.resizable(False, False)

title = tk.Label(
    window,
    text="Add Transaction",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

# Date
tk.Label(window, text="Date").pack()
date_entry = DateEntry(window, width=25)
date_entry.pack(pady=5)

# Type
tk.Label(window, text="Type").pack()

type_combo = ttk.Combobox(
    window,
    values=["Income", "Expense"],
    state="readonly",
    width=27
)
type_combo.current(0)
type_combo.pack(pady=5)

# Category
tk.Label(window, text="Category").pack()

category_combo = ttk.Combobox(
    window,
    values=[
        "Salary",
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Other"
    ],
    state="readonly",
    width=27
)
category_combo.current(0)
category_combo.pack(pady=5)

# Amount
tk.Label(window, text="Amount").pack()
amount_entry = tk.Entry(window, width=30)
amount_entry.pack(pady=5)

# Description
tk.Label(window, text="Description").pack()
description_entry = tk.Entry(window, width=30)
description_entry.pack(pady=5)

# Save Button
save_btn = tk.Button(
    window,
    text="Save Transaction",
    width=20,
    command=save_transaction
)
save_btn.pack(pady=20)

window.mainloop()
