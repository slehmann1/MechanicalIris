import functools
import math

import numpy as np
from scipy.optimize import least_squares


class Blade:
    def __init__(self):
        pass

    @staticmethod
    def calc_closed_loop_equations(theta_a, AC, BC, pinned_radius):
        """Calculates values of theta 3 and theta 4 given a theta 2 value

        Args:
            theta_a (float): In radians
            AC (float): Distance between points A and C
            BC (float): Distance between points B and C
            pinned_radius (float): Radius from the iris center at which one end of the blade is pinned


        Returns:
            (AB, theta_b, theta_c): Thetas measured in radians
        """
        return least_squares(
            functools.partial(
                Blade.closed_loop_equations,
                theta_a=theta_a,
                AC=AC,
                BC=BC,
                pinned_radius=pinned_radius,
            ),
            (BC, np.pi * 3 / 4, np.pi / 4),
            bounds=((BC, np.pi / 2, 0), (AC, np.pi, np.pi / 2)),
        ).x

    @staticmethod
    def closed_loop_equations(guess, theta_a, AC, BC, pinned_radius):
        """Closed-loop equations for crank-slider mechanism of a blade

        Args:
            guess (AB, theta_b, theta_c): Initial guesses for AB, theta_c, and theta_b
            theta_a (float): In radians
            AC (float): Distance between points A and C
            BC (float): Distance between points B and C
            pinned_radius (float): Radius from the iris center at which one end of the blade is pinned

        Returns:
            (Equation 1, Equation 2, Equation 3): Closed loop equations
        """
        AB, theta_b, theta_c = guess
        eq_1 = AC * math.cos(theta_a) + BC * math.cos(theta_c) + AB * math.cos(theta_b)
        eq_2 = AC * math.sin(theta_a) + BC * math.sin(theta_c) + AB * math.sin(theta_b)

        L = (
            -pinned_radius
            - math.sqrt(pinned_radius**2 - (AC * math.cos(theta_a)) ** 2)
            - AC * math.sin(theta_a)
        )

        eq_3 = math.acos((L**2 + AB**2 - BC**2) / (2 * L * AB)) - (
            -np.pi / 2 + theta_b
        )

        return eq_1, eq_2, eq_3
