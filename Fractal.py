import argparse
from itertools import cycle

import matplotlib.colors as clr
import matplotlib.pyplot as plt
import numpy as np

REAL_MIN, REAL_MAX, IMAG_MIN, IMAG_MAX = -2.5, 1.5, -2, 2
HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION = 1000, 1000
MAX_ITERATIONS = 300
ESCAPE_RADIUS = 10
POWER = 2
C_VALUE = 0 + 0j
ZOOM = False
ZOOM_CENTER = -0.793191078177363 + 0.16093721735804j
ZOOM_LEVELS = 10
ZOOM_FACTOR = 12000.0


def generate_fractal(
    real_min: float,
    real_max: float,
    hor_res: int,
    imag_min: float,
    imag_max: float,
    ver_res: int,
    max_iterations: int = 200,
    escape_radius: float = 10,
    power: int = 2,
    c_value: complex = 0 + 0j,
) -> np.ndarray:
    """
    Generate a fractal set for a given range of complex numbers with custom parameters.

    Parameters:
    - real_min, real_max: float, range for the real part of the complex number
    - imag_min, imag_max: float, range for the imaginary part of the complex number
    - hor_res, ver_res: int, resolution of the grid
    - max_iterations: int, maximum number of iterations
    - escape_radius: float, threshold to consider a point as escaping to infinity
    - power: int, the power to which the complex number is raised
    - c_value: complex, constant value to add in each iteration (used for Julia sets)

    Returns:
    - np.ndarray: 2D array representing the fractal set
    """
    fractal_image = np.zeros((hor_res, ver_res))
    real_axis, imag_axis = np.mgrid[
        real_min: real_max: (hor_res * 1j), imag_min: imag_max: (ver_res * 1j)
    ]
    complex_grid = real_axis + 1j * imag_axis
    z = np.zeros_like(complex_grid) if c_value == 0 else complex_grid

    for iteration in range(max_iterations):
        z = z**power + c_value if c_value != 0 else z**power + complex_grid
        mask = (np.abs(z) > escape_radius) & (fractal_image == 0)
        fractal_image[mask] = iteration
        z[mask] = np.nan

    return -fractal_image.T


def plot_and_save_fractal(image: np.ndarray, colormap: str, filename: str) -> None:
    """
    Plot and save the fractal set image.

    Parameters:
    - image: np.ndarray, the image data of the fractal set
    - colormap: str, the colormap to use for plotting
    - filename: str, the filename to save the image
    """
    plt.figure(figsize=(10, 10))
    plt.xticks([])
    plt.yticks([])
    plt.imshow(image, cmap=colormap, interpolation="none")
    plt.savefig(filename)
    print(f"{filename} saved")


def main():
    parser = argparse.ArgumentParser(description="Generate and save fractal images.")
    parser.add_argument(
        "--real_min", type=float, default=REAL_MIN, help="Minimum real axis value."
    )
    parser.add_argument(
        "--real_max", type=float, default=REAL_MAX, help="Maximum real axis value."
    )
    parser.add_argument(
        "--imag_min", type=float, default=IMAG_MIN, help="Minimum imaginary axis value."
    )
    parser.add_argument(
        "--imag_max", type=float, default=IMAG_MAX, help="Maximum imaginary axis value."
    )
    parser.add_argument(
        "--hor_res",
        type=int,
        default=HORIZONTAL_RESOLUTION,
        help="Horizontal resolution.",
    )
    parser.add_argument(
        "--ver_res", type=int, default=VERTICAL_RESOLUTION, help="Vertical resolution."
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=MAX_ITERATIONS,
        help="Maximum number of iterations.",
    )
    parser.add_argument(
        "--escape_radius", type=float, default=ESCAPE_RADIUS, help="Escape radius."
    )
    parser.add_argument(
        "--power", type=int, default=POWER, help="Power to raise the complex number."
    )
    parser.add_argument(
        "--c_value",
        type=complex,
        default=C_VALUE,
        help="Constant value for Julia sets.",
    )
    parser.add_argument(
        "--zoom",
        action="store_true",
        default=ZOOM,
        help="Enable zoom into a specific region.",
    )
    parser.add_argument(
        "--zoom_center",
        type=complex,
        default=ZOOM_CENTER,
        help="Center point for zooming.",
    )
    parser.add_argument(
        "--zoom_levels", type=int, default=ZOOM_LEVELS, help="Number of zoom levels."
    )
    parser.add_argument(
        "--zoom_factor",
        type=float,
        default=ZOOM_FACTOR,
        help="Factor by which to zoom.",
    )

    args = parser.parse_args()

    color_points = [
        (1 - (1 - val) ** 4, color)
        for val, color in zip(
            np.linspace(0, 1, 20), cycle(["#ffff88", "#000000", "#ffaa00"])
        )
    ]
    custom_colormap = clr.LinearSegmentedColormap.from_list(
        "custom_colormap", color_points, N=2048
    )

    fractal_image = generate_fractal(
        args.real_min,
        args.real_max,
        args.hor_res,
        args.imag_min,
        args.imag_max,
        args.ver_res,
        args.max_iterations,
        args.escape_radius,
        args.power,
        args.c_value,
    )
    plot_and_save_fractal(fractal_image, custom_colormap, "fractal.png")

    if args.zoom:
        real_center, imag_center = args.zoom_center.real, args.zoom_center.imag
        for i in range(1, args.zoom_levels + 1):
            scale_factor = i / args.zoom_factor
            real_min_scaled = (args.real_min - real_center) * scale_factor + real_center
            imag_min_scaled = (args.imag_min - imag_center) * scale_factor + imag_center
            real_max_scaled = (args.real_max - real_center) * scale_factor + real_center
            imag_max_scaled = (args.imag_max - imag_center) * scale_factor + imag_center

            zoomed_fractal_image = generate_fractal(
                real_min_scaled,
                real_max_scaled,
                500,
                imag_min_scaled,
                imag_max_scaled,
                500,
                args.max_iterations,
                args.escape_radius,
                args.power,
                args.c_value,
            )
            filename = f"fractal-zoom-{i}.png"
            plot_and_save_fractal(zoomed_fractal_image, "flag", filename)


if __name__ == "__main__":
    main()
