import math

import matplotlib.patches as patch
import matplotlib.pyplot as plt
import numpy as np


class Ring:
    DEFAULT_RING_THICKNESS = 10
    DEFAULT_SLOT_WIDTH = 5
    SLOT_COLOUR = "red"
    BORDER_COLOUR = "black"

    def __init__(
        self,
        blade_count,
        start_theta_2,
        end_theta_2,
        pin_radial_loc,
        slot_width=DEFAULT_SLOT_WIDTH,
        radial_thickness=DEFAULT_RING_THICKNESS,
    ):
        self.blade_count = blade_count
        self.start_theta_2 = start_theta_2
        self.end_theta_2 = end_theta_2
        self.radial_thickness = radial_thickness
        self.id = (pin_radial_loc - radial_thickness / 2) * 2
        self.od = (pin_radial_loc + radial_thickness / 2) * 2
        self.slot_width = slot_width

    def draw(self, axs):
        inner_wall = plt.Circle(
            (0, 0), self.id / 2, color=self.BORDER_COLOUR, fill=False
        )
        axs.add_patch(inner_wall)
        outer_wall = plt.Circle(
            (0, 0), self.od / 2, color=self.BORDER_COLOUR, fill=False
        )
        axs.add_patch(outer_wall)
        slot_id = (self.id + self.od) / 2 - self.slot_width
        slot_od = slot_id + self.slot_width * 2

        for i in range(self.blade_count):
            self.draw_slot(
                axs,
                i * 2 * np.pi / self.blade_count + self.start_theta_2,
                i * 2 * np.pi / self.blade_count + self.end_theta_2,
                slot_id,
                slot_od,
            )

    def draw_slot(self, axs, start_angle, end_angle, id, od):
        """Draws a curved slot

        Args:
            axs (Axes): Axes to draw on
            start_angle (float): Measured from +x in rad
            end_angle (float): Measured from +x in rad
            id (float): Internal diameter of the slot
            od (float): Outer diameter of the slot
        """
        slot_theta_1 = start_angle * 180 / np.pi
        slot_theta_2 = end_angle * 180 / np.pi
        inner_slot = patch.Arc(
            (0, 0),
            id,
            id,
            theta1=slot_theta_1,
            theta2=slot_theta_2,
            color=self.SLOT_COLOUR,
        )
        outer_slot = patch.Arc(
            (0, 0),
            od,
            od,
            theta1=slot_theta_1,
            theta2=slot_theta_2,
            color=self.SLOT_COLOUR,
        )
        start_wall = patch.Arc(
            (
                (id + od) / 4 * math.cos(start_angle),
                (id + od) / 4 * math.sin(start_angle),
            ),
            (od - id) / 2,
            (od - id) / 2,
            theta1=180 + start_angle * 180 / np.pi,
            theta2=start_angle * 180 / np.pi,
            color=self.SLOT_COLOUR,
        )
        end_wall = patch.Arc(
            (
                (id + od) / 4 * math.cos(end_angle),
                (id + od) / 4 * math.sin(end_angle),
            ),
            (od - id) / 2,
            (od - id) / 2,
            theta1=end_angle * 180 / np.pi,
            theta2=180 + end_angle * 180 / np.pi,
            color=self.SLOT_COLOUR,
        )
        axs.add_patch(inner_slot)
        axs.add_patch(outer_slot)
        axs.add_patch(start_wall)
        axs.add_patch(end_wall)
