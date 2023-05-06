import math

import numpy as np

from geometry import Coordinate, Rectangle
from tabbed_ring import TabbedRing


class ActuatorRing(TabbedRing):
    _COLOUR = "purple"
    _DXF_FILE_NAME = "actuatorRing.dxf"

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
        # Add slots for each pin
        self.shapes.extend(
            [
                Rectangle(
                    Coordinate(
                        math.cos(rotation_angle + theta) * self.pin_radius,
                        math.sin(rotation_angle + theta) * self.pin_radius,
                    ),
                    2 * self.hole_radius,
                    2 * self.hole_radius,
                    rotation_angle + theta,
                    self._COLOUR,
                )
                for theta in np.arange(0, 2 * np.pi, 2 * np.pi / self.pin_count)
            ]
        )
        return self.shapes
