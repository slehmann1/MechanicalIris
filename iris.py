import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from blade import Blade
from ring import Ring


class Iris:
    PLOT_RANGE = [-100, 100, -100, 100]

    def __init__(
        self, blade_count, a, b, c, d, e, f, g, theta_5, start_theta_2, end_theta_2
    ):
        self.blade_count = blade_count
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.theta_5 = theta_5
        self.start_theta_2 = start_theta_2
        self.end_theta_2 = end_theta_2
        self.ring = Ring(blade_count, end_theta_2 - start_theta_2, theta_5, a)
        self.blades = [
            Blade(
                a,
                b,
                c,
                d,
                e,
                f,
                g,
                2 * np.pi / blade_count * i,
                theta_5,
                0,
                0,
            )
            for i in range(blade_count)
        ]

    def animateIris(self, start_theta_2=None, end_theta_2=None):
        """Plots the motion of the iris through a range of theta_2 values

        Args:
            start_theta_2 (float): Beginning theta_2 value for all blades
            end_theta_2 (float): Ending theta_2 value for all blades
        """

        if start_theta_2 is None or end_theta_2 is None:
            start_theta_2 = self.start_theta_2
            end_theta_2 = self.end_theta_2

        x_y_paths = [
            blade.get_x_y_motion_coordinates(
                blade.calc_blade_states(
                    start_theta_2,
                    end_theta_2,
                )
            )
            for blade in self.blades
        ]

        plt.figure()
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        lines = [ax.plot(x[0], y[0], color="k")[0] for (x, y) in x_y_paths]
        circle = plt.Circle((0, 0), self.a, color="blue", fill=False)
        ax.add_patch(circle)
        _ = animation.FuncAnimation(
            fig,
            self.update_lines,
            len(x_y_paths[0][0]),
            fargs=[x_y_paths, lines],
            interval=1,
            blit=False,
        )
        self.ring.draw(ax)
        plt.show()

    def update_lines(self, num, x_y_paths, lines):
        for i, line in enumerate(lines):
            line.set_data(x_y_paths[i][0][num], x_y_paths[i][1][num])
            line.axes.axis(self.PLOT_RANGE)
        return (line,)


iris = Iris(
    3,
    66.5,
    42,
    39.5,
    36.5,
    41.5,
    35,
    72,
    60 * np.pi / 180,
    200 * np.pi / 180,
    230 * np.pi / 180,
)
iris.animateIris()
