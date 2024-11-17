import calendar
import datetime
import getpass  # For secure password input
import os  # For file operations

# Expense class to store expense details
class Expense:
    def __init__(self, name, category, amount, date):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"Expense(name={self.name}, category={self.category}, amount={self.amount}, date={self.date})"

# User authentication
def authenticate_user():
    print("Welcome to the Expense Tracker!")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Check for the existence of the users file
    if not os.path.exists("users.txt"):
        print("❌ No registered users found. Please register first.")
        return False

    with open("users.txt", "r") as f:
        users = f.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(",")
            if username == stored_username and password == stored_password:
                print(f"✅ Login successful! Welcome, {username}.")
                return True

    print("❌ Invalid username or password. Exiting...")
    return False

# User registration
def register_user():
    print("Register a new account:")
    username = input("Enter a username: ")
    password = getpass.getpass("Enter a password: ")

    # Check if users file exists
    with open("users.txt", "a") as f:
        f.write(f"{username},{password}\n")

    print(f"✅ User {username} registered successfully!")

# Main function to run the application
def main():
    print("Expense Tracker with User Authentication!")
    user_choice = input("Do you want to (L)ogin or (R)egister? ").lower()

    if user_choice == "r":
        register_user()
        return
    elif user_choice != "l":
        print("❌ Invalid choice. Exiting...")
        return

    if not authenticate_user():
        return

    expense_file_path = "expenses.csv"
    budget = 2000

    while True:
        print("\n--- Menu ---")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. Delete Expense")
        print("4. View Expenses")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == "2":
            edit_expense(expense_file_path)
        elif choice == "3":
            delete_expense(expense_file_path)
        elif choice == "4":
            summarize_expenses(expense_file_path, budget)
        elif choice == "5":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# Function to get user expense input
def get_user_expense():
    print(f"Getting User Expense")
    expense_name = input("Enter expense name: ")
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                print("❌ Please enter a valid positive amount!")
                continue
            break
        except ValueError:
            print("❌ Invalid input. Please enter a valid number for the amount.")

    expense_categories = ["Food", "Home", "Work", "Fun"]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if selected_index not in range(len(expense_categories)):
                print("❌ Invalid category. Please try again!")
                continue
            selected_category = expense_categories[selected_index]
            break
        except ValueError:
            print("❌ Please enter a valid number.")

    date = input("Enter the date (YYYY-MM-DD) or press Enter for today: ")
    date = date if date else datetime.date.today().isoformat()

    new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount, date=date)
    return new_expense

# Function to save expense to file
def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

# Function to edit an existing expense
def edit_expense(expense_file_path):
    print("Editing an expense...")
    expenses = load_expenses(expense_file_path)

    for i, expense in enumerate(expenses):
        print(f"{i + 1}. {expense}")

    try:
        choice = int(input("Enter the expense number to edit: ")) - 1
        if 0 <= choice < len(expenses):
            expense = expenses[choice]
            print(f"Editing {expense}...")
            expense.name = input(f"New name (or press Enter to keep '{expense.name}'): ") or expense.name
            expense.amount = float(input(f"New amount (or press Enter to keep {expense.amount}): ") or expense.amount)
            expense.category = input(f"New category (or press Enter to keep '{expense.category}'): ") or expense.category
            save_expenses_to_file(expenses, expense_file_path)
            print("✅ Expense updated successfully!")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Invalid input. Please try again.")

# Function to delete an expense
def delete_expense(expense_file_path):
    print("Deleting an expense...")
    expenses = load_expenses(expense_file_path)

    for i, expense in enumerate(expenses):
        print(f"{i + 1}. {expense}")

    try:
        choice = int(input("Enter the expense number to delete: ")) - 1
        if 0 <= choice < len(expenses):
            del expenses[choice]
            save_expenses_to_file(expenses, expense_file_path)
            print("✅ Expense deleted successfully!")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Invalid input. Please try again.")

# Function to summarize expenses and remaining budget
def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expenses")
    expenses = load_expenses(expense_file_path)
    date_filter = input("Enter a date range (YYYY-MM-DD to YYYY-MM-DD) or press Enter for all: ")

    if date_filter:
        start_date, end_date = date_filter.split(" to ")
        expenses = [
            e for e in expenses if start_date <= e.date <= end_date
        ]

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: Rs.{amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: Rs.{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(green(f"✅ Budget Remaining: Rs.{remaining_budget:.2f}"))

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: Rs.{daily_budget:.2f}"))

# Function to load expenses from file
def load_expenses(expense_file_path):
    expenses = []
    if os.path.exists(expense_file_path):
        with open(expense_file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category, expense_date = line.strip().split(",")
                expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                    date=expense_date
                )
                expenses.append(expense)
    return expenses

# Function to save all expenses to file
def save_expenses_to_file(expenses, expense_file_path):
    with open(expense_file_path, "w") as f:
        for expense in expenses:
            f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

# Function to display text in green color
def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
