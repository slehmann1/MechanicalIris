import math
import time

import matplotlib.animation as animation
import matplotlib.patches as patch
import matplotlib.pyplot as plt
import numpy as np

from blade import Blade


class Iris:
    PLOT_RANGE = [-200, 200, -200, 200]
    SLEEP_TIME = 0.001
    _COLOUR = "red"

    def __init__(self, blade_count, AC, BC, pinned_radius):
        self.blade_count = blade_count
        self.AC = AC
        self.BC = BC
        self.pinned_radius = pinned_radius

        self.blades = [
            Blade(2 * np.pi / blade_count * i, self.pinned_radius, self.AC, self.BC)
            for i in range(blade_count)
        ]

        plt.figure()
        self.fig, self.axs = plt.subplots()
        self.fig.set_size_inches(10, 10)

    def drawIris(self, start_theta_a, end_theta_a):
        blade_states = [
            blade.calc_blade_states(
                start_theta_a,
                end_theta_a,
            )
            for blade in self.blades
        ]
        plt.show(block=False)
        i = 0

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

            i += 1

            if i == len(blade_states[0]) - 1:
                i = 0


iris = Iris(16, 100, 60, 45)
iris.drawIris(270 * np.pi / 180, 290 * np.pi / 180)
