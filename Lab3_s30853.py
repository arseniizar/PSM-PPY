import math
import matplotlib.pyplot as plt
import numpy as np

g = 10
length = 1.0
initial_angle = math.pi / 4
initial_velocity = 0.0
tmax = 10
time_step = 0.01
steps = int(tmax / time_step) + 1

def accur(alpha, omega):
    epsilon = -(g / length) * np.sin(alpha)
    return omega, epsilon

def euler_method(angle, velocity, time_step):
    time = 0.0
    time_values, angle_values, velocity_values = [time], [angle], [velocity]
    for _ in range(steps):
        k1_omega, k1_epsilon = accur(angle, velocity)
        angle += k1_omega * time_step
        velocity += k1_epsilon * time_step
        time += time_step
        time_values.append(time)
        angle_values.append(angle)
        velocity_values.append(velocity)
    return time_values, angle_values, velocity_values, "Euler Method"

def midpoint_method(angle, velocity, time_step):
    time = 0.0
    time_values, angle_values, velocity_values = [time], [angle], [velocity]
    for _ in range(steps):
        k1_omega, k1_epsilon = accur(angle, velocity)
        mid_angle = angle + 0.5 * k1_omega * time_step
        mid_velocity = velocity + 0.5 * k1_epsilon * time_step
        k2_omega, k2_epsilon = accur(mid_angle, mid_velocity)
        angle += k2_omega * time_step
        velocity += k2_epsilon * time_step
        time += time_step
        time_values.append(time)
        angle_values.append(angle)
        velocity_values.append(velocity)
    return time_values, angle_values, velocity_values, "Midpoint Method"

def rk4_method(angle, velocity, time_step):
    time = 0.0
    time_values, angle_values, velocity_values = [time], [angle], [velocity]
    for _ in range(steps):
        k1_omega, k1_epsilon = accur(angle, velocity)
        k2_omega, k2_epsilon = accur(angle + 0.5 * time_step * k1_omega, velocity + 0.5 * time_step * k1_epsilon)
        k3_omega, k3_epsilon = accur(angle + 0.5 * time_step * k2_omega, velocity + 0.5 * time_step * k2_epsilon)
        k4_omega, k4_epsilon = accur(angle + time_step * k3_omega, velocity + time_step * k3_epsilon)
        angle += (time_step / 6) * (k1_omega + 2 * k2_omega + 2 * k3_omega + k4_omega)
        velocity += (time_step / 6) * (k1_epsilon + 2 * k2_epsilon + 2 * k3_epsilon + k4_epsilon)
        time += time_step
        time_values.append(time)
        angle_values.append(angle)
        velocity_values.append(velocity)
    return time_values, angle_values, velocity_values, "Runge-Kutta 4 Method"

def display_energy(time_values, angle_values, velocity_values, length, mass, method):
    angle_values, velocity_values = np.array(angle_values), np.array(velocity_values)
    kinetic_energy = 0.5 * mass * (length * velocity_values) ** 2
    potential_energy = mass * g * length * (1 - np.cos(angle_values))
    total_energy = kinetic_energy + potential_energy
    plt.plot(time_values, kinetic_energy, label=f'{method} - Kinetic Energy')
    plt.plot(time_values, potential_energy, label=f'{method} - Potential Energy')
    plt.plot(time_values, total_energy, label=f'{method} - Total Energy')
    plt.legend()
    plt.title(f'Energy over Time - {method}')
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.show()

def draw_graph(angle_values, length, method):
    x_values, y_values = length * np.sin(angle_values), -length * np.cos(angle_values)
    plt.plot(x_values, y_values, label=f'{method} - Trajectory')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.title(f'Trajectory - {method}')
    plt.show()

if __name__ == '__main__':
    mass = 1.0
    methods = [euler_method, midpoint_method, rk4_method]
    for method in methods:
        time_values, angle_values, velocity_values, method_name = method(initial_angle, initial_velocity, time_step)
        display_energy(time_values, angle_values, velocity_values, length, mass, method_name)
        draw_graph(angle_values, length, method_name)
