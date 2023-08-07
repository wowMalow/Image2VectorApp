import cairo
import numpy as np
import cv2
import os

from PIL import Image

from typing import List


class Canvas:
    def __init__(self, width: int, height: int, normalize: bool=True):
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)

        if normalize:
            self.context.scale(self.width, self.height)  # Normalizing the canvas

    def show(self) -> Image:
        return self.to_pillow()

    def save_png(self, file_name: str):
        self.surface.write_to_png(f"{file_name}.png") 

    def to_pillow(self) -> Image:
        image = Image.frombuffer(
            "RGBA",
            (self.surface.get_width(), self.surface.get_height()),
            self.surface.get_data(),
            "raw",
            "BGRA",
            0,
            1,
        )
        return image

    def to_numpy(self) -> np.array:
        return np.array(self.to_pillow)

    def set_gradient_background(self, color1: tuple, color2: tuple):
        pat = cairo.LinearGradient(0.0, 0.0, 1.0, 1.0)
        pat.add_color_stop_rgba(0, *color1, 1)  # First stop, 50% opacity
        pat.add_color_stop_rgba(1, *color2, 1)  # Last stop, 100% opacity

        self.context.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
        self.context.set_source(pat)
        self.context.fill()

    def path(self, points: list, color: tuple, width: float=0.0005):
        # Drawing spiral
        self.context.translate(0.5, 0.5)
        # context.set_line_width(0.001)
        self.context.set_line_width(width)
        self.context.move_to(*points[0])
        for line in points:
            self.context.line_to(*line)

        # Shape and color
        self.context.set_source_rgb(*color)
        # context.fill()
        self.context.set_line_join(cairo.LINE_JOIN_ROUND)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
        self.context.stroke()

    def poligon(self, points: list, color: tuple) -> None:
        # Drawing spiral
        self.context.translate(0.5, 0.5)
        self.context.set_line_width(0.001)
        self.context.move_to(*points[0])
        for line in points:
            self.context.line_to(*line)

        # Shape and color
        self.context.set_source_rgb(*color)
        self.context.fill()
        self.context.set_line_join(cairo.LINE_JOIN_ROUND)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
        self.context.stroke()