import math

sales_data = {
    'Product A': [100, 200, 300],
    'Product B': [150, 250, 350],
    'Product C': [50, 70, 90]
}


# 1

def calculate_sales_data(data):
    totals = {}
    for label in data:
        total = 0
        for sale in sales_data[label]:
            total += sale
        print('total for ' + label + ' is ' + str(total))
        totals[label] = total
    return max(totals.values())


# 2

def operator_switch(value):
    if value == 'mul':
        return lambda x, y: x * y
    elif value == 'div':
        return lambda x, y: x / y
    elif value == 'add':
        return lambda x, y: x + y
    elif value == 'sub':
        return lambda x, y: x - y
    elif value == 'pow':
        return lambda x, y: x ** y

def calculate(operator, first, second):
    operation = operator_switch(operator)
    return operation(first, second)


def convert(num):
    if isinstance(num, float):
        return int(num)
    elif isinstance(num, int):
        return float(num)
    else:
        raise ValueError("Unsupported type")


def calculate_abs_diff(first, second):
    return abs(first - second)


def are_even(first, second):
    if first % 2 == 0 and second % 2 == 0:
        print('both numbers are even')
    elif first % 2 != 0 and second % 2 != 0:
        print('both numbers are odd')
    else:
        print('one number is odd and another is even')


# 3

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def primes_in_range(start, end):
    result = []
    for num in range(start, end + 1):
        if is_prime(num):
            result.append(num)
    return result

# 4

# Q: How would you handle the case where the user tries to divide by zero?
# A: I just print that this is an invalid operation and continue the loop

# Q: What data types would you use for the inputs and how would you convert user input appropriately?
# A: I use floats so its more flexible, even if user types in an int it is still not a problem

# Q: If the user inputs an invalid choice, how would you make sure the program
# - prompts them again for a valid option instead of terminating the program?
# A: I dont raise any errors, instead I print information about the error to the user and continue the loop so It
# - will start from the beggining

def calculator():
    while True:
        op = input('Type operation (pow, sqrt, add, mul, div, sub): ')
        if op not in ['pow', 'sqrt', 'add', 'mul', 'div', 'sub']:
            print('Invalid operation')
            continue
        operation = operator_switch(op)
        if op == 'sqrt':
            a = float(input('Type a: '))
            if a < 0:
                print()
                continue
            print(math.sqrt(a))
        else:
            a = float(input('Type a: '))
            b = float(input('Type b: '))
            if op == 'div' and b == 0:
                print('cannot divide by zero')
                continue
            print(str(operation(a, b)))
        choice = input('type \'exit\' to quit or \'continue\' to proceed: ')
        if choice == 'exit':
            break

def main():
    print('Biggest total is ' + str(calculate_sales_data(sales_data)))
    print(calculate('mul', 3, 5))
    print('float to int: ' + str(1.5) + ' to ' + str(convert(1.5)))
    print('int to float: ' + str(5) + ' to ' + str(convert(5)))
    print('absolute difference (5 - 8): ' + str(calculate_abs_diff(5, 8)))
    print('are even (5 and 11):')
    are_even(5, 11)
    print('primes in range (from 5 to 234): ' + str(primes_in_range(5, 234)))
    calculator()


main()
