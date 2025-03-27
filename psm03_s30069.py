import math
import matplotlib.pyplot as plt
import numpy as np

g_const = 9.81
t_final = 10
dt = 0.01
num_steps = int(t_final / dt) + 1

m = 0
L = 1.0
start_angle = math.pi / 4
start_velocity = 0.0
method_name = ''


def dynamics(a, v):
    w = v
    eps = -(g_const / L) * np.sin(a)
    return w, eps


def euler_integration(a, v):
    w, eps = dynamics(a, v)
    return a + w * dt, v + eps * dt


def midpoint_integration(a, v):
    w1, e1 = dynamics(a, v)
    a_mid = a + 0.5 * w1 * dt
    v_mid = v + 0.5 * e1 * dt
    w2, e2 = dynamics(a_mid, v_mid)
    return a + w2 * dt, v + e2 * dt


def rk4_integration(a, v):
    w1, e1 = dynamics(a, v)
    w2, e2 = dynamics(a + 0.5 * dt * w1, v + 0.5 * dt * e1)
    w3, e3 = dynamics(a + 0.5 * dt * w2, v + 0.5 * dt * e2)
    w4, e4 = dynamics(a + dt * w3, v + dt * e3)
    return (a + (dt / 6) * (w1 + 2 * w2 + 2 * w3 + w4),
            v + (dt / 6) * (e1 + 2 * e2 + 2 * e3 + e4))


def run_simulation(func, a, v):
    t = 0.0
    t_vals = [t]
    a_vals = [a]
    v_vals = [v]
    for _ in range(num_steps):
        a, v = func(a, v)
        t += dt
        t_vals.append(t)
        a_vals.append(a)
        v_vals.append(v)
    return t_vals, a_vals, v_vals


def plot_outcome(ts, as_, vs):
    arr_a = np.array(as_)
    arr_v = np.array(vs)
    ke = 0.5 * m * (L * arr_v) ** 2
    pe = m * g_const * L * (1 - np.cos(arr_a))
    te = ke + pe
    fig, axx = plt.subplots(1, 2, figsize=(12, 5))
    axx[0].plot(ts, ke, label='Kinetic')
    axx[0].plot(ts, pe, label='Potential')
    axx[0].plot(ts, te, label='Total')
    axx[0].set_title(f'Energy - {method_name}')
    axx[0].set_xlabel('Time (s)')
    axx[0].set_ylabel('Energy (J)')
    axx[0].legend()
    xs = L * np.sin(arr_a)
    ys = -L * np.cos(arr_a)
    axx[1].plot(xs, ys, label='Path')
    axx[1].set_title(f'Trajectory - {method_name}')
    axx[1].set_xlabel('X (m)')
    axx[1].set_ylabel('Y (m)')
    axx[1].legend()
    plt.tight_layout()
    plt.show()


def select_method(num):
    global method_name
    if num == 1:
        method_name = 'Euler'
        f = euler_integration
    elif num == 2:
        method_name = 'Midpoint'
        f = midpoint_integration
    elif num == 3:
        method_name = 'RK4'
        f = rk4_integration
    else:
        print("Invalid choice.")
        return
    ts, angs, vels = run_simulation(f, start_angle, start_velocity)
    plot_outcome(ts, angs, vels)


def ask_for_value(txt, conv, cond=lambda x: True, err="Invalid input"):
    while True:
        try:
            val = conv(input(txt))
            if not cond(val):
                print(err)
                continue
            return val
        except ValueError:
            print(err)


def main():
    global m, L, start_angle, start_velocity
    m = ask_for_value("Mass: ", float, lambda x: x > 0, "Must be > 0")
    L = ask_for_value("Length: ", float, lambda x: x > 0, "Must be > 0")
    deg_a = ask_for_value("Angle (deg): ", float)
    start_angle = math.radians(deg_a)
    start_velocity = ask_for_value("Velocity: ", float)
    choice = ask_for_value("Method (1=Euler,2=Midpoint,3=RK4): ", int,
                           lambda x: x in [1, 2, 3], "Enter 1,2,or 3")
    select_method(choice)


main()
