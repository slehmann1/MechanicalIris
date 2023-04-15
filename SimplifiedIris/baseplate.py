import math

import matplotlib.pyplot as plt
import numpy as np


class BasePlate:
    _COLOUR = "green"
    _DEFAULT_PIN_DIAMETER = 5

    def __init__(
        self,
        blade_count,
        start_theta_2,
        end_theta_2,
        pin_radial_loc,
        id,
        od,
        pin_diameter=None,
    ):
        if pin_diameter is None:
            pin_diameter = self._DEFAULT_PIN_DIAMETER

        self.blade_count = blade_count
        self.start_theta_2 = start_theta_2
        self.end_theta_2 = end_theta_2
        self.pin_radial_loc = pin_radial_loc
        self.pin_diameter = pin_diameter
        self.id = id
        self.od = od

    def draw(self, axs, rotation_angle=0):
        """Draws the baseplate to a set of axes

        Args:
            axs (Axes): Axes to draw on
            rotation_angle (float, optional): Rotation angle from +x in rad. Defaults to 0.
        """
        inner_wall = plt.Circle((0, 0), self.id / 2, color=self._COLOUR, fill=False)
        outer_wall = plt.Circle((0, 0), self.od / 2, color=self._COLOUR, fill=False)
        axs.add_patch(inner_wall)
        axs.add_patch(outer_wall)

        for i in range(self.blade_count):
            angle = i * 2 * np.pi / self.blade_count + rotation_angle
            peg = plt.Circle(
                (
                    self.pin_radial_loc * math.cos(angle),
                    self.pin_radial_loc * math.sin(angle),
                ),
                self.pin_diameter / 2,
                color=self._COLOUR,
                fill=False,
            )
            axs.add_patch(peg)
