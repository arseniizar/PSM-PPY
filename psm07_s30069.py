import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def convert_hex_to_rgb(hex_str: str) -> tuple[float, ...]:
    return tuple(int(hex_str[i: i + 2], 16) / 255 for i in (0, 2, 4))


def create_thermal_cmap(colors: list[str | tuple[float, float, float]]) -> LinearSegmentedColormap:
    rgb_list = [convert_hex_to_rgb(c) if isinstance(c, str) else c for c in colors]
    stops = np.linspace(0, 1, len(rgb_list))
    return LinearSegmentedColormap.from_list("thermal", list(zip(stops, rgb_list)))


def relax_to_convergence(
        grid: np.ndarray,
        max_iter: int = 5000,
        tol: float = 1e-4
) -> np.ndarray:
    for _ in range(max_iter):
        old = grid.copy()
        grid[1:-1, 1:-1] = 0.25 * (
                old[:-2, 1:-1] + old[2:, 1:-1] +
                old[1:-1, :-2] + old[1:-1, 2:]
        )
        if np.max(np.abs(grid - old)) < tol:
            break
    return grid


def compute_steady_state_temperature(
        width: int,
        height: int,
        top_temp: float,
        right_temp: float,
        bottom_temp: float,
        left_temp: float,
) -> np.ndarray:
    grid = np.zeros((height, width), float)
    grid[0, 1:-1] = bottom_temp
    grid[-1, 1:-1] = top_temp
    grid[1:-1, 0] = left_temp
    grid[1:-1, -1] = right_temp
    grid[0, 0] = (bottom_temp + left_temp) / 2
    grid[0, -1] = (bottom_temp + right_temp) / 2
    grid[-1, 0] = (top_temp + left_temp) / 2
    grid[-1, -1] = (top_temp + right_temp) / 2
    avg = (top_temp + right_temp + bottom_temp + left_temp) / 4
    grid[1:-1, 1:-1] = avg
    return relax_to_convergence(grid)


def display_temperature_map(
        grid: np.ndarray,
        cmap: LinearSegmentedColormap,
        title: str = "Steady-State Temperature"
) -> None:
    plt.figure(figsize=(8, 6))
    img = plt.imshow(grid, cmap=cmap, origin="lower", interpolation="nearest")
    cbar = plt.colorbar(img, pad=0.02)
    cbar.set_label("Temperature")
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.tight_layout()
    plt.show()


def main():
    grid_w, grid_h = 40, 40
    top_T = 100.0
    right_T = 150.0
    bottom_T = 50.0
    left_T = 200.0

    print(f"Computing temperature on {grid_w}×{grid_h} grid...")
    temp_grid = compute_steady_state_temperature(
        grid_w, grid_h, top_T, right_T, bottom_T, left_T
    )

    cmap = create_thermal_cmap(["66CC66", "FFFF00", "FF0000"])
    display_temperature_map(temp_grid, cmap)


if __name__ == "__main__":
    main()
