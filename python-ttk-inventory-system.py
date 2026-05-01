import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import database

# Initialize DB
database.connect_db()

root = tk.Tk()
root.title("Inventory Management System")
root.geometry("900x550")

# ================= FUNCTIONS =================

def add_product():
    name = name_entry.get()
    category = category_entry.get()
    quantity = qty_entry.get()
    price = price_entry.get()

    if not name or not category or not quantity or not price:
        messagebox.showwarning("Warning", "All fields are required")
        return

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (product_name, category, quantity, price) VALUES (?, ?, ?, ?)",
        (name, category, quantity, price)
    )
    conn.commit()
    conn.close()

    clear_fields()
    load_products()


def load_products():
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")

    for row in cursor.fetchall():
        table.insert('', tk.END, values=row)

    conn.close()


def delete_product():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a product")
        return

    product_id = table.item(selected, 'values')[0]

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

    load_products()


def clear_fields():
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

# ================= UI =================

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

# Form Section
form = ttk.LabelFrame(frame, text="Add Product", padding=10)
form.pack(fill="x")

labels = ["Product Name", "Category", "Quantity", "Price"]
entries = []

for i, label in enumerate(labels):
    ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=5)

name_entry = ttk.Entry(form)
category_entry = ttk.Entry(form)
qty_entry = ttk.Entry(form)
price_entry = ttk.Entry(form)

name_entry.grid(row=0, column=1, padx=5)
category_entry.grid(row=1, column=1, padx=5)
qty_entry.grid(row=2, column=1, padx=5)
price_entry.grid(row=3, column=1, padx=5)

# Buttons
ttk.Button(form, text="Add Product", command=add_product).grid(row=4, columnspan=2, pady=10)

# Table
columns = ("ID", "Product", "Category", "Quantity", "Price")
table = ttk.Treeview(frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

table.pack(fill="both", expand=True, pady=15)

ttk.Button(frame, text="Delete Selected", command=delete_product).pack()

load_products()
root.mainloop()

# Built-in libraries only
