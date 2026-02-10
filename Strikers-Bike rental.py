import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

DATA_DIR = "data"
ITEMS_FILE = f"{DATA_DIR}/items.csv"
RENTALS_FILE = f"{DATA_DIR}/rentals.csv"

os.makedirs(DATA_DIR, exist_ok=True)

# ---------- FILE SETUP ----------
def setup_files():
    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Item ID", "Item Name", "Category", "Price", "Available"])

    if not os.path.exists(RENTALS_FILE):
        with open(RENTALS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["User", "Item", "Days", "Total", "Date"])

setup_files()

# ---------- HELPERS ----------
def read_items():
    with open(ITEMS_FILE, "r") as f:
        return list(csv.reader(f))

def write_items(rows):
    with open(ITEMS_FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)

def add_rental(user, item, days, total):
    with open(RENTALS_FILE, "a", newline="") as f:
        csv.writer(f).writerow(
            [user, item, days, total, datetime.now().strftime("%Y-%m-%d %H:%M")]
        )

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Rental Management System")
root.geometry("400x350")

# ---------- SCREENS ----------
def clear():
    for widget in root.winfo_children():
        widget.destroy()

# ---------- HOME ----------
def home():
    clear()
    tk.Label(root, text="Rental Management System", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="User", width=20, command=user_menu).pack(pady=10)
    tk.Button(root, text="Admin", width=20, command=admin_login).pack(pady=10)

# ---------- USER ----------
def user_menu():
    clear()
    tk.Label(root, text="User Menu", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Rent Item", width=20, command=rent_item).pack(pady=5)
    tk.Button(root, text="Return Item", width=20, command=return_item).pack(pady=5)
    tk.Button(root, text="Back", width=20, command=home).pack(pady=20)

def rent_item():
    clear()
    tk.Label(root, text="Rent Item", font=("Arial", 14)).pack(pady=10)

    items = read_items()
    available = [row for row in items[1:] if row[4] == "Yes"]

    if not available:
        messagebox.showinfo("Info", "No items available")
        home()
        return

    tk.Label(root, text="Your Name").pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    tk.Label(root, text="Select Item").pack()
    listbox = tk.Listbox(root, width=40)
    listbox.pack(pady=5)

    for item in available:
        listbox.insert(tk.END, f"{item[0]} - {item[1]} (₹{item[3]}/day)")

    tk.Label(root, text="Days").pack()
    days_entry = tk.Entry(root)
    days_entry.pack()

    def confirm_rent():
        if not listbox.curselection():
            messagebox.showerror("Error", "Select an item")
            return

        index = listbox.curselection()[0]
        item = available[index]

        user = user_entry.get()
        days = int(days_entry.get())
        total = days * int(item[3])

        add_rental(user, item[1], days, total)

        for r in items:
            if r and r[0] == item[0]:
                r[4] = "No"

        write_items(items)
        messagebox.showinfo("Success", f"Rented! Total ₹{total}")
        home()

    tk.Button(root, text="Confirm Rent", command=confirm_rent).pack(pady=10)
    tk.Button(root, text="Back", command=user_menu).pack()

def return_item():
    clear()
    tk.Label(root, text="Return Item", font=("Arial", 14)).pack(pady=10)

    items = read_items()
    rented = [row for row in items[1:] if row[4] == "No"]

    if not rented:
        messagebox.showinfo("Info", "No rented items")
        home()
        return

    tk.Label(root, text="Item ID").pack()
    item_entry = tk.Entry(root)
    item_entry.pack()

    def confirm_return():
        item_id = item_entry.get()

        for row in items:
            if row and row[0] == item_id:
                row[4] = "Yes"
                write_items(items)
                messagebox.showinfo("Success", "Item returned")
                home()
                return

        messagebox.showerror("Error", "Item not found")

    tk.Button(root, text="Return", command=confirm_return).pack(pady=10)
    tk.Button(root, text="Back", command=user_menu).pack()

# ---------- ADMIN ----------
def admin_login():
    clear()
    tk.Label(root, text="Admin Login", font=("Arial", 14)).pack(pady=10)

    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    def check():
        if pass_entry.get() == "123":
            admin_menu()
        else:
            messagebox.showerror("Error", "Wrong password")

    tk.Button(root, text="Login", command=check).pack(pady=10)
    tk.Button(root, text="Back", command=home).pack()

def admin_menu():
    clear()
    tk.Label(root, text="Admin Dashboard", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Add Item", width=20, command=add_item).pack(pady=5)
    tk.Button(root, text="Back", width=20, command=home).pack(pady=20)

def add_item():
    clear()
    tk.Label(root, text="Add Item", font=("Arial", 14)).pack(pady=10)

    name = tk.Entry(root)
    category = tk.Entry(root)
    price = tk.Entry(root)

    tk.Label(root, text="Item Name").pack()
    name.pack()
    tk.Label(root, text="Category").pack()
    category.pack()
    tk.Label(root, text="Price per day").pack()
    price.pack()

    def save():
        items = read_items()
        item_id = str(len(items))
        items.append([item_id, name.get(), category.get(), price.get(), "Yes"])
        write_items(items)
        messagebox.showinfo("Success", "Item added")
        admin_menu()

    tk.Button(root, text="Save", command=save).pack(pady=10)
    tk.Button(root, text="Back", command=admin_menu).pack()

# ---------- START ----------
home()
root.mainloop()
