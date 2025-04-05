import numpy as np
import matplotlib.pyplot as plt

KM_TO_M = 1000.0
HOUR_TO_S = 3600.0
DAY_TO_S = 24 * HOUR_TO_S
YEAR_TO_S = 365.25 * DAY_TO_S

DEFAULT_VALUES = {
    "G": 6.6743e-11,
    "Ms": 1.989e30,
    "Mz": 5.972e24,
    "Mk": 7.347e22,
    "R_ZS_km": 1.5e8,
    "R_ZK_km": 384400,
    "dt_hours": 1.0,
    "T_days": 365.25
}


def input_parameter(prompt, default, factor=1.0):
    try:
        value_str = input(f"{prompt} [{default}]: ")
        return float(value_str) * factor if value_str else default * factor
    except ValueError:
        return default * factor


def get_simulation_parameters(defaults):
    params = {}
    print("Enter simulation parameters (leave blank to use defaults):")
    params['G'] = input_parameter("Gravitational constant G (Nm^2/kg^2)", defaults['G'])
    params['Ms'] = input_parameter("Mass of Sun Ms (kg)", defaults['Ms'])
    params['Mz'] = input_parameter("Mass of Earth Mz (kg)", defaults['Mz'])
    params['Mk'] = input_parameter("Mass of Moon Mk (kg)", defaults['Mk'])
    params['R_ZS'] = input_parameter("Earth-Sun distance R_ZS (km)", defaults['R_ZS_km'], KM_TO_M)
    params['R_ZK'] = input_parameter("Earth-Moon distance R_ZK (km)", defaults['R_ZK_km'], KM_TO_M)
    params['dt'] = input_parameter("Time step dt (hours)", defaults['dt_hours'], HOUR_TO_S)
    params['T'] = input_parameter("Total simulation time T (days)", defaults['T_days'], DAY_TO_S)
    print("\nUsing Parameters:")
    print(f"  G    = {params['G']:.4e} Nm^2/kg^2")
    print(f"  Ms   = {params['Ms']:.3e} kg")
    print(f"  Mz   = {params['Mz']:.3e} kg")
    print(f"  Mk   = {params['Mk']:.3e} kg")
    print(f"  R_ZS = {params['R_ZS']:.3e} m")
    print(f"  R_ZK = {params['R_ZK']:.3e} m")
    print(f"  dt   = {params['dt']:.1f} s ({params['dt'] / HOUR_TO_S:.2f} hours)")
    print(f"  T    = {params['T']:.3e} s ({params['T'] / DAY_TO_S:.2f} days)")
    print("-" * 20)
    return params


def get_earth_initial_conditions(params):
    G, Ms, R_ZS = params['G'], params['Ms'], params['R_ZS']
    position = np.array([R_ZS, 0.0])
    speed = np.sqrt(G * Ms / R_ZS)
    velocity = np.array([0.0, speed])
    return position, velocity


def get_moon_initial_conditions(params, earth_position, earth_velocity):
    G, Mz, R_ZK = params['G'], params['Mz'], params['R_ZK']
    rel_position = np.array([R_ZK, 0.0])
    rel_speed = np.sqrt(G * Mz / R_ZK)
    rel_velocity = np.array([0.0, rel_speed])
    position = earth_position + rel_position
    velocity = earth_velocity + rel_velocity
    return position, velocity


def calculate_initial_positions_velocities(params):
    earth_pos, earth_vel = get_earth_initial_conditions(params)
    moon_pos, moon_vel = get_moon_initial_conditions(params, earth_pos, earth_vel)
    return np.concatenate((earth_pos, earth_vel, moon_pos, moon_vel))


def compute_earth_acceleration(earth_position, G, Ms):
    r = np.linalg.norm(earth_position)
    return -G * Ms * earth_position / (r ** 3) if r != 0 else np.zeros(2)


def compute_moon_acceleration(moon_position, earth_position, G, Ms, Mz):
    r_moon = np.linalg.norm(moon_position)
    r_vector = moon_position - earth_position
    r_em = np.linalg.norm(r_vector)
    acc_from_sun = -G * Ms * moon_position / (r_moon ** 3) if r_moon != 0 else np.zeros(2)
    acc_from_earth = -G * Mz * r_vector / (r_em ** 3) if r_em != 0 else np.zeros(2)
    return acc_from_sun + acc_from_earth


def calculate_gravitational_derivatives(state, t, G, Ms, Mz, Mk):
    earth_pos = state[0:2]
    earth_vel = state[2:4]
    moon_pos = state[4:6]
    moon_vel = state[6:8]
    earth_acc = compute_earth_acceleration(earth_pos, G, Ms)
    moon_acc = compute_moon_acceleration(moon_pos, earth_pos, G, Ms, Mz)
    return np.concatenate((earth_vel, earth_acc, moon_vel, moon_acc))


def perform_improved_euler_step(state, t, dt, deriv_func, G, Ms, Mz, Mk):
    k1 = dt * deriv_func(state, t, G, Ms, Mz, Mk)
    midpoint_state = state + k1 / 2.0
    k2 = dt * deriv_func(midpoint_state, t + dt / 2.0, G, Ms, Mz, Mk)
    return state + k2


