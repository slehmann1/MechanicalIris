import math

import numpy as np

from iris_calculator.geometry import Coordinate, Rectangle
from iris_calculator.tabbed_ring import TabbedRing


class ActuatorRing(TabbedRing):
    _COLOUR = "purple"
    _DXF_FILE_NAME = "actuatorRing.dxf"

    def __init__(
        self,
        inner_radius,
        outer_radius,
        hole_radius,
        pin_count,
        slot_inner_radius,
        slot_outer_radius,
        tab_width,
        tab_height,
    ):
        self.hole_radius = hole_radius
        self.pin_count = pin_count
        self.slot_inner_radius = slot_inner_radius
        self.slot_outer_radius = slot_outer_radius
        super().__init__(
            self._COLOUR,
            self._DXF_FILE_NAME,
            tab_width,
            tab_height,
            inner_radius,
            outer_radius,
        )

    def get_slot_inner_radius(self):
        return self.slot_inner_radius - self.hole_radius

    def get_slot_outer_radius(self):
        return self.slot_outer_radius + self.hole_radius

    def build_shapes(self, **kwargs):
        self.shapes = super().build_shapes(**kwargs)
        rotation_angle = kwargs["rotation_angle"]
        # Add slots for each pin
        self.shapes.extend(
            [
                Rectangle(
                    Coordinate(
                        math.cos(rotation_angle + theta)
                        * (self.slot_inner_radius + self.slot_outer_radius)
                        / 2,
                        math.sin(rotation_angle + theta)
                        * (self.slot_inner_radius + self.slot_outer_radius)
                        / 2,
                    ),
                    2 * self.hole_radius,
                    self.slot_outer_radius
                    - self.slot_inner_radius
                    + 2 * self.hole_radius,
                    rotation_angle + theta + np.pi / 2,
                    self._COLOUR,
                )
                for theta in np.arange(0, 2 * np.pi, 2 * np.pi / self.pin_count)
            ]
        )
        return self.shapes
