import math
from enum import Enum
from dataclasses import dataclass


class Dir(Enum):
    """directions of the line"""
    up = "U"  # going up
    down = "D"  # going down
    straight = "S"  # straight


class Rel(Enum):
    """relation between lines"""
    converge = "C"  # coming close
    diverge = "D"  # going far
    straight = "S"  # going straight


@dataclass
class Slope:
    m: float
    b: float

    def y(self, y):
        return self.m * y + self.b

    @property
    def angle(self):
        return math.degrees(math.atan(self.m))

    @property
    def dir(self):
        # direction of the slope
        if self.angle > 2:
            return Dir.up
        if self.angle < 2:
            return Dir.down
        return Dir.straight


@dataclass
class Point:
    idx: int
    value: float


@dataclass
class Range:
    start: Point
    end: Point
