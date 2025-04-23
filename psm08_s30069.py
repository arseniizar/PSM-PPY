import warnings
import matplotlib.pyplot as plt
import numpy as np


def lorenz_derivative(state, A, B, C):
    x, y, z = state
    return np.array([
        A * (y - x),
        B * x - y - x * z,
        x * y - C * z
    ], dtype=float)


def euler_step(state, dt, A, B, C):
    return state + dt * lorenz_derivative(state, A, B, C)


def midpoint_step(state, dt, A, B, C):
    k1 = lorenz_derivative(state, A, B, C)
    mid = state + 0.5 * dt * k1
    k2 = lorenz_derivative(mid, A, B, C)
    return state + dt * k2


def rk4_step(state, dt, A, B, C):
    k1 = lorenz_derivative(state, A, B, C)
    k2 = lorenz_derivative(state + 0.5 * dt * k1, A, B, C)
    k3 = lorenz_derivative(state + 0.5 * dt * k2, A, B, C)
    k4 = lorenz_derivative(state + dt * k3, A, B, C)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate(method, initial, dt, steps, A, B, C):
    x = np.empty(steps + 1)
    z = np.empty(steps + 1)
    state = np.array(initial, dtype=float)
    x[0], z[0] = state[0], state[2]

    for i in range(1, steps + 1):
        state = method(state, dt, A, B, C)
        if np.any(np.isnan(state)):
            x[i:], z[i:] = np.nan, np.nan
            print(f"  [{method.__name__}] NaN at step {i}, aborting.")
            break
        x[i], z[i] = state[0], state[2]

    return x, z


def plot_attractor(x, z, label):
    plt.plot(x, z, lw=0.5, label=label)


def show_plots():
    plt.xlabel("x")
    plt.ylabel("z")
    plt.legend()
    plt.grid(True)
    plt.show()


def get_params():
    return {
        "A": 10.0,
        "B": 28.0,
        "C": 8.0 / 3.0,
        "initial": [1.0, 1.0, 1.0],
        "dt": 0.01,
        "t_max": 30.0
    }


def display_params(params):
    steps = int(params["t_max"] / params["dt"])
    print("Lorenz System Parameters:")
    print(f"  A={params['A']}, B={params['B']}, C={params['C']:.4f}")
    print(f"  initial={params['initial']}")
    print(f"  dt={params['dt']}, steps={steps}\n")


def main():
    params = get_params()
    display_params(params)
    steps = int(params["t_max"] / params["dt"])

    methods = [euler_step, midpoint_step, rk4_step]
    plt.figure(figsize=(8, 6))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for m in methods:
            print(f"Running {m.__name__}...")
            x, z = simulate(m, params["initial"], params["dt"],
                            steps, params["A"], params["B"], params["C"])
            plot_attractor(x, z, m.__name__)

    print("Simulation complete, displaying plots.")
    show_plots()


if __name__ == "__main__":
    main()
