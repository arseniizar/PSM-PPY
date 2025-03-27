# shared functions

def prompt_data(target_dict, fields, key_field, converters=None, validators=None, prompt_msg=None):
    if prompt_msg is None:
        field_list = ", ".join(fields)
        prompt_msg = f"Type data in form of '{field_list}' or 'continue' to proceed: "
    while True:
        info = input(prompt_msg)
        if info.strip().lower() == "continue":
            break
        parts = [p.strip() for p in info.split(',')]
        if len(parts) != len(fields):
            print(f"Please enter exactly {len(fields)} values separated by commas.")
            continue
        entry = {}
        valid = True
        for i, field in enumerate(fields):
            value = parts[i]
            if converters and field in converters:
                try:
                    value = converters[field](value)
                except Exception as e:
                    print(f"Invalid conversion for '{field}': {e}")
                    valid = False
                    break
            if validators and field in validators:
                if not validators[field](value):
                    print(f"Invalid value for '{field}'")
                    valid = False
                    break
            entry[field] = value
        if not valid:
            continue
        key = entry[key_field]
        target_dict[key] = entry
    return target_dict


# 1

sales_transactions = {}
total_revenues = {}


def calculate_total_revenue():
    for name in sales_transactions:
        tp = sales_transactions[name]
        price = tp['price']
        quantity = tp['quantity']
        revenue = price * quantity
        total_revenues[name] = revenue


def display_revenues():
    print('task1: name - total revenue')
    for name in total_revenues:
        print(name + ' - ' + str(total_revenues[name]))


# 2

employee_data = {}


def apply_salary_adjustments():
    for name in employee_data:
        adjusted_salary = employee_data[name]['salary']
        performance_score = employee_data[name]['performance_score']
        if performance_score >= 5:
            adjusted_salary = employee_data[name]['salary'] + employee_data[name]['salary'] * 0.1
        elif 3.0 < performance_score < 4.4:
            adjusted_salary = employee_data[name]['salary'] + employee_data[name]['salary'] * 0.05
        employee_data[name]['salary'] = adjusted_salary


def collect_employee_data():
    global employee_data
    print("|INFO| Performance score should be from 0.0 to 5.0")
    employee_data = prompt_data(employee_data, ["name", "salary", "performance_score"],
                                "name",
                                {"salary": int, "performance_score": float},
                                {"price:": lambda x: x >= 0,
                                 "quantity": lambda x: 5 >= x >= 0})


def print_adjusted_salaries():
    print('task2: name - salary')
    for name in employee_data:
        print(name + ' ' + str(employee_data[name]['salary']))


# 3

def task3():
    print("Enter stock availability:")
    stock = {}
    stock = prompt_data(stock,
                        ["product", "stock"],
                        "product",
                        {"stock": int},
                        {"stock": lambda x: x >= 0},
                        prompt_msg="Enter 'product, stock' or 'continue' to finish: ")
    print("Enter customer orders:")
    orders = {}
    orders = prompt_data(orders,
                         ["product", "order_qty"],
                         "product",
                         {"order_qty": int},
                         {"order_qty": lambda x: x >= 0},
                         prompt_msg="Enter 'product, order_qty' or 'continue' to finish: ")
    print("\nOrder Processing Results:")
    for prod in orders:
        order_qty = orders[prod]["order_qty"]
        if prod in stock:
            available = stock[prod]["stock"]
            if order_qty <= available:
                print(f"Order for {prod} approved (ordered: {order_qty}, available: {available})")
                stock[prod]["stock"] = available - order_qty
            else:
                print(f"Order for {prod} rejected (ordered: {order_qty}, available: {available})")
        else:
            print(f"Order for {prod} rejected (product not found in stock)")
    print("\nUpdated Stock:")
    for prod in stock:
        print(f"{prod}: {stock[prod]['stock']}")


# 4

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    fib_seq = [0, 1]
    for i in range(2, n):
        fib_seq.append(fib_seq[i - 1] + fib_seq[i - 2])
    return fib_seq


def task4():
    try:
        n = int(input("Enter the number of Fibonacci sequence elements to generate: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return
    result = fibonacci(n)
    print("Fibonacci sequence:", result)


# 5

def task5():
    login_data = {"correct_password": "secure123", "attempts": 3}
    while login_data["attempts"] > 0:
        pwd = input("Enter password: ")
        if pwd == login_data["correct_password"]:
            print("Access granted!")
            return
        else:
            login_data["attempts"] -= 1
            if login_data["attempts"] > 0:
                print(f"Wrong password! {login_data['attempts']} attempts left.")
            else:
                print("Account locked!")


# task running methods:

def task1():
    global sales_transactions
    sales_transactions = prompt_data(sales_transactions,
                                     ["name", "price", "quantity"],
                                     "name",
                                     {"price": int, "quantity": int},
                                     {"price": lambda x: x >= 0,
                                      "quantity": lambda x: x >= 0})
    calculate_total_revenue()
    display_revenues()


def task2():
    collect_employee_data()
    apply_salary_adjustments()
    print_adjusted_salaries()


def task_switch_case(name):
    match name:
        case 'task1':
            task1()
        case 'task2':
            task2()
        case 'task3':
            task3()
        case 'task4':
            task4()
        case 'task5':
            task5()
        case _:
            print('Invalid option')


def main():
    task_name = input('choose task number (task1 to task5): ')
    task_switch_case(task_name)


main()
