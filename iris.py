import math
import time

import matplotlib.animation as animation
import matplotlib.patches as patch
import matplotlib.pyplot as plt
import numpy as np

from blade import Blade


class Iris:
    PLOT_RANGE = [-200, 200, -200, 200]
    SLEEP_TIME = 0.01
    _COLOUR = "red"

    def __init__(
        self,
        blade_count,
        blade_angle,
        AC,
        BC,
        inner_radius,
        pinned_radius,
        blade_radius,
        blade_width,
    ):
        self.blade_count = blade_count
        self.AC = AC
        self.BC = BC
        self.inner_radius = inner_radius
        self.pinned_radius = pinned_radius
        self.blade_width = blade_width

        self.blades = [
            Blade(
                2 * np.pi / blade_count * i,
                blade_angle,
                self.pinned_radius,
                blade_radius,
                self.BC,
            )
            for i in range(blade_count)
        ]

        self.fig = plt.figure()
        self.axs = self.fig.gca()
        self.fig.set_size_inches(10, 10)
        self.blades[0].set_theta_a_domain(inner_radius, pinned_radius)
        self.domain = self.blades[0].theta_a_range

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
            plt.cla()
            for blade_index in range(len(self.blades)):
                self.blades[blade_index].draw(self.axs, blade_states[blade_index][i])

            self.axs.add_patch(
                patch.Circle((0, 0), self.pinned_radius, color=self._COLOUR, fill=False)
            )

            self.axs.add_patch(
                patch.Circle((0, 0), self.inner_radius, color=self._COLOUR, fill=False)
            )

            self.axs.axis(self.PLOT_RANGE)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(self.SLEEP_TIME)

            i += 1 * multiplier

            if i in [len(blade_states[0]) - 1, 0]:
                multiplier *= -1


iris = Iris(6, np.pi, 100, 60, 30, 45, 50.5, 20)
iris.drawIris()
