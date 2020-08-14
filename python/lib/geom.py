import sys

MAX = sys.float_info.max
MIN = sys.float_info.min


def center(point_a, point_b):
    return [
        0.5 * (point_a[0] + point_b[0]),
        0.5 * (point_a[1] + point_b[1]),
        0.5 * (point_a[2] + point_b[2])
    ]


class Bounds:
    def __init__(self):
        self.min = [MAX, MAX, MAX]
        self.max = [MIN, MIN, MIN]

    def add(self, point):
        self.min = [
            min(self.min[0], point[0]),
            min(self.min[1], point[1]),
            min(self.min[2], point[2])
        ]
        self.max = [
            max(self.max[0], point[0]),
            max(self.max[1], point[1]),
            max(self.max[2], point[2])
        ]

    def center(self):
        return center(self.min, self.max)


class ConstBounds:
    def __init__(self, min, max):
        self._min = min
        self._max = max

    @property
    def min(self):
        return this._min[:]

    @property
    def max(self):
        return this._max[:]

    def diameter(self):
        "Max of X and Y diameters"
        return max(
            abs(self._max[0] - self._min[0]),
            abs(self._max[1] - self._min[1])
        )

    def center(self):
        return center(self._min, self._max)
