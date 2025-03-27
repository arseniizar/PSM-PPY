import math
import matplotlib.pyplot as plt
import numpy as np

g = 9.81
mass = 0
method_name = ''
length = 1.0
initial_angle = math.pi / 4
initial_velocity = 0.0
tmax = 10
time_step = 0.01
steps = int(tmax / time_step) + 1
times = []
angles = []
velocities = []


def accuracy(alpha, omega):
    epsilon = -(g / length) * np.sin(alpha)
    return omega, epsilon


def euler_method(angle, velocity):
    global times, velocities, angles
    time = 0.0
    times, angles, velocities = [time], [angle], [velocity]
    for _ in range(steps):
        k1_omega, k1_epsilon = accuracy(angle, velocity)
        angle += k1_omega * time_step
        velocity += k1_epsilon * time_step
        time += time_step
        times.append(time)
        angles.append(angle)
        velocities.append(velocity)
    display_energy()
    draw_graph()


def midpoint_method(angle, velocity):
    global times, angles, velocities
    time = 0.0
    time_values, angle_values, velocity_values = [time], [angle], [velocity]
    for _ in range(steps):
        k1_omega, k1_epsilon = accuracy(angle, velocity)
        mid_angle = angle + 0.5 * k1_omega * time_step
        mid_velocity = velocity + 0.5 * k1_epsilon * time_step
        k2_omega, k2_epsilon = accuracy(mid_angle, mid_velocity)
        angle += k2_omega * time_step
        velocity += k2_epsilon * time_step
        time += time_step
        time_values.append(time)
        angle_values.append(angle)
        velocity_values.append(velocity)
    display_energy()
    draw_graph()


def rk4_method(angle, velocity):
    global times, angles, velocities
    time = 0.0
    times, angles, velocities, = [time], [angle], [velocity]
    for _ in range(steps):
        k1_omega, k1_epsilon = accuracy(angle, velocity)
        k2_omega, k2_epsilon = accuracy(angle + 0.5 * time_step * k1_omega, velocity + 0.5 * time_step * k1_epsilon)
        k3_omega, k3_epsilon = accuracy(angle + 0.5 * time_step * k2_omega, velocity + 0.5 * time_step * k2_epsilon)
        k4_omega, k4_epsilon = accuracy(angle + time_step * k3_omega, velocity + time_step * k3_epsilon)
        angle += (time_step / 6) * (k1_omega + 2 * k2_omega + 2 * k3_omega + k4_omega)
        velocity += (time_step / 6) * (k1_epsilon + 2 * k2_epsilon + 2 * k3_epsilon + k4_epsilon)
        time += time_step
        times.append(time)
        angles.append(angle)
        velocities.append(velocity)
    display_energy()
    draw_graph()


def display_energy():
    global angles, velocities
    angles, velocities = np.array(angles), np.array(velocities)
    kinetic_energy = 0.5 * mass * (length * velocities) ** 2
    potential_energy = mass * g * length * (1 - np.cos(angles))
    total_energy = kinetic_energy + potential_energy
    plt.plot(times, kinetic_energy, label=f'{method_name} - Kinetic Energy')
    plt.plot(times, potential_energy, label=f'{method_name} - Potential Energy')
    plt.plot(times, total_energy, label=f'{method_name} - Total Energy')
    plt.legend()
    plt.title(f'Energy over Time - {method_name}')
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.show()


def draw_graph():
    x_values, y_values = length * np.sin(angles), -length * np.cos(angles)
    plt.plot(x_values, y_values, label=f'{method_name} - Trajectory')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.title(f'Trajectory - {method_name}')
    plt.show()


def method_switch(number):
    global method_name
    if number == 1:
        method_name = 'Euler Method'
        euler_method()
    elif number == 2:
        method_name = 'Midpoint Method'
        midpoint_method()
    elif number == 3:
        method_name = 'Runge-Kutta 4 Method'
        rk4_method()


def main():
    global mass, length, initial_angle, initial_velocity

    mass = float(input("Enter mass: "))
    length = float(input("Enter length: "))
    initial_angle = float(input("Enter initial angle: "))
    initial_velocity = float(input("Enter initial velocity: "))

    choice = int(input(
'''Choose a method:
1 - Euler
2 - Midpoint
3 - Rk4
'''))

    method_switch(choice)


main()
