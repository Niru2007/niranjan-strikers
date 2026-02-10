import csv
import os
from datetime import datetime

DATA_DIR = "data"
ITEMS_FILE = f"{DATA_DIR}/items.csv"
RENTALS_FILE = f"{DATA_DIR}/rentals.csv"

os.makedirs(DATA_DIR, exist_ok=True)

# ---------------- FILE SETUP ----------------
def setup_files():
    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Item ID", "Item Name", "Category", "Price per Day", "Available"])

    if not os.path.exists(RENTALS_FILE):
        with open(RENTALS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["User Name", "Item Name", "Days", "Total Price", "Date"])

# ---------------- ADMIN FUNCTIONS ----------------
def admin_menu():
    password = input("Enter admin password: ")

    if password != "123":
        print("❌ Wrong password")
        return

    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Add Item")
        print("2. View Items")
        print("3. View Rentals")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            view_items()
        elif choice == "3":
            view_rentals()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

def add_item():
    name = input("Item name: ")
    category = input("Category: ")
    price = input("Price per day: ")

    item_id = sum(1 for _ in open(ITEMS_FILE)) # simple ID

    with open(ITEMS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([item_id, name, category, price, "Yes"])

    print("✅ Item added successfully")

def view_items():
    with open(ITEMS_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        print("\n--- ITEMS ---")
        for row in reader:
            print(row)

def view_rentals():
    with open(RENTALS_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        print("\n--- RENTALS ---")
        for row in reader:
            print(row)

# ---------------- USER FUNCTIONS ----------------
def user_menu():
    print("\n--- AVAILABLE ITEMS ---")
    items = []

    with open(ITEMS_FILE, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[4] == "Yes":
                items.append(row)
                print(f"{row[0]}. {row[1]} - ₹{row[3]}/day")

    if not items:
        print("No items available")
        return

    user = input("Your name: ")
    item_id = input("Enter item ID to rent: ")
    days = int(input("Number of days: "))

    for item in items:
        if item[0] == item_id:
            total = days * int(item[3])
            save_rental(user, item[1], days, total)
            mark_unavailable(item_id)
            print(f"✅ Rented successfully. Total: ₹{total}")
            return

    print("❌ Item not found")

def save_rental(user, item_name, days, total):
    with open(RENTALS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            user,
            item_name,
            days,
            total,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ])

def mark_unavailable(item_id):
    rows = []

    with open(ITEMS_FILE, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows:
        if row and row[0] == item_id:
            row[4] = "No"

    with open(ITEMS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# ---------------- MAIN ----------------
def main():
    setup_files()

    while True:
        print("\n=== RENTAL SYSTEM ===")
        print("1. User")
        print("2. Admin")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            user_menu()
        elif choice == "2":
            admin_menu()
        elif choice == "3":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
