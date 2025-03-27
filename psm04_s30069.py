import math
import matplotlib.pyplot as plt

# list of values:
# constants
g = 9.81

# provided
mass = 0
height = 0
radius = 0
alpha = 0
time = 0
steps = 0

# calculated
inertia = 0
acceleration = 0
epsilon = 0
dt = 0
sx = 0
sy = 0
vx = 0
dsx = 0
dvx = 0
xc = 0
yc = 0
beta = 0
omega = 0
db = 0
dw = 0
x = 0
y = 0

# energies
ep = 0
ek = 0
et = 0

# for plotting
t_data = []
x_data = []
y_data = []
ep_data = []
ek_data = []
et_data = []

# user choices
object_choice = 0
method_choice = 0


def prompt_value(txt, cond=lambda x: True, err="Invalid input"):
    while True:
        val_str = input(txt)
        try:
            val = float(val_str)
        except ValueError:
            print(err)
            continue
        if not cond(val):
            print(err)
            continue
        return val


def choose_object():
    while True:
        print("Choose object to simulate:")
        print("1 - Sphere")
        print("2 - Cylinder")
        val_str = input("Enter choice: ")
        try:
            choice = int(val_str)
            if choice in [1, 2]:
                return choice
        except ValueError:
            pass
        print("Invalid choice. Please enter 1 or 2.")


def choose_method():
    while True:
        print("Choose integration method:")
        print("1 - Euler Method")
        print("2 - Midpoint Method")
        val_str = input("Enter choice: ")
        try:
            choice = int(val_str)
            if choice in [1, 2]:
                return choice
        except ValueError:
            pass
        print("Invalid choice. Please enter 1 or 2.")


def set_inertia_for_object():
    global inertia
    if object_choice == 1:
        # Sphere
        inertia = (2.0 / 5.0) * mass * (radius ** 2)
    elif object_choice == 2:
        # Solid Cylinder
        inertia = 0.5 * mass * (radius ** 2)


def calculate_acceleration():
    global acceleration
    numerator = g * math.sin(alpha)
    denominator = 1 + (inertia / (mass * (radius ** 2)))
    acceleration = numerator / denominator


def calculate_epsilon():
    global epsilon
    epsilon = acceleration / radius


def calculate_dt():
    global dt
    dt = time / steps


# EULER METHOD UPDATES
def update_euler():
    global sx, vx, dsx, dvx
    global beta, omega, db, dw

    # Linear
    dsx = dt * vx
    sx += dsx
    dvx = acceleration * dt
    vx += dvx

    # Rotation
    db = omega * dt
    beta += db
    dw = epsilon * dt
    omega += dw


# MIDPOINT METHOD UPDATES
def update_midpoint():
    # s_mid and beta_mid are not used because alpha is constant so acceleration is also
    global sx, vx, dsx, dvx
    global beta, omega, db, dw

    k1_s = vx
    k1_v = acceleration

    s_mid = sx + 0.5 * k1_s * dt
    v_mid = vx + 0.5 * k1_v * dt

    k1_beta = omega
    k1_omega = epsilon

    beta_mid = beta + 0.5 * k1_beta * dt
    omega_mid = omega + 0.5 * k1_omega * dt

    # k2 for linear
    k2_s = v_mid
    k2_v = acceleration

    # k2 for rotation
    k2_beta = omega_mid
    k2_omega = epsilon

    # linear
    sx += k2_s * dt
    vx += k2_v * dt

    # rotation
    beta += k2_beta * dt
    omega += k2_omega * dt


def update_center_coords():
    global xc, yc
    first_term = sx * math.cos(-alpha)
    second_term = sy * math.sin(-alpha)
    xc = first_term - second_term

    first_term = sx * math.sin(-alpha)
    second_term = sy * math.cos(-alpha)
    yc = first_term + second_term + height


def calculate_x():
    global x
    x = xc + radius * math.cos(alpha + math.pi / 2 - beta)


def calculate_y():
    global y
    y = yc + radius * math.sin(alpha + math.pi / 2 - beta)


def update_xy():
    calculate_x()
    calculate_y()


def update_energies():
    global ep, ek, et
    ep = mass * g * yc
    ek = 0.5 * mass * (vx ** 2) + 0.5 * inertia * (omega ** 2)
    et = ep + ek


def plot_results():
    plt.figure(figsize=(7, 5))
    plt.plot(x_data, y_data, 'o-', label='Path')
    plt.title("Path (X vs. Y)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)

    plt.figure(figsize=(7, 5))
    plt.plot(t_data, ep_data, label="Ep")
    plt.plot(t_data, ek_data, label="Ek")
    plt.plot(t_data, et_data, label="Et")
    plt.title("Energies vs. Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Energy (J)")
    plt.legend()
    plt.grid(True)

    plt.show()


def main():
    global mass, height, radius, alpha, time, steps
    global object_choice, method_choice
    object_choice = choose_object()

    method_choice = choose_method()

    mass = prompt_value('Enter mass: ', lambda v: v > 0, "Must be > 0")
    height = prompt_value('Enter height: ', lambda v: v >= 0, "Must be >= 0")
    radius = prompt_value('Enter radius: ', lambda v: v > 0, "Must be > 0")
    alpha_deg = prompt_value('Enter angle (deg): ', lambda v: v >= 0, "Must be >= 0")
    time = prompt_value('Enter time (s): ', lambda v: v > 0, "Must be > 0")
    steps = int(prompt_value('Enter steps: ', lambda v: v > 0, "Must be > 0"))

    alpha = math.radians(alpha_deg)

    set_inertia_for_object()
    calculate_acceleration()
    calculate_epsilon()
    calculate_dt()

    t_data.clear()
    x_data.clear()
    y_data.clear()
    ep_data.clear()
    ek_data.clear()
    et_data.clear()

    for i in range(steps + 1):
        t_current = i * dt
        t_data.append(t_current)

        if method_choice == 1:
            update_euler()
        else:
            update_midpoint()

        update_center_coords()

        update_xy()

        update_energies()

        x_data.append(x)
        y_data.append(y)
        ep_data.append(ep)
        ek_data.append(ek)
        et_data.append(et)

    plot_results()


main()
