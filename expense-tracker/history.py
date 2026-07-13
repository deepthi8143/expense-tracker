import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_database
from edit_transaction import EditTransaction


# Load Transactions
def load_transactions():
    for row in tree.get_children():
        tree.delete(row)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, type, category, amount, description
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    connection.close()


# Search Transactions
def search_transactions():
    keyword = search_entry.get().strip()

    for row in tree.get_children():
        tree.delete(row)

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, type, category, amount, description
        FROM transactions
        WHERE
            date LIKE ?
            OR type LIKE ?
            OR category LIKE ?
            OR description LIKE ?
        ORDER BY id DESC
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    connection.close()


# Edit Transaction
def edit_transaction():
    selected = tree.focus()
    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a transaction."
        )
        return

    values = tree.item(selected, "values")

    EditTransaction(values)

    load_transactions()


# Delete Transaction
def delete_transaction():
    selected = tree.focus()
    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a transaction."
        )
        return

    values = tree.item(selected, "values")

    transaction_id = values[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this transaction?"
    )

    if not confirm:
        return

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id=?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Transaction Deleted Successfully!"
    )

    load_transactions()


# Main Window
window = tk.Tk()
window.title("Transaction History")
window.geometry("950x550")
window.resizable(False, False)

title = tk.Label(
    window,
    text="Transaction History",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)


# Search Frame
search_frame = tk.Frame(window)
search_frame.pack(pady=5)

tk.Label(
    search_frame,
    text="Search:"
).pack(side=tk.LEFT)

search_entry = tk.Entry(
    search_frame,
    width=30
)
search_entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(
    search_frame,
    text="Search",
    command=search_transactions
)
search_btn.pack(side=tk.LEFT)

show_all_btn = tk.Button(
    search_frame,
    text="Show All",
    command=load_transactions
)
show_all_btn.pack(side=tk.LEFT, padx=5)


# Table
columns = (
    "ID",
    "Date",
    "Type",
    "Category",
    "Amount",
    "Description"
)

tree = ttk.Treeview(
    window,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(padx=10, pady=10)


# Buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

edit_btn = tk.Button(
    button_frame,
    text="Edit Selected",
    width=18,
    bg="green",
    fg="white",
    command=edit_transaction
)
edit_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(
    button_frame,
    text="Delete Selected",
    width=18,
    bg="red",
    fg="white",
    command=delete_transaction
)
delete_btn.pack(side=tk.LEFT, padx=10)

# Load Data
load_transactions()
window.mainloop()
