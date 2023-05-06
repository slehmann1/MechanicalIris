import math

import numpy as np

import geometry
from geometry import Arc, Circle, Coordinate, Line, Rectangle
from part import Part


class ActuatorRing(Part):
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
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.pin_radius = pin_radius
        self.hole_radius = hole_radius
        self.pin_count = pin_count
        self.tab_width = tab_width
        self.tab_height = tab_height
        super().__init__(self._COLOUR, self._DXF_FILE_NAME)

    def build_shapes(self, **kwargs):
        rotation_angle = kwargs["rotation_angle"]
        tab_angle = geometry.get_chord_subtended_angle(
            self.tab_width, self.outer_radius
        )
        handle_coords = self.get_handle_coords(tab_angle, rotation_angle)
        shapes = [
            # ID
            Circle(Coordinate(0, 0), self.inner_radius, self._COLOUR),
            # OD
            Arc(
                Coordinate(0, 0),
                self.outer_radius * 2,
                self.outer_radius * 2,
                rotation_angle * 180 / np.pi - tab_angle / 2 * 180 / np.pi,
                360 + rotation_angle * 180 / np.pi + tab_angle / 2 * 180 / np.pi,
                self._COLOUR,
            ),
            Line(handle_coords[1], handle_coords[3], self._COLOUR),
            Line(handle_coords[2], handle_coords[4], self._COLOUR),
            Arc(
                handle_coords[5],
                handle_coords[3].distance_to(handle_coords[4]),
                handle_coords[5].distance_to(handle_coords[6]) * 2,
                180,
                rotation_angle * 180 / np.pi + 90,
                self._COLOUR,
            ),
        ]
        # Add slots for each pin
        shapes.extend(
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
        self.shapes = shapes
        return shapes

    def get_handle_coords(self, tab_angle, rotation_angle):
        c_1 = Coordinate(
            self.outer_radius * math.cos(rotation_angle - tab_angle / 2),
            self.outer_radius * math.sin(rotation_angle - tab_angle / 2),
        )
        c_2 = Coordinate(
            self.outer_radius * math.cos(rotation_angle + tab_angle / 2),
            self.outer_radius * math.sin(rotation_angle + tab_angle / 2),
        )
        c_3 = Coordinate(
            (self.outer_radius + self.tab_height)
            * math.cos(rotation_angle - tab_angle / 2),
            (self.outer_radius + self.tab_height)
            * math.sin(rotation_angle - tab_angle / 2),
        )
        c_4 = Coordinate(
            (self.outer_radius + self.tab_height)
            * math.cos(rotation_angle + tab_angle / 2),
            (self.outer_radius + self.tab_height)
            * math.sin(rotation_angle + tab_angle / 2),
        )
        c_5 = c_4.linterp(c_3, 0.5)
        c_6 = c_3.midpoint_normal(c_4, c_3.distance_to(c_4) / 2)

        return {1: c_1, 2: c_2, 3: c_3, 4: c_4, 5: c_5, 6: c_6}

    def draw(self, axs, rotation_angle=0):
        self.build_shapes(rotation_angle=rotation_angle)

        for shape in self.shapes:
            shape.draw(axs)
