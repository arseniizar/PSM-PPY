import math
import matplotlib.pyplot as plt

k = int(input('Input drag (k): '))
m = int(input('Input mass (m): '))
steps_count = int(input('Input number of steps for simulation: '))
t_total = int(input('Input time (s): '))
vx = int(input('Input horizontal velocity vx (m/s): '))
vy = int(input('Input vertical velocity vy (m/s): '))

if steps_count < 1 or m < 1 or t_total < 1 or k < 1:
    print('ERROR: Invalid input!')
    exit(0)

dt = t_total / steps_count
x = 0
y = 0
g = 9.81
ax = 0
ay = 0

# shared functions

def calculate_ax():
    global vx, ax
    ax = (-k / m) * vx


def calculate_ay():
    global vy, ay
    ay = -g - (k / m) * vy


def calculate_accelerations():
    calculate_ax()
    calculate_ay()


# euler

def calculate_new_vx():
    global vx
    vx = vx + ax * dt


def calculate_new_vy():
    global vy
    vy = vy + ay * dt


def calculate_velocities():
    calculate_new_vx()
    calculate_new_vy()


def calculate_new_x():
    global x
    x = x + vx * dt


def calculate_new_y():
    global y
    y = y + vy * dt


def calculate_positions():
    calculate_new_x()
    calculate_new_y()


# midpoint

def calculate_halfstep_vx():
    global vx
    vx = vx + ax * dt / 2


def calculate_haflstep_vy():
    global vy
    vy = vy + ay * dt / 2


def calculate_halfstep_velocities():
    calculate_halfstep_vx()
    calculate_haflstep_vy()


def calculate_halfstep_x():
    global vx
    vx = vx + ax * dt / 2


def calculate_halfstep_y():
    global vy
    vy = vy + ay * dt / 2


def calculate_halfstep_positions():
    calculate_halfstep_x()
    calculate_halfstep_y()

# Run Euler
def run_euler_simulation():
    xs = [x]
    ys = [y]
    for i in range(steps_count):
        calculate_accelerations()
        calculate_velocities()
        calculate_positions()
        xs.append(x)
        ys.append(y)
    return xs, ys

# Run Midpoint
def run_midpoint_simulation():
    xs = [x]
    ys = [y]
    for i in range(steps_count):
        calculate_accelerations()
        calculate_halfstep_velocities()
        calculate_halfstep_positions()
        # Recalculate acceleration at the “half step”
        calculate_accelerations()
        # Now do the full step with the new acceleration
        calculate_velocities()
        calculate_positions()
        xs.append(x)
        ys.append(y)
    return xs, ys

def draw_and_run(choice):
    if choice == 1:
        method_name = "Euler"
        xs, ys = run_euler_simulation()
    elif choice == 2:
        method_name = "Midpoint"
        xs, ys = run_midpoint_simulation()
    else:
        print('ERROR: Invalid choice!')
        exit(0)

    ts = [i * dt for i in range(len(xs))]

    plt.figure(figsize=(10, 6))

    plt.plot(xs, ys, marker='o', markersize=4, label=f'{method_name} Trajectory', linewidth=1)

    plt.scatter(xs, ys, c='red', s=10, alpha=0.5, label='Data Points')

    N = max(1, steps_count // 10)
    for i in range(0, len(xs), N):
        plt.text(xs[i], ys[i], f"t={ts[i]:.2f}s", fontsize=8)

    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.title(f'{method_name} Projectile Trajectory')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    choice = int(input('Input 1 for euler simulation or 2 for midpoint simulation: '))
    draw_and_run(choice)

main()