def simulation_loop(state, t, dt, T, deriv_func, G, Ms, Mz, Mk):
    times = [t]
    history = [state]
    n_steps = int(T / dt)
    for i in range(n_steps):
        state = perform_improved_euler_step(state, t, dt, deriv_func, G, Ms, Mz, Mk)
        t += dt
        history.append(state)
        times.append(t)
        if (i + 1) % (n_steps // 20) == 0:
            print(f"  Progress: {100 * (i + 1) / n_steps:.1f}%")
    return times, np.array(history)


def run_simulation(params, initial_state):
    G, Ms, Mz, Mk = params['G'], params['Ms'], params['Mz'], params['Mk']
    dt, T = params['dt'], params['T']
    print("Running simulation...")
    times, states = simulation_loop(initial_state, 0.0, dt, T, calculate_gravitational_derivatives, G, Ms, Mz, Mk)
    print("Simulation complete.")
    return times, states


def extract_trajectories(states_array):
    earth_x = states_array[:, 0]
    earth_y = states_array[:, 1]
    moon_x = states_array[:, 4]
    moon_y = states_array[:, 5]
    return earth_x, earth_y, moon_x, moon_y


def plot_full_view(params, earth_x, earth_y, moon_x, moon_y):
    plt.figure(figsize=(10, 10))
    plt.plot(0, 0, 'yo', markersize=15, label='Sun')
    plt.plot(earth_x, earth_y, 'b-', label="Earth's Path", linewidth=1)
    plt.plot(earth_x[-1], earth_y[-1], 'bo', markersize=8, label='Earth (Final)')
    plt.plot(moon_x, moon_y, 'grey', label="Moon's Path", linewidth=0.5)
    plt.plot(moon_x[-1], moon_y[-1], 'ko', markersize=5, label='Moon (Final)')
    plt.title('Trajectory of Moon Relative to Sun (Full View)')
    plt.xlabel('X Position (meters)')
    plt.ylabel('Y Position (meters)')
    plt.legend()
    plt.grid(True)
    limit = params['R_ZS'] * 1.2
    plt.xlim(-limit, limit)
    plt.ylim(-limit, limit)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def plot_zoomed_view(params, earth_x, earth_y, moon_x, moon_y):
    plt.figure(figsize=(8, 8))
    final_earth_x = earth_x[-1]
    final_earth_y = earth_y[-1]
    zoom_radius = params['R_ZK'] * 5
    num_total_points = len(earth_x)
    num_zoom_points = max(10, num_total_points // 12)
    start_index = -num_zoom_points
    plt.plot(earth_x[start_index:], earth_y[start_index:], 'b-', label="Earth's Path (Zoomed)", linewidth=1)
    plt.plot(moon_x[start_index:], moon_y[start_index:], 'grey', label="Moon's Path (Zoomed)", linewidth=1)
    plt.plot(final_earth_x, final_earth_y, 'bo', markersize=10, label='Earth (Final)')
    plt.plot(moon_x[-1], moon_y[-1], 'ko', markersize=6, label='Moon (Final)')
    plt.plot(0, 0, 'yo', markersize=5, label='Sun (Likely off-screen)')
    plt.title('Trajectory of Moon Relative to Sun (Zoomed View Near Earth)')
    plt.xlabel('X Position (meters)')
    plt.ylabel('Y Position (meters)')
    plt.xlim(final_earth_x - zoom_radius, final_earth_x + zoom_radius)
    plt.ylim(final_earth_y - zoom_radius, final_earth_y + zoom_radius)
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def plot_moon_relative_view(params, earth_x, earth_y, moon_x, moon_y):
    plt.figure(figsize=(8, 8))
    rel_x = moon_x - earth_x
    rel_y = moon_y - earth_y
    plt.plot(0, 0, 'bo', markersize=10, label='Earth (Origin)')
    plt.plot(rel_x, rel_y, 'grey', label="Moon's Orbit around Earth", linewidth=1)
    plt.plot(rel_x[-1], rel_y[-1], 'ko', markersize=5, label='Moon (Final Relative Position)')
    plt.title('Trajectory of Moon Relative to Earth')
    plt.xlabel('Relative X Position to Earth (meters)')
    plt.ylabel('Relative Y Position to Earth (meters)')
    limit_rel = params['R_ZK'] * 1.5
    plt.xlim(-limit_rel, limit_rel)
    plt.ylim(-limit_rel, limit_rel)
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def plot_system_trajectories(params, earth_x, earth_y, moon_x, moon_y):
    plot_full_view(params, earth_x, earth_y, moon_x, moon_y)
    plot_zoomed_view(params, earth_x, earth_y, moon_x, moon_y)
    plot_moon_relative_view(params, earth_x, earth_y, moon_x, moon_y)


def main():
    sim_params = get_simulation_parameters(DEFAULT_VALUES)
    init_state = calculate_initial_positions_velocities(sim_params)
    sim_times, states_history = run_simulation(sim_params, init_state)
    earth_x, earth_y, moon_x, moon_y = extract_trajectories(states_history)
    plot_system_trajectories(sim_params, earth_x, earth_y, moon_x, moon_y)

main()