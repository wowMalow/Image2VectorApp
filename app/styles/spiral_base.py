import numpy as np
from abc import abstractmethod

from app.styles.utils import rootspace


class SpiralBase:
    def __init__(self, step: float=0.0063) -> None:
        self._step = step
        self._num_points = self._calc_num_poins(self._step)

    def _get_spiral_points(self) -> np.array:
        b = self._step / np.pi
        a = b
        r_max = 0.45
        phi_max = (r_max - a) / b
        phi = rootspace(0, phi_max, self._num_points, power=1.9)
        r = (a + b * phi)

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        points = np.hstack([x.reshape(-1, 1), y.reshape(-1, 1)])
        return points
    
    def _get_envelope(self, image: np.array, spiral_points: np.array) -> np.array:
        scale = min(image.shape[:2])
        offset = scale // 2
        px_points = np.intp(spiral_points * scale + offset)
        max_width = int(self._step * scale / 2.)

        weights = []

        for point in px_points:
            x, y = point
            mean_color = np.mean(image[y - max_width:y + max_width + 1, x - max_width:x + max_width + 1])
            weights.append(mean_color)

        return np.array(weights) / max(weights)
    
    @abstractmethod
    def transform_image(image: np.array) -> np.array:
        pass

    def _calc_num_poins(self, step: float) -> int:
        return int(1 / step * 2_000)
