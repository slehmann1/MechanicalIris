import functools
import math
from dataclasses import dataclass

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class BladeState:
    o_4: Coordinate
    a: Coordinate
    b: Coordinate
    g: Coordinate


class blade:
    NUM_POINTS = 100
    PLOT_RANGE = [-100, 100, -100, 100]

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
        blade_states = self.calc_blade_states(200 * np.pi / 180, 280 * np.pi / 180)
        self.plot_blade_motion(blade_states)

    def calc_blade_state(self, theta_2):
        """Calculates the geometric state of the blade for a givent theta_2 value

        Args:
            theta_2 (float): In radian

        Returns:
            BladeState: Representing the geometric state of the blade
        """
        theta_34 = self.calc_theta_3_4(theta_2)
        o_4 = self.calc_point_o_4()
        a = self.calc_point_a(theta_2, o_4)
        b = self.calc_point_b(theta_34[1], o_4)
        g = self.calc_point_g(theta_34[1], o_4)
        return BladeState(o_4, a, b, g)

    def calc_blade_states(self, start_theta_2, end_theta_2, num_points=NUM_POINTS):
        """Calculates blade states for a range of theta_2 values

        Args:
            start_theta_2 (float): In radians
            end_theta_2 (float): In radians
            num_points (int, optional): Number of points to calculate blade state for. Defaults to NUM_POINTS.

        Returns:
            (BladeState): List of blade states over the given range of theta_2 values
        """
        theta_2s = np.arange(
            start_theta_2, end_theta_2, (end_theta_2 - start_theta_2) / num_points
        )
        return [self.calc_blade_state(theta_2) for theta_2 in theta_2s]

    def plot_blade_motion(self, blade_states):
        """Plots the motion of the blade through a series of blade states

        Args:
            blade_states ([BladeState]): Geometric states of the blade to plot
        """
        plt.figure()

        x = [
            [
                0,
                blade_state.o_4.x,
                0,
                blade_state.a.x,
                blade_state.b.x,
                blade_state.o_4.x,
                blade_state.g.x,
                blade_state.b.x,
            ]
            for blade_state in blade_states
        ]
        y = [
            [
                0,
                blade_state.o_4.y,
                0,
                blade_state.a.y,
                blade_state.b.y,
                blade_state.o_4.y,
                blade_state.g.y,
                blade_state.b.y,
            ]
            for blade_state in blade_states
        ]

        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        (line,) = ax.plot(x[0], y[0], color="k")
        ani = animation.FuncAnimation(
            fig, self.update_line, len(x), fargs=[x, y, line], interval=1, blit=False
        )
        plt.show()

    def update_line(self, num, x, y, line):
        line.set_data(x[num], y[num])
        line.axes.axis(self.PLOT_RANGE)
        return (line,)

    def calc_point_a(self, theta_2, o_4):
        """Calculates x and y coordinates of point a

        Args:
            theta_2 (float): In radians
            o_4 ((x:float,y:float)): in mm

        Returns:
            (x:float, y:float): Coordinates of point a
        """
        return Coordinate(
            o_4.x + self.c * math.cos(theta_2),
            o_4.y + self.c * math.sin(theta_2),
        )

    def calc_point_b(self, theta_4, o_2):
        """Calculates x and y coordinates of point b

        Args:
            theta_4 (float): In radians
            o_2 ((x:float,y:float)): in mm

        Returns:
            (x:float, y:float): Coordinates of point b
        """
        return Coordinate(
            o_2.x + self.d * math.cos(theta_4),
            o_2.y + self.d * math.sin(theta_4),
        )

    def calc_point_g(self, theta_4, o_4):
        """Calculates x and y coordinates of point g

        Args:
            theta_4 (float): In radians
            o_4 ((x:float,y:float)): in mm

        Returns:
            (x:float, y:float): Coordinates of point g
        """
        return Coordinate(
            o_4.x + self.g * math.cos(theta_4 + self.theta_5),
            o_4.y + self.g * math.sin(theta_4 + self.theta_5),
        )

    def calc_point_o_4(self):
        """Calculates x and y coordinates of point o_4

        Returns:
            (coordinate): Coordinates of point o_4
        """
        return Coordinate(
            self.d * math.cos(self.theta_1), self.d * math.sin(self.theta_1)
        )

    def calc_theta_3_4(self, theta_2):
        """Calculates values of theta 3 and theta 4 given a theta 2 value

        Args:
            theta_2 (float): In radians

        Returns:
            (theta_3: float, theta_4: float): In radians
        """
        return fsolve(
            functools.partial(self.closed_loop_equations, theta_2=theta_2), (0, 0)
        )

    def closed_loop_equations(self, guess, theta_2):
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
