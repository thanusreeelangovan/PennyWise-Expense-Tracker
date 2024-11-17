import tkinter as tk
from tkinter import messagebox, ttk
import os
import datetime


# Expense class to store expense details
class Expense:
    def __init__(self, name, category, amount, date):
        self.name = name        # Name of the expense
        self.category = category  # Category (Food, Work, etc.)
        self.amount = amount      # Amount spent
        self.date = date          # Date of the expense


# Main Application Class for Expense Tracker
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PennyWise - Track Your Expenses")
        self.default_font = ("Times New Roman", 12)  # Font set to Times New Roman
        self.expense_file = "expenses.txt"  # File to save expenses
        self.user_file = "users.txt"  # File to save registered users
        self.expenses = []  # Will be populated after login
        self.current_user = ""  # Store the current logged-in user

        # Set the background color to pastel purple and text color to dark indigo
        self.root.configure(bg="#D0B0FF")

        # Show login screen when the app starts
        self.login_screen()

    # Function to show the login screen
    def login_screen(self):
        self.clear_screen()  # Clear any existing widgets

        # Title of the app with a large font
        title_label = tk.Label(self.root, text="PennyWise", font=("Times New Roman", 24, "bold"), bg="#D0B0FF", fg="#4B0082")
        title_label.pack(pady=20)

        # Slogan for the app
        slogan_label = tk.Label(self.root, text="Track your expenses with ease!", font=("Times New Roman", 14), bg="#D0B0FF", fg="#4B0082")
        slogan_label.pack(pady=5)

        # Login button
        login_button = tk.Button(self.root, text="Login", command=self.login_page, font=self.default_font, fg="#4B0082")
        login_button.pack(pady=10)

        # Register button
        register_button = tk.Button(self.root, text="Register", command=self.register_page, font=self.default_font, fg="#4B0082")
        register_button.pack(pady=10)

    # Function to display the login page
    def login_page(self):
        self.clear_screen()  # Clear the screen

        # Title of the app
        title_label = tk.Label(self.root, text="PennyWise Login", font=("Times New Roman", 24, "bold"), bg="#D0B0FF", fg="#4B0082")
        title_label.pack(pady=20)

        # Username and password fields
        tk.Label(self.root, text="Username:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=self.default_font)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=self.default_font, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(self.root, text="Login", command=self.check_login, font=self.default_font, fg="#4B0082").pack(pady=10)

        # Back button to go back to the initial screen
        tk.Button(self.root, text="Back", command=self.login_screen, font=self.default_font, fg="#4B0082").pack(pady=5)

    # Function to check if login is successful
    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username and password are valid
        with open(self.user_file, "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    self.current_user = username  # Set the current user
                    self.load_expenses()  # Load the user's expenses
                    self.view_expenses_screen()  # Show the expenses screen
                    return
        messagebox.showerror("Error", "Invalid username or password.")  # Error if login fails

    # Function to display the register page
    def register_page(self):
        self.clear_screen()  # Clear the screen

        # Title of the app
        title_label = tk.Label(self.root, text="PennyWise Register", font=("Times New Roman", 24, "bold"), bg="#D0B0FF", fg="#4B0082")
        title_label.pack(pady=20)

        # Username and password fields for registration
        tk.Label(self.root, text="Username:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.reg_username_entry = tk.Entry(self.root, font=self.default_font)
        self.reg_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.reg_password_entry = tk.Entry(self.root, font=self.default_font, show="*")
        self.reg_password_entry.pack(pady=5)

        # Register button
        tk.Button(self.root, text="Register", command=self.save_user, font=self.default_font, fg="#4B0082").pack(pady=10)

        # Back button to go back to the login screen
        tk.Button(self.root, text="Back", command=self.login_screen, font=self.default_font, fg="#4B0082").pack(pady=5)

    # Function to save the new user to the file
    def save_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        # Validate if fields are not empty
        if username and password:
            with open(self.user_file, "a") as f:
                f.write(f"{username},{password}\n")
            messagebox.showinfo("Success", "Registration successful. You can now log in.")  # Show success message
            self.login_screen()  # Go back to login screen
        else:
            messagebox.showerror("Error", "Please fill in both fields.")  # Error if input is invalid

    # Function to display the expenses screen after login
    def view_expenses_screen(self):
        self.clear_screen()  # Clear the screen

        # Title of the app
        title_label = tk.Label(self.root, text="PennyWise", font=("Times New Roman", 24, "bold"), bg="#D0B0FF", fg="#4B0082")
        title_label.pack(pady=20)

        # Display user info
        user_label = tk.Label(self.root, text=f"Welcome, {self.current_user}!", font=("Times New Roman", 14), bg="#D0B0FF", fg="#4B0082")
        user_label.pack(pady=5)

        # Button to add a new expense
        add_button = tk.Button(self.root, text="Add New Expense", command=self.add_expense_screen, font=self.default_font, fg="#4B0082")
        add_button.pack(pady=10)

        # Listbox to display existing expenses
        self.expense_listbox = tk.Listbox(self.root, width=50, height=10, font=self.default_font, fg="#4B0082")
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"{expense.name} - {expense.amount} ({expense.category})")
        self.expense_listbox.pack(pady=10)

        # Buttons for editing and deleting selected expenses
        edit_button = tk.Button(self.root, text="Edit Selected Expense", command=self.edit_selected_expense, font=self.default_font, fg="#4B0082")
        edit_button.pack(pady=5)

        delete_button = tk.Button(self.root, text="Delete Selected Expense", command=self.delete_selected_expense, font=self.default_font, fg="#4B0082")
        delete_button.pack(pady=5)

    # Function to add a new expense (same as in the previous code)
    def add_expense_screen(self):
        self.clear_screen()  # Clear the screen to show new form

        title_label = tk.Label(self.root, text="PennyWise", font=("Times New Roman", 24, "bold"), bg="#D0B0FF", fg="#4B0082")
        title_label.pack(pady=20)

        # Expense entry fields
        tk.Label(self.root, text="Name:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.name_entry = tk.Entry(self.root, font=self.default_font)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Amount:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, font=self.default_font)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Category:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.category_combobox = ttk.Combobox(self.root, values=["Food", "Transport", "Entertainment", "Other"], font=self.default_font)
        self.category_combobox.pack(pady=5)

        tk.Label(self.root, text="Date:", font=self.default_font, bg="#D0B0FF", fg="#4B0082").pack(pady=5)
        self.date_entry = tk.Entry(self.root, font=self.default_font)
        self.date_entry.pack(pady=5)

        # Save and Cancel buttons
        save_button = tk.Button(self.root, text="Save", command=self.save_expense, font=self.default_font, fg="#4B0082")
        save_button.pack(pady=5)

        cancel_button = tk.Button(self.root, text="Cancel", command=self.view_expenses_screen, font=self.default_font, fg="#4B0082")
        cancel_button.pack(pady=5)

    # Function to save an expense (same as in the previous code)
    def save_expense(self):
        name = self.name_entry.get()  # Get the name of the expense
        amount = self.amount_entry.get()  # Get the amount of the expense
        category = self.category_combobox.get()  # Get the category of the expense
        date = self.date_entry.get()  # Get the date of the expense

        if name and amount and category:  # Check if all fields are filled
            new_expense = Expense(name, category, float(amount), date)
            self.expenses.append(new_expense)  # Add the new expense to the list
            self.save_expenses_to_file()  # Save the updated expense list
            self.view_expenses_screen()  # Go back to the expenses screen
        else:
            messagebox.showerror("Error", "Please fill in all fields.")  # Show error if not all fields are filled

    # Function to delete a selected expense (same as in the previous code)
    def delete_selected_expense(self):
        selected_index = self.expense_listbox.curselection()  # Get the selected expense index
        if selected_index:
            response = messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?")
            if response:
                del self.expenses[selected_index[0]]  # Delete the expense
                self.save_expenses_to_file()  # Save the updated expenses
                self.view_expenses_screen()  # Refresh the screen

    # Function to save expenses to file (same as in the previous code)
    def save_expenses_to_file(self):
        with open(self.expense_file, "w") as f:
            for expense in self.expenses:
                f.write(f"{expense.name},{expense.category},{expense.amount},{expense.date}\n")

    # Function to load expenses from the file (same as in the previous code)
    def load_expenses(self):
        if os.path.exists(self.expense_file):
            with open(self.expense_file, "r") as f:
                for line in f:
                    name, category, amount, date = line.strip().split(",")
                    self.expenses.append(Expense(name, category, float(amount), date))

    # Function to clear the screen
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)  # Create the app instance
    root.mainloop()  # Start the Tkinter event loop
