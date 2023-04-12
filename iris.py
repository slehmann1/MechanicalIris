import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from blade import Blade


class Iris:
    PLOT_RANGE = [-100, 100, -100, 100]

    def __init__(
        self, blade_count, a, b, c, d, e, f, g, blade_rotation, theta_5
    ) -> None:
        self.blade_count = blade_count
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.blade_rotation = blade_rotation
        self.theta_5 = theta_5

        self.blades = []
        for i in range(blade_count):
            theta_1 = 2 * np.pi / blade_count * i
            self.blades.append(
                Blade(
                    a,
                    b,
                    c,
                    d,
                    e,
                    f,
                    g,
                    0,
                    0,
                    self.blade_rotation * i,
                    theta_1,
                    theta_5,
                )
            )

    def animateIris(self, start_theta_2, end_theta_2):
        # Adding theta_1 is required to ensure blades are in sync with eachother
        x_y_paths = [
            blade.get_x_y_motion_coordinates(
                blade.calc_blade_states(
                    start_theta_2 + blade.theta_1,
                    end_theta_2 + blade.theta_1,
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
        ani = animation.FuncAnimation(
            fig,
            self.update_lines,
            len(x_y_paths[0][0]),
            fargs=[x_y_paths, lines],
            interval=1,
            blit=False,
        )

        plt.show()

    def update_lines(self, num, x_y_paths, lines):
        for i, line in enumerate(lines):
            line.set_data(x_y_paths[i][0][num], x_y_paths[i][1][num])
            line.axes.axis(self.PLOT_RANGE)
        return (line,)


iris = Iris(3, 66.5, 42, 39.5, 36.5, 41.5, 35, 72, 120 * np.pi / 180, 60 * np.pi / 180)
iris.animateIris(140 * np.pi / 180, 220 * np.pi / 180)
