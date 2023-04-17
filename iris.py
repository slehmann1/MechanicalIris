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

    def __init__(self, blade_count, AC, BC, pinned_radius, blade_radius, blade_width):
        self.blade_count = blade_count
        self.AC = AC
        self.BC = BC
        self.pinned_radius = pinned_radius
        self.blade_width = blade_width

        self.blades = [
            Blade(
                2 * np.pi / blade_count * i,
                self.pinned_radius,
                blade_radius,
                self.BC,
            )
            for i in range(blade_count)
        ]

        self.fig = plt.figure()
        self.axs = self.fig.gca()
        self.fig.set_size_inches(10, 10)
        self.domain = self.blades[0].theta_a_range
        print(f"DOMAIN: {self.domain}")

        print(f" BX: {self.blades[0].calc_Bx_range()}")

    def drawIris(self, start_theta_a=None, end_theta_a=None):
        if start_theta_a is None or end_theta_a is None:
            start_theta_a = self.domain[0]
            end_theta_a = self.domain[1]

        blade_states = [
            blade.calc_blade_states(
                start_theta_a,
                end_theta_a,
            )
            for blade in self.blades
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

            self.axs.axis(self.PLOT_RANGE)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(self.SLEEP_TIME)

            i += 1 * multiplier

            if i in [len(blade_states[0]) - 1, 0]:
                multiplier *= -1


iris = Iris(12, 100, 60, 45, 50.5, 20)
iris.drawIris()
