import matplotlib.pyplot as plt
import numpy as np
import warnings

def lorenz_system(state, A, B, C):
    x, y, z = state.astype(np.float64)
    try:
        dx_dt = A * (y - x)
        dy_dt = -x * z + B * x - y
        dz_dt = x * y - C * z

        if np.any(np.isinf([dx_dt, dy_dt, dz_dt])) or np.any(np.isnan([dx_dt, dy_dt, dz_dt])):
            raise OverflowError("Derivative calculation resulted in overflow or NaN.")
        return np.array([dx_dt, dy_dt, dz_dt], dtype=np.float64)
    except OverflowError:

        warnings.warn("Overflow encountered in lorenz_system calculation.", RuntimeWarning)
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)


def euler_step(func, state, dt, A, B, C):
    if np.any(np.isnan(state)):
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    derivatives = func(state, A, B, C)

    if np.any(np.isnan(derivatives)):
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    next_state = state + dt * derivatives

    if np.any(np.isinf(next_state)) or np.any(np.isnan(next_state)):
        warnings.warn(f"Overflow or NaN detected in euler_step.", RuntimeWarning)
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)
    return next_state


def midpoint_step(func, state, dt, A, B, C):
    if np.any(np.isnan(state)):
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    k1 = dt * func(state, A, B, C)
    if np.any(np.isnan(k1)): return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    mid_state = state + k1 / 2.0
    if np.any(np.isinf(mid_state)) or np.any(np.isnan(mid_state)):
        warnings.warn(f"Overflow or NaN detected during midpoint calculation (mid_state).", RuntimeWarning)
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    k2 = dt * func(mid_state, A, B, C)
    if np.any(np.isnan(k2)): return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    next_state = state + k2
    if np.any(np.isinf(next_state)) or np.any(np.isnan(next_state)):
        warnings.warn(f"Overflow or NaN detected in midpoint_step.", RuntimeWarning)
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)
    return next_state


def is_invalid(arr):
    return np.any(np.isinf(arr)) or np.any(np.isnan(arr))


def calculate_k_value(func, state_for_eval, dt, A, B, C):
    if is_invalid(state_for_eval):
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    derivs = func(state_for_eval, A, B, C)

    if is_invalid(derivs):
        warnings.warn(f"Derivative calculation (func) returned NaN/Inf.", RuntimeWarning)
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    k = dt * derivs

    if is_invalid(k):
        warnings.warn(f"Calculated k value became NaN/Inf.", RuntimeWarning)
        return np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    return k


def rk4_step(func, state, dt, A, B, C):
    nan_array = np.array([np.nan, np.nan, np.nan], dtype=np.float64)

    if is_invalid(state):
        warnings.warn("Initial state for rk4_step is invalid.", RuntimeWarning)
        return nan_array

    k1 = calculate_k_value(func, state, dt, A, B, C)
    if is_invalid(k1): return nan_array

    state_for_k2 = state + k1 / 2.0
    k2 = calculate_k_value(func, state_for_k2, dt, A, B, C)
    if is_invalid(k2): return nan_array

    state_for_k3 = state + k2 / 2.0
    k3 = calculate_k_value(func, state_for_k3, dt, A, B, C)
    if is_invalid(k3): return nan_array

    state_for_k4 = state + k3
    k4 = calculate_k_value(func, state_for_k4, dt, A, B, C)
    if is_invalid(k4): return nan_array

    next_state = state + (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0

    if is_invalid(next_state):
        warnings.warn(f"Final next_state calculation resulted in NaN/Inf in rk4_step.", RuntimeWarning)
        return nan_array

    return next_state


def solve_lorenz(method_step, initial_state, dt, num_steps, A, B, C):
    x_vals = np.zeros(num_steps + 1, dtype=np.float64)
    y_vals = np.zeros(num_steps + 1, dtype=np.float64)
    z_vals = np.zeros(num_steps + 1, dtype=np.float64)

    current_state = np.array(initial_state, dtype=np.float64)
    x_vals[0], y_vals[0], z_vals[0] = current_state

    print(f"Running simulation with method: {method_step.__name__}...")
    nan_encountered = False
    for i in range(num_steps):
        if (i + 1) % (num_steps // 10) == 0 or i == num_steps - 1:
            print(f"  Step {i + 1}/{num_steps}")

        current_state = method_step(lorenz_system, current_state, dt, A, B, C)

        if np.any(np.isnan(current_state)):
            warnings.warn(f"NaN detected at step {i + 1}. Stopping simulation for {method_step.__name__}.",
                          RuntimeWarning)

            x_vals[i + 1:] = np.nan
            y_vals[i + 1:] = np.nan
            z_vals[i + 1:] = np.nan
            nan_encountered = True
            break  # Exit the loop

        x_vals[i + 1], y_vals[i + 1], z_vals[i + 1] = current_state

    if not nan_encountered:
        print("Simulation complete.")
    else:
        print("Simulation stopped early due to numerical instability (NaN/Overflow).")
    return x_vals, y_vals, z_vals


def plot_results(x_vals, z_vals, title):
    print(f"Generating plot: {title}")
    plt.figure(figsize=(8, 6))

    valid_indices = ~np.isnan(x_vals) & ~np.isnan(z_vals)
    if np.count_nonzero(valid_indices) > 1:
        plt.plot(x_vals[valid_indices], z_vals[valid_indices], lw=0.5)
    else:
        print(f"Warning: Not enough valid data points to plot for '{title}'.")
    plt.xlabel("x(t)")
    plt.ylabel("z(t)")
    plt.title(title)
    plt.grid(True)


def main():
    print("--- Lorenz System Solver ---")

    with warnings.catch_warnings():
        warnings.simplefilter("always", RuntimeWarning)

        A = 10.0
        B = 25.0
        C = 8.0 / 3.0
        initial_state = [1.0, 1.0, 1.0]

        dt = 0.01
        t_max = 60.0
        num_steps = int(t_max / dt)

        print("\nParameters:")
        print(f"  A = {A}, B = {B}, C = {C:.4f}")
        print(f"  Initial State (x0, y0, z0) = {initial_state}")
        print(f"  Time Step (dt) = {dt}")
        print(f"  Total Simulation Time = {t_max}")
        print(f"  Number of Steps = {num_steps}\n")

        x_euler, y_euler, z_euler = solve_lorenz(
            euler_step, initial_state, dt, num_steps, A, B, C
        )
        plot_results(x_euler, z_euler, f"Lorenz Attractor (z vs x) - Euler Method (dt={dt})")

        x_midpoint, y_midpoint, z_midpoint = solve_lorenz(
            midpoint_step, initial_state, dt, num_steps, A, B, C
        )
        plot_results(x_midpoint, z_midpoint, f"Lorenz Attractor (z vs x) - Midpoint Method (dt={dt})")

        x_rk4, y_rk4, z_rk4 = solve_lorenz(
            rk4_step, initial_state, dt, num_steps, A, B, C
        )
        plot_results(x_rk4, z_rk4, f"Lorenz Attractor (z vs x) - RK4 Method (dt={dt})")

        print("\nDisplaying plots...")
        plt.show()
        print("--- Program Finished ---")


if __name__ == "__main__":
    main()
