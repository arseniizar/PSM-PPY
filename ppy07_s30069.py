import functools
import math


# Exercise 1: Pretty Printer

@functools.singledispatch
def pretty_print(x):
    print(f"[Default] {type(x).__name__}: {x}")


@pretty_print.register
def _(x: int):
    kind = "even" if x % 2 == 0 else "odd"
    print(f"[Integer] {x} is {kind}")


@pretty_print.register
def _(x: float):
    print(f"[Float] {x:.2f}")


@pretty_print.register
def _(x: str):
    print(f"[String] len={len(x)}, reversed='{x[::-1]}'")


@pretty_print.register
def _(x: dict):
    print(f"[Dict] {len(x)} keys")
    for k, v in x.items():
        print(f"  {k}: {v}")


def run_pretty_printer():
    print("\n-- Exercise 1: Pretty Printer --")
    samples = [
        8,
        3.14159,
        "Hello World",
        "A very long string example to test reversal.",
        {"x": 1, "y": 2},
        {"name": "Alice", "age": 30, "city": "Wonderland"},
        [1, 2, 3],
    ]
    for item in samples:
        pretty_print(item)
    input("\nDone. Press Enter to return to menu...")


# Exercise 2: Geometry Calculator

class Circle:
    def __init__(self, r):
        self.r = r


class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h


class Triangle:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c


@functools.singledispatch
def area(s):
    raise NotImplementedError("Unknown shape")


@area.register
def _(c: Circle):
    return math.pi * c.r * c.r


@area.register
def _(r: Rectangle):
    return r.w * r.h


@area.register
def _(t: Triangle):
    s = (t.a + t.b + t.c) / 2
    return math.sqrt(s * (s - t.a) * (s - t.b) * (s - t.c))


@functools.singledispatch
def perimeter(s):
    raise NotImplementedError("Unknown shape")


@perimeter.register
def _(c: Circle):
    return 2 * math.pi * c.r


@perimeter.register
def _(r: Rectangle):
    return 2 * (r.w + r.h)


@perimeter.register
def _(t: Triangle):
    return t.a + t.b + t.c


def run_geometry():
    print("\n-- Exercise 2: Geometry Calculator --")
    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
        Circle(2.5),
        Rectangle(10, 3),
    ]
    for i, s in enumerate(shapes, 1):
        a = area(s)
        p = perimeter(s)
        print(f"Shape {i}: {s.__class__.__name__}")
        print(f"  Area     = {a:.2f}")
        print(f"  Perimeter= {p:.2f}")
    input("\nDone. Press Enter to return to menu...")


# Main menu

def main():
    while True:
        print("\nLIST - TRAINING TASKS")
        print("1: Pretty Printer")
        print("2: Geometry Calculator")
        print("0: Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            run_pretty_printer()
        elif choice == "2":
            run_geometry()
        elif choice == "0":
            print("Exit!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
