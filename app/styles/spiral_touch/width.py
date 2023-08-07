import numpy as np

from app.styles.spiral_base import SpiralBase
from app.styles.utils import rootspace


class WidthPath(SpiralBase):
    def __init__(self, step: float=0.0063) -> None:
        super().__init__(step=step)

    def transform_image(self, image: np.array) -> np.array:
        spiral_points = self._get_spiral_points()
        envelope = self._get_envelope(image, spiral_points)
        stylized_image_points = self._get_spiral_width_points(envelope)
        return stylized_image_points

    def _get_spiral_width_points(self, envelope: np.array) -> np.array:
        b = self._step / np.pi
        a = b
        r_max = 0.45
        phi_max = (r_max - a) / b
        phi = rootspace(0, phi_max, self._num_points, power=1.9)
        

        amp = 0.95 * envelope * self._step
        r = (a + b * phi) + amp

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        points_high = np.hstack([x.reshape(-1, 1), y.reshape(-1, 1)])

        r = (a + b * phi) - amp

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        points_low = np.hstack([x.reshape(-1, 1), y.reshape(-1, 1)])
        return np.vstack([points_high, points_low[::-1]])