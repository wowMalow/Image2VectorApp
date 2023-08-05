import cairo
import numpy as np
import cv2
import os

from PIL import Image


def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def set_background(color1: tuple, color2: tuple, context):
    pat = cairo.LinearGradient(0.0, 0.0, 1.0, 1.0)
    pat.add_color_stop_rgba(0, *color1, 1)  # First stop, 50% opacity
    pat.add_color_stop_rgba(1, *color2, 1)  # Last stop, 100% opacity

    context.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    context.set_source(pat)
    context.fill()


def get_spiral(alpha: float, normalize):
    arc = 4
    phi = 0
    points = []
    steps = []
    x, y = 0, 0
    while (abs(x) < 0.45) & (abs(y) < 0.45):
        radius = phi * alpha
        x = np.cos(phi) * radius / normalize
        y = np.sin(phi) * radius / normalize
        points.append((x, y))
        if radius != 0:
            step = np.arcsin(arc / (2 * radius))
        else:
            step = arc / (2 * alpha)

        phi += step
        steps.append(step)
    return points, steps


def spiral_width(alpha: float, normalize, steps, widths):
    phi = 0
    line_top = []
    line_bottom = []
    scaled = scale_array(widths, 0.001, 1 * np.pi * alpha)

    for step, weight in zip(steps, scaled):
        for side in ['top', 'bottom']:
            if side == "top":
                radius = phi * alpha + weight
                x = np.cos(phi) * radius / normalize
                y = np.sin(phi) * radius / normalize
                line_top.append((x, y))
            if side == "bottom":
                radius = phi * alpha - weight
                x = np.cos(phi) * radius / normalize
                y = np.sin(phi) * radius / normalize
                line_bottom.append((x, y))

        phi += step

    return line_top[1:] + line_bottom[1:][::-1]


def scale_array(array: np.array, min_value: float, max_value: float) -> np.array:
    min_array = np.min(array)
    max_array = np.max(array)
    delta_array = max_array - min_array
    normalized = (array - min_array) / delta_array

    delta_scaled = max_value - min_value
    return normalized * delta_scaled + min_value


def image_preprocessing(image_file: str, auto_contrast: bool = False, inverse: bool = False) -> np.array:
    image = np.array(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    height, width = image.shape[:2]
    offset = min(height, width) // 2
    image = image[height // 2 - offset: height // 2 + offset:,
                    width // 2 - offset: width // 2 + offset]

    if auto_contrast:
        image = cv2.convertScaleAbs(image, alpha=1.1, beta=10)
    if inverse:
        image = cv2.bitwise_not(image)

    return image


def get_weights(image: np.array, spiral_points: list, alpha: float) -> np.array:
    scale = min(image.shape[:2])
    offset = scale // 2

    weights = []

    for point in spiral_points:
        point = [int(coord * scale + offset) for coord in point]
        x, y = point
        max_width = int(alpha + 1)
        mean_color = np.mean(image[y - max_width:y + max_width, x - max_width:x + max_width])
        weights.append(mean_color)

    return weights


def draw_spiral(context: cairo.Context, spiral: list, color: tuple) -> None:
    # Drawing spiral
    context.translate(0.5, 0.5)
    context.set_line_width(0.0005)
    context.move_to(0, 0)
    for line in spiral:
        context.line_to(*line)

    context.close_path()

    # Shape and color
    context.set_source_rgb(*color)  # Spiral color
    context.fill()
    context.set_line_join(cairo.LINE_JOIN_ROUND)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.stroke()


def transform_image(
        file: Image,
        mode: str = 'PNG',
        alpha: float = 2.5,
        background_color1: str = "#64130A", 
        background_color2: str = "#051646",
        spiral_color: str = "#65BFFC",
        inverse_flag: bool = False,
        contrast_flag: bool = False
    ) -> None:
    # Work with arguments
    bg_color1 = hex_to_rgb(background_color1)
    bg_color2 = hex_to_rgb(background_color2)
    spiral_color = hex_to_rgb(spiral_color)

    # Preparing image
    source = image_preprocessing(file, inverse=inverse_flag, auto_contrast=contrast_flag)

    # Chose output format
    if mode == 'PNG':
        SIZE = 2000
        ALPHA = alpha
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, SIZE, SIZE)

    # Preparing canvas
    canvas = cairo.Context(surface)
    canvas.scale(SIZE, SIZE)  # Normalizing the canvas
    set_background(bg_color1, bg_color2, canvas)

    # Construct the spiral
    points, steps = get_spiral(ALPHA, SIZE)
    weights = get_weights(source, points, ALPHA)
    lines = spiral_width(ALPHA, SIZE, steps, weights)

    # Drawing spiral
    draw_spiral(canvas, lines, spiral_color)

    # Export result

    img = Image.frombuffer(
        "RGBA",
        (surface.get_width(), surface.get_height()),
        surface.get_data(),
        "raw",
        "BGRA",
        0,
        1,
    )

    return img
