import math
from typing import Tuple


def two_point_distance(self, xy1: Tuple[int, int], xy2: Tuple[int, int]) -> float:
    """
    Return the distance between the current entity and the given (x, y) coordinate.
    """
    x1, y1 = xy1
    x2, y2 = xy2

    return math.sqrt((x2- x1) ** 2 + (y2 - y1) ** 2)
