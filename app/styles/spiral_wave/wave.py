import numpy as np

from app.styles.spiral_base import SpiralBase
from app.styles.utils import rootspace


class WavePath(SpiralBase):
    def __init__(self, step: float=0.0063) -> None:
        super().__init__(step=step)

    def transform_image(self, image: np.array) -> np.array:
        spiral_points = self._get_spiral_points()
        envelope = self._get_envelope(image, spiral_points)
        stylized_image_points = self._get_spiral_wave_points(envelope)
        return stylized_image_points

    def _get_spiral_wave_points(self, envelope: np.array) -> np.array:
        b = self._step / np.pi
        a = b
        r_max = 0.45
        phi_max = (r_max - a) / b
        phi = rootspace(0, phi_max, self._num_points, power=1.9)
        

        amp = 0.99 * envelope * self._step
        wo_start = 3
        wo_end = wo_start * (phi_max // np.pi - 1)
        w = rootspace(wo_start, wo_end, self._num_points, power=1.9)
        r = (a + b * phi) + amp * np.sin(w * phi)

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        points = np.hstack([x.reshape(-1, 1), y.reshape(-1, 1)])
        return points