import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Coordinate:
    x: float
    y: float

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def rotate(self, angle):
        init_magnitude = self.magnitude()
        init_angle = self.angle()
        self.x = init_magnitude * math.cos(init_angle + angle)
        self.y = init_magnitude * math.sin(init_angle + angle)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle(self):
        angle = math.atan2(self.y, self.x)
        if angle < 0:
            angle += 2 * np.pi
        return angle


def get_circle(a, b, c):
    """Gets the center and radius of a circle that connects three coordinates

    Args:
        a (Coordinate): Coordinate to generate a circle from
        b (Coordinate): Coordinate to generate a circle from
        c (Coordinate): Coordinate to generate a circle from

    Returns:
        (Coordinate, float): Center of circle and circle radius
    """
    # Equation of circle is x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    x_ab = a.x - b.x
    x_ac = a.x - c.x
    y_ab = a.y - b.y
    y_ac = a.y - c.y

    sx_ac = a.x**2 - c.x**2
    sy_ac = a.y**2 - c.y**2
    sx_ba = b.x**2 - a.x**2
    sy_ba = b.y**2 - a.y**2

    f = (sx_ac * x_ab + sy_ac * x_ab + sx_ba * x_ac + sy_ba * x_ac) / (
        2 * (-y_ac * x_ab + y_ab * x_ac)
    )

    g = (sx_ac * y_ab + sy_ac * y_ab + sx_ba * y_ac + sy_ba * y_ac) / (
        2 * (-x_ac * y_ab + x_ab * y_ac)
    )

    c = -pow(a.x, 2) - pow(a.y, 2) - 2 * g * a.x - 2 * f * a.y

    r = math.sqrt(g**2 + f**2 - c)

    return (Coordinate(-g, -f), r)
