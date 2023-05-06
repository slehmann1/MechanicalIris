import time

import matplotlib.patches as patch
import matplotlib.pyplot as plt
import numpy as np

from actuator_ring import ActuatorRing
from base_plate import BasePlate
from blade import Blade


class Iris:
    _SLEEP_TIME = 0.0001
    _COLOUR = "red"
    _ENDLESS_DRAW = False

    def __init__(
        self,
        blade_count,
        blade_angle,
        inner_radius,
        outer_radius,
        blade_width,
        peg_radius,
    ):
        self.blade_count = blade_count
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.blade_width = blade_width
        self.peg_radius = peg_radius

        self.pinned_radius = outer_radius + blade_width / 2
        self.BC = self.pinned_radius + blade_width
        blade_radius = self.pinned_radius * 1.2

        if blade_width > blade_radius:
            raise ValueError("Blade width too large")
        self.blades = [
            Blade(
                2 * np.pi / blade_count * i,
                blade_angle,
                self.pinned_radius,
                blade_radius,
                self.BC,
                self.blade_width,
            )
            for i in range(blade_count)
        ]

        self.fig = plt.figure()
        self.axs = self.fig.gca()
        self.fig.set_size_inches(10, 10)
        self.blades[0].set_theta_a_domain(
            inner_radius + blade_width / 2, outer_radius + blade_width / 2
        )
        tab_width = self.blade_width / 2
        tab_height = self.blade_width / 2

        self.domain = self.blades[0].theta_a_range
        self.base_plate = BasePlate(
            (self.pinned_radius - blade_width),
            (self.pinned_radius + blade_width),
            self.pinned_radius,
            self.peg_radius,
            self.blade_count,
            tab_width,
            tab_height,
        )
        self.actuator_ring = ActuatorRing(
            self.pinned_radius - blade_width,
            self.pinned_radius + blade_width,
            self.pinned_radius,
            self.peg_radius,
            self.blade_count,
            tab_width,
            tab_height,
        )

    def drawIris(self, start_theta_a=None, end_theta_a=None):
        if start_theta_a is None or end_theta_a is None:
            start_theta_a = self.domain[0]
            end_theta_a = self.domain[1]

        # Only calculate blade state for one blade, others are rotated duplicates
        initial_blade_state = self.blades[0].calc_blade_states(
            start_theta_a, end_theta_a
        )

        blade_states = [
            [
                initial_blade_state[ii].rotated_copy(2 * np.pi / self.blade_count * i)
                for ii in range(len(initial_blade_state))
            ]
            for i in range(self.blade_count)
        ]

        plt.show(block=False)
        i = 0
        multiplier = 1

        while i < len(blade_states[0]):
            rotation_angle = blade_states[0][i].C.angle()

            plt.cla()
            for blade_index in range(len(self.blades)):
                self.blades[blade_index].build_shapes(
                    blade_state=blade_states[blade_index][i]
                )
                self.blades[blade_index].draw(self.axs, blade_states[blade_index][i])

            self.base_plate.draw(self.axs, rotation_angle)
            self.actuator_ring.draw(self.axs, 0)

            self.axs.add_patch(
                patch.Circle((0, 0), self.outer_radius, color=self._COLOUR, fill=False)
            )

            self.axs.add_patch(
                patch.Circle((0, 0), self.inner_radius, color=self._COLOUR, fill=False)
            )

            self.axs.add_patch(
                patch.Circle((0, 0), 0.01, color=self._COLOUR, fill=True)
            )

            self.axs.axis(
                [
                    -self.outer_radius * 2.5,
                    self.outer_radius * 2.5,
                    -self.outer_radius * 2.5,
                    self.outer_radius * 2.5,
                ]
            )
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(self._SLEEP_TIME)

            i += 1 * multiplier

            if self._ENDLESS_DRAW and i in [len(blade_states[0]) - 1, 0]:
                multiplier *= -1
        plt.close()

        self.blades[0].save_dxf()
        self.base_plate.save_dxf()
        self.actuator_ring.save_dxf()


iris = Iris(4, np.pi, 30, 45, 20, 1)
iris.drawIris()
