import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def get_cell_type(point, width, height):
    x, y = point
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    if (x, y) in corners:
        return "corner"
    if x == 0:
        return "left"
    if x == width - 1:
        return "right"
    if y == 0:
        return "bottom"
    if y == height - 1:
        return "top"
    return None


def generate_table(width, height, boundaries):
    total_cells = (width - 2) * (height - 2)
    A = np.zeros((total_cells, total_cells))
    b = np.zeros(total_cells)

    index_map = {}
    idx = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            index_map[(x, y)] = idx
            idx += 1

    for (x, y), idx in index_map.items():
        A[idx, idx] = -4
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            neighbor_type = get_cell_type((new_x, new_y), width, height)

            if neighbor_type is None:
                A[idx, index_map[(new_x, new_y)]] = 1
            elif neighbor_type != "corner":
                b[idx] -= boundaries[neighbor_type]
    return A, b


def calculate_heat_grid(width=40, height=40, top=100, right=150, bottom=50, left=200):
    boundaries = {
        "top": top,
        "right": right,
        "bottom": bottom,
        "left": left
    }

    A, b = generate_table(width, height, boundaries)
    X = np.linalg.solve(A, b)

    grid = np.empty((height, width))
    grid.fill(np.nan)
    grid[0, 1:-1] = bottom
    grid[-1, 1:-1] = top
    grid[1:-1, 0] = left
    grid[1:-1, -1] = right

    idx = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y, x] = X[idx]
            idx += 1
    return grid


def create_colormap(colors):
    def hex_to_rgb(hex_str):
        return tuple(int(hex_str[i:i + 2], 16) / 255 for i in (0, 2, 4))

    rgb_colors = []
    for color in colors:
        if isinstance(color, str):
            rgb_colors.append(hex_to_rgb(color))
        else:
            rgb_colors.append(color)
    positions = np.linspace(0, 1, len(colors))
    return LinearSegmentedColormap.from_list("ThermalGradient", list(zip(positions, rgb_colors)))


def show_temperature():
    grid = calculate_heat_grid()
    cmap = create_colormap([(0.4, 0.8, 0.4), (1, 1, 0), (1, 0, 0)])

    plt.figure(figsize=(10, 10))
    img = plt.imshow(grid, cmap=cmap, interpolation="nearest")

    cbar = plt.colorbar(img)
    cbar.set_label("Temperature", rotation=270, labelpad=20)

    plt.gca().invert_yaxis()
    plt.title("Temperature distribution")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


if __name__ == "__main__":
    show_temperature()
