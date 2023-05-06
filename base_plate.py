import math

import numpy as np

from geometry import Circle, Coordinate
from tabbed_ring import TabbedRing


class BasePlate(TabbedRing):
    _COLOUR = "green"
    _DXF_FILE_NAME = "basePlate.dxf"

    def __init__(
        self,
        inner_radius,
        outer_radius,
        pin_radius,
        hole_radius,
        pin_count,
        tab_width,
        tab_height,
    ):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.pin_radius = pin_radius
        self.hole_radius = hole_radius
        self.pin_count = pin_count
        super().__init__(
            self._COLOUR,
            self._DXF_FILE_NAME,
            tab_width,
            tab_height,
            inner_radius,
            outer_radius,
        )

    def build_shapes(self, **kwargs):
        self.shapes = super().build_shapes(**kwargs)
        rotation_angle = kwargs["rotation_angle"]

        # Add holes for each pin
        self.shapes.extend(
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
        return self.shapes
