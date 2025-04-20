import numpy as np
import matplotlib.pyplot as plt
from math import pi
import time


class WaveParams:
    def __init__(self, length, segments, speed, dt, t_end, amp):
        self.length = length
        self.segments = segments
        self.speed = speed
        self.dt = dt
        self.t_end = t_end
        self.amp = amp

    def points(self):
        return self.segments + 1

    def spacing(self):
        return self.length / self.segments

    def speed_sq(self):
        return self.speed ** 2


class StepData:
    def __init__(self, time, disp, vel, ek, ep, et):
        self.time = time
        self.disp = disp
        self.vel = vel
        self.ek = ek
        self.ep = ep
        self.et = et


def init_wave(params):
    n = params.points()
    dx = params.spacing()
    disp = np.zeros(n)
    vel = np.zeros(n)
    for i in range(1, params.segments):
        x = i * dx
        disp[i] = params.amp * np.sin(pi * x / params.length)
    ek, ep, et = compute_energies(disp, vel, params)
    return StepData(0.0, disp, vel, ek, ep, et)


def compute_accel(disp, params):
    n = params.points()
    a = np.zeros(n)
    dx2 = params.spacing() ** 2
    c2 = params.speed_sq()
    for i in range(1, params.segments):
        a[i] = c2 * (disp[i - 1] - 2 * disp[i] + disp[i + 1]) / dx2
    return a


def compute_energies(disp, vel, params):
    dx = params.spacing()
    ke = np.sum(0.5 * dx * vel ** 2)
    pe = np.sum((disp[1:] - disp[:-1]) ** 2) / (2 * dx)
    return ke, pe, ke + pe


def midpoint_integrate(state, params):
    dt = params.dt
    a1 = compute_accel(state.disp, params)
    disp_mid = state.disp + state.vel * (dt / 2)
    vel_mid = state.vel + a1 * (dt / 2)
    a2 = compute_accel(disp_mid, params)
    disp_new = state.disp + vel_mid * dt
    vel_new = state.vel + a2 * dt
    ek, ep, et = compute_energies(disp_new, vel_new, params)
    return StepData(state.time + dt, disp_new, vel_new, ek, ep, et)


def record_history(params):
    state = init_wave(params)
    history = [state]
    steps = int(np.ceil(params.t_end / params.dt))
    for _ in range(steps):
        state = midpoint_integrate(state, params)
        history.append(state)
    return history


def display_params(params):
    dx = params.spacing()
    cfl = params.speed * params.dt / dx
    print(f"L={params.length:.3f}, N={params.segments}, c={params.speed:.1f}")
    print(f"dx={dx:.4e}, dt={params.dt:.4e}, T_end={params.t_end:.2f}")
    print(f"CFL={cfl:.3f}")
    if cfl > 1.0:
        print("Warning: CFL>1 unstable")


def time_simulation(params):
    start = time.time()
    hist = record_history(params)
    print(f"Sim time: {time.time() - start:.2f}s")
    return hist


def plot_wave_energy(history):
    t = [s.time for s in history]
    ke = [s.ek for s in history]
    pe = [s.ep for s in history]
    te = [s.et for s in history]
    plt.figure()
    plt.plot(t, ke, label='KE')
    plt.plot(t, pe, label='PE')
    plt.plot(t, te, label='TE')
    plt.xlabel('t (s)')
    plt.ylabel('Energy')
    plt.legend()
    plt.tight_layout()
    plt.show()


def run():
    params = WaveParams(
        length=pi,
        segments=10,
        speed=1.0,
        dt=0.001,
        t_end=10.0,
        amp=10.0
    )
    display_params(params)
    history = time_simulation(params)
    plot_wave_energy(history)


if __name__ == "__main__":
    run()
