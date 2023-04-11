import functools
import math
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve


class blade:
    def __init__(self, a, b, c, d, e, f, g, theta_1, theta_5):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.theta_1 = theta_1
        self.theta_5 = theta_5
        self.calc_points()

    def calc_points(self):
        theta_2s = np.arange(200, 280, 1)
        thetas = [self.calc_thetas(theta_2 * np.pi / 180) for theta_2 in theta_2s]
        o_4_points = [self.calc_point_o4() for _ in thetas]
        b_points = [self.calc_point_b(theta[1], o_4_points[0]) for theta in thetas]
        a_points = [
            self.calc_point_a(theta_2 * np.pi / 180, (0, 0)) for theta_2 in theta_2s
        ]

        g_points = [self.calc_point_g(o_4_points[0], theta[1]) for theta in thetas]

        plt.figure()

        x = [
            [
                0,
                o_4_points[i][0],
                0,
                a_points[i][0],
                b_points[i][0],
                o_4_points[i][0],
                g_points[i][0],
                b_points[i][0],
            ]
            for i in range(len(thetas))
        ]
        y = [
            [
                0,
                o_4_points[i][1],
                0,
                a_points[i][1],
                b_points[i][1],
                o_4_points[i][1],
                g_points[i][1],
                b_points[i][1],
            ]
            for i in range(len(thetas))
        ]

        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        (line,) = ax.plot(x[0], y[0], color="k")
        ani = animation.FuncAnimation(
            fig, self.update, len(x), fargs=[x, y, line], interval=1, blit=False
        )
        ani.save("test.gif")
        plt.show()

    def update(self, num, x, y, line):
        line.set_data(x[num], y[num])
        line.axes.axis([-100, 100, -100, 100])
        return (line,)

    def plot_b(self):
        theta_2s = np.arange(200, 280, 0.1)
        thetas = [self.calc_thetas(theta_2 * np.pi / 180) for theta_2 in theta_2s]
        b_xs = [self.b * math.cos(theta[1]) for theta in thetas]
        b_ys = [self.b * math.sin(theta[1]) for theta in thetas]
        # plt.plot(theta_2s, b_xs, label="x")
        # plt.plot(theta_2s, b_ys, label="y")

        plt.plot(b_xs, b_ys, label="x")
        plt.legend()
        plt.show()

    def calc_point_b(self, theta_4, o2):
        return (o2[0] + self.d * math.cos(theta_4), o2[1] + self.d * math.sin(theta_4))

    def calc_point_a(self, theta_4, o4):
        return (o4[0] + self.c * math.cos(theta_4), o4[1] + self.c * math.sin(theta_4))

    def calc_point_o4(self):
        return (self.d * math.cos(self.theta_1), self.d * math.sin(self.theta_1))

    def calc_point_g(self, o4, theta_4):
        return (
            o4[0] + self.g * math.cos(theta_4 + self.theta_5),
            o4[1] + self.g * math.sin(theta_4 + self.theta_5),
        )

    def calc_thetas(self, theta_2):
        return fsolve(functools.partial(self.equations, theta_2=theta_2), (0, 0))

    def equations(self, guess, theta_2):
        """Closed-loop equations for four bar mechanism of a blade

        Args:
            guess (theta_3, theta_4): Initial guesses for theta_3 and theta_4
            theta_2 (float): theta_2 value

        Returns:
            (Equation 1, Equation 2): Closed loop equations
        """
        theta_3, theta_4 = guess
        eq_1 = (
            self.a * math.cos(theta_2)
            + self.b * math.cos(theta_3)
            - self.c * math.cos(theta_4)
            - self.d * math.cos(self.theta_1)
        )
        eq_2 = (
            self.a * math.sin(theta_2)
            + self.b * math.sin(theta_3)
            - self.c * math.sin(theta_4)
            - self.d * math.sin(self.theta_1)
        )
        return eq_1, eq_2


blade(66.5, 42, 39.5, 36.5, 41.5, 35, 72, 200 * np.pi / 180, 60 * np.pi / 180)
