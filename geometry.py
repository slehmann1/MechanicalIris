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

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def rotate(self, angle):
        init_magnitude = self.magnitude()
        init_angle = self.angle()
        self.x = init_magnitude * math.cos(init_angle + angle)
        self.y = init_magnitude * math.sin(init_angle + angle)

    def rotated_copy(self, angle):
        init_magnitude = self.magnitude()
        init_angle = self.angle()
        x = init_magnitude * math.cos(init_angle + angle)
        y = init_magnitude * math.sin(init_angle + angle)
        return Coordinate(x, y)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle(self):
        angle = math.atan2(self.y, self.x)
        if angle < 0:
            angle += 2 * np.pi
        return angle

    def linterp(self, other, progress):
        """Linearly interpolates between two coordinates

        Args:
            other (Coordinate): Coordinate to make progress towardds
            progress (float): Value between 0 and 1

        Returns:
            Coordinate: Interpolated coordinate
        """
        return Coordinate(
            self.x + (other.x - self.x) * progress,
            self.y + (other.y - self.y) * progress,
        )


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


def get_circle_center(a, b, radius, convex_right=True):
    """Gets the center of a circle tangent to two points with a given radius

    Args:
        a (Coordinate): Coincident on the circle
        b (Coordinate): Coincident on the circle
        radius (float): Circle radius
        convex_right (bool, optional): Whether the circle through the two points has its convex surface pointing rightwards. Defaults to True.

    Returns:
        _type_: _description_
    """
    chord_length = a.distance_to(b)

    # Chord length distance formula
    d = math.sqrt(radius**2 - (chord_length / 2) ** 2)

    multiplier = 1 if convex_right else -1
    mid_chord = a.linterp(b, 0.5)
    chord_angle = (b - a).angle()
    return Coordinate(
        mid_chord.x + d * multiplier * math.cos(chord_angle + np.pi / 2),
        mid_chord.y + d * multiplier * math.sin(chord_angle + np.pi / 2),
    )


def get_chord_coord(a, center, theta, radius):
    """Gets the coordinate of a point tangent on a circle and part of a chord

    Args:
        a (Coordinate): Coordinate of a point coincident on a circle, forming part of a chord
        center (Coordinate): The center of the circle
        theta (float): Angle subtended by a chord
        radius (float): Radius of the circle

    Returns:
        Coordinate: Coordinates of the other point of the chord
    """
    alpha = (a - center).angle()
    x = (
        a.x
        - (radius - radius * math.cos(theta)) * math.cos(alpha)
        - radius * math.sin(theta) * math.sin(alpha)
    )
    y = (
        a.y
        - (radius - radius * math.cos(theta)) * math.sin(alpha)
        + radius * math.sin(theta) * math.cos(alpha)
    )
    return Coordinate(x, y)
