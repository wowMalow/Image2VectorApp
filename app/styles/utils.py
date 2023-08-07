import numpy as np
from typing import Union, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rootspace(
        start: Union[float, int],
        end: Union[float, int],
        num: int,
        power: int
    ) -> np.array:
    x_max = end ** power
    x_min = start ** power
    a = np.linspace(x_min, x_max, num)
    return np.power(a, 1. / power)