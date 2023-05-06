import math
from abc import abstractmethod
from dataclasses import dataclass

import matplotlib.patches as patch
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
        return self

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

    def midpoint_normal(self, other, normal_dist, positive=True):
        """Gets the coordinate of a point a normal distance from the midpoint between another coordinate

        Args:
            other (Coordinate): The other coordinate to determine a normal distance and angle from
            normal_dist (float): Distance from the midpoint line
            positive (bool, optional): Controls which side of the midpoint line the coordinate lies. Defaults to True.

        Returns:
            Coordinate: A point a normal distance away from a midpoint between the two driver coordinates
        """
        midpoint = self.linterp(other, 0.5)
        angle = (self - other).angle()
        normal_angle = angle + np.pi / 2 if positive else angle + 3 * np.pi / 2
        return Coordinate(
            midpoint.x + math.cos(normal_angle) * normal_dist,
            midpoint.y + math.sin(normal_angle) * normal_dist,
        )


class Shape:
    def __init__(self, colour, contruction_line=False):
        self.colour = colour
        self.construction_line = contruction_line

    @abstractmethod
    def add_to_dxf(self, doc):
        pass

    @abstractmethod
    def draw(self, axs):
        pass


class Line(Shape):
    def __init__(self, start_coord, end_coord, colour, contruction_line=False):
        self.start_coord = start_coord
        self.end_coord = end_coord
        super().__init__(colour, contruction_line)

    def draw(self, axs):
        axs.plot(
            [self.start_coord.x, self.end_coord.x],
            [self.start_coord.y, self.end_coord.y],
            color=self.colour,
            linestyle="dashed" if self.construction_line else "solid",
        )

    def add_to_dxf(self, doc):
        doc.modelspace.add_line(
            [self.start_coord.x, self.start_coord.y],
            [self.end_coord.x, self.end_coord.y],
        )


class Rectangle(Shape):
    def __init__(
        self, centre_coord, width, height, theta, colour, contruction_line=False
    ):
        coords = self._gen_coords(centre_coord, width, height, theta)
        self.lines = [
            Line(coords[0], coords[1], colour),
            Line(coords[1], coords[2], colour),
            Line(coords[2], coords[3], colour),
            Line(coords[3], coords[0], colour),
        ]
        super().__init__(colour, contruction_line)

    def _gen_coords(self, centre_coord, width, height, theta):
        c_1 = Coordinate(-width / 2, -height / 2).rotate(theta) + centre_coord
        c_2 = Coordinate(-width / 2, height / 2).rotate(theta) + centre_coord
        c_3 = Coordinate(width / 2, height / 2).rotate(theta) + centre_coord
        c_4 = Coordinate(width / 2, -height / 2).rotate(theta) + centre_coord

        return [c_1, c_2, c_3, c_4]

    def draw(self, axs):
        for line in self.lines:
            line.draw(axs)

    def add_to_dxf(self, doc):
        for line in self.lines:
            line.add_to_dxf(doc)


class Arc(Shape):
    def __init__(
        self, center, width, height, theta_1, theta_2, colour, construction_line=False
    ):
        """Creates an elliptical arc

        Args:
            center (Coordinate): Centerpoint
            width (float): Width of the ellipse
            height (float): Height of the ellipse
            theta_1 (float): Start angle measured in degrees from +x
            theta_2 (flaot): End angle measured in degrees from +x
            colour (str): Matplotlib colour
            construction_line (bool, optional): Whether the arc is a construction line that should be hidden in the DXF. Defaults to False.
        """
        self.center = center
        self.width = width
        self.height = height
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        super().__init__(colour, construction_line)

    def draw(self, axs):
        axs.add_patch(
            patch.Arc(
                (self.center.x, self.center.y),
                self.width,
                self.height,
                theta1=self.theta_1,
                theta2=self.theta_2,
                color=self.colour,
                linestyle="dashed" if self.construction_line else "solid",
            )
        )

    def add_to_dxf(self, doc):
        ratio = self.height / self.width
        doc.modelspace.add_ellipse(
            (self.center.x, self.center.y),
            (self.height / 2, 0),
            ratio,
            self.theta_1 * np.pi / 180,
            self.theta_2 * np.pi / 180,
        )


class Circle(Shape):
    def __init__(self, center, radius, colour, filled=False, construction_line=False):
        """Creates an elliptical arc

        Args:
            center (Coordinate): Centerpoint
            width (float): Width of the ellipse
            height (float): Height of the ellipse
            theta_1 (float): Start angle measured in degrees from +x
            theta_2 (flaot): End angle measured in degrees from +x
            colour (str): Matplotlib colour
            construction_line (bool, optional): Whether the arc is a construction line that should be hidden in the DXF. Defaults to False.
        """
        self.center = center
        self.radius = radius
        self.filled = filled
        super().__init__(colour, construction_line)

    def draw(self, axs):
        axs.add_patch(
            patch.Circle(
                (self.center.x, self.center.y),
                self.radius,
                color=self.colour,
                fill=self.filled,
            )
        )

    def add_to_dxf(self, doc):
        doc.modelspace.add_circle((self.center.x, self.center.y), self.radius)


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

    if radius > chord_length / 2:
        # Chord length distance formula
        d = math.sqrt(radius**2 - (chord_length / 2) ** 2)
    else:
        # Chord length distance formula
        d = math.sqrt((chord_length / 2) ** 2 - radius**2)

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


def get_chord_subtended_angle(chord_length, r):
    """Gets the angle in radians subtended by a chord on a circle

    Args:
        chord_length (float): Length of the chord
        r (float): Radius of the circle

    Returns:
        float: Subtended angle in radians
    """
    return 2 * math.asin(chord_length / 2 / r)
