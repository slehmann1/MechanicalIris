import math

import numpy as np

from dxf import DXF
from geometry import Circle, Coordinate
from part import Part


class BasePlate(Part):
    _COLOUR = "green"
    _DXF_FILE_NAME = "basePlate.dxf"

    def __init__(self, inner_radius, outer_radius, pin_radius, hole_radius, pin_count):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.pin_radius = pin_radius
        self.hole_radius = hole_radius
        self.pin_count = pin_count
        super().__init__(self._COLOUR, self._DXF_FILE_NAME)

    def build_shapes(self, **kwargs):
        rotation_angle = kwargs["rotation_angle"]
        shapes = [
            # ID
            Circle(Coordinate(0, 0), self.inner_radius, self._COLOUR),
            # OD
            Circle(Coordinate(0, 0), self.outer_radius, self._COLOUR),
        ]
        # Add holes for each pin
        shapes.extend(
            [
                Circle(
                    Coordinate(
                        math.cos(rotation_angle + theta) * self.pin_radius,
                        math.sin(rotation_angle + theta) * self.pin_radius,
                    ),
                    self.hole_radius,
                    self._COLOUR,
                )
                for theta in np.arange(0, 2 * np.pi, 2 * np.pi / self.pin_count)
            ]
        )
        self.shapes = shapes
        return shapes

    def draw(self, axs, rotation_angle=0):
        self.build_shapes(rotation_angle=rotation_angle)

        for shape in self.shapes:
            shape.draw(axs)
