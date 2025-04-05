# 1
import sys


def bank_transactions():
    accounts = {
        "Alice": {"balance": 1000.0, "history": []},
        "Bob": {"balance": 1500.0, "history": []},
    }
    while True:
        account_name = input("Enter your name: ")
        if account_name not in accounts:
            print("Invalid name")
            continue
        try:
            operation = int(input("What would you like to do? (1 - deposit, 2 - withdrawal, 3 - check the balance): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match operation:
            case 1:
                try:
                    amount = float(input("Enter the amount you want to deposit: "))
                    if amount <= 0:
                        print("Deposit amount must be positive.")
                        continue
                    deposit(accounts, account_name, amount)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
            case 2:
                try:
                    amount = float(input("Enter the amount you want to withdrawal: "))
                    if amount <= 0:
                        print("Withdrawal amount must be positive.")
                        continue
                    withdraw(accounts, account_name, amount)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
            case 3:
                check_the_balance(accounts, account_name)
            case _:
                print("Invalid input")
        print_account_info(accounts, account_name)
        i = input("If you want to continue with this account, enter \"continue\", otherwise enter \"done\": ")
        if i.lower() == "done": break;


def print_account_info(accounts, name):
    print(f"Account name: {name}, balance: {accounts[name]['balance']}, history: {accounts[name]['history']}")


def deposit(accounts, name, amount):
    accounts[name]["balance"] += amount
    accounts[name]["history"].append(("Deposited", amount))


def withdraw(accounts, name, amount):
    if accounts[name]["balance"] < amount:
        print("Insufficient balance")
    else:
        accounts[name]["balance"] -= amount
        accounts[name]["history"].append(("Withdrawn", amount))


def check_the_balance(accounts, name):
    print(f"Your balance: {accounts[name]['balance']}")
    accounts[name]["history"].append(("Checked balance", accounts[name]['balance']))


# 2

def inventory_management_system():
    inventory = {
        "Laptop": 5,
        "Mouse": 10,
        "Keyboard": 8,
        "Headphones": 3,
    }

    product_name = input("Enter product name: ")
    if product_name not in inventory:
        print(f"Product '{product_name}' not found in inventory.")
        return

    try:
        quantity = int(input("Enter quantity: "))
        if quantity <= 0:
            print("Quantity must be positive.")
            return
    except ValueError:
        print("Invalid quantity. Please enter a whole number.")
        return

    if inventory[product_name] >= quantity:
        print("Order accepted")
        inventory[product_name] -= quantity
        print(f"Remaining stock for {product_name}: {inventory[product_name]}")
    else:
        print(f"Order rejected. Insufficient stock for {product_name}. Available: {inventory[product_name]}")


# 3

def library_book_checkout_system():
    library_books = {
        "The Great Gatsby": True,
        "1984": False,
        "Moby Dick": True,
        "To Kill a Mockingbird": False
    }

    while True:
        book = input("Enter the book title to check out (or type 'exit' to quit): ")
        if book.lower() == "exit":
            break
        if book not in library_books:
            print("This book is not in our library.")
            continue
        if library_books[book]:
            print(f"You have checked out '{book}'. Enjoy reading!")
            library_books[book] = False
        else:
            print(f"Sorry, '{book}' is already checked out.")


# 4

def student_grade_evaluation_system():
    students = [
        {"name": "Alice", "exam_score": 85, "attendance": 90},
        {"name": "Bob", "exam_score": 58, "attendance": 75},
        {"name": "Charlie", "exam_score": 45, "attendance": 80},
        {"name": "Diana", "exam_score": 92, "attendance": 95},
        {"name": "Ethan", "exam_score": 60, "attendance": 40}
    ]

    min_attendance = 50
    min_score = 60

    print("\n--- Student Grade Evaluation ---")
    for student in students:
        name = student["name"]
        score = student["exam_score"]
        attendance = student["attendance"]

        passed_attendance = attendance >= min_attendance
        passed_score = score >= min_score

        if passed_attendance and passed_score:
            print(f"{name}: Passed (Score: {score}%, Attendance: {attendance}%)")
        else:
            reason = []
            if not passed_attendance:
                reason.append(f"Attendance below {min_attendance}% ({attendance}%)")
            if not passed_score:
                reason.append(f"Exam score below {min_score}% ({score}%)")
            print(f"{name}: Failed ({', '.join(reason)})")
    print("--- Evaluation Complete ---\n")


# menu:

def main():
    while True:
        print("\n--- Main Menu ---")
        print("1 - Bank Transactions")
        print("2 - Inventory Management System")
        print("3 - Library Book Checkout System")
        print("4 - Student Grade Evaluation System")
        print("0 - Exit")
        choice = input("Select a task: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        match choice:
            case 1:
                bank_transactions()
            case 2:
                inventory_management_system()
            case 3:
                library_book_checkout_system()
            case 4:
                student_grade_evaluation_system()
            case 0:
                print("Exiting")
                sys.exit()
            case _:
                print("Invalid selection.")


if __name__ == "__main__":
    main()
