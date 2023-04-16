import functools
import math
from dataclasses import dataclass

import matplotlib.patches as patch
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

import geometry
from geometry import Coordinate


@dataclass
class BladeState:
    A: Coordinate
    B: Coordinate
    C: Coordinate


class Blade:
    _NUM_POINTS = 50
    _COLOUR = "black"

    def __init__(self, rotation_angle, pinned_radius, AC, BC):
        self.rotation_angle = rotation_angle
        self.pinned_radius = pinned_radius
        self.AC = AC
        self.BC = BC

    def draw(self, axs, blade_state):
        center, radius = geometry.get_circle(
            blade_state.A, blade_state.B, blade_state.C
        )

        axs.add_patch(
            patch.Arc(
                (center.x, center.y),
                radius * 2,
                radius * 2,
                theta1=(blade_state.C - center).angle() * 180 / np.pi,
                theta2=(blade_state.A - center).angle() * 180 / np.pi,
                color=self._COLOUR,
            )
        )

        axs.scatter(
            [state.x for state in [blade_state.A, blade_state.B, blade_state.C]],
            [state.y for state in [blade_state.A, blade_state.B, blade_state.C]],
            color=self._COLOUR,
        )

    def calc_blade_states(self, start_theta_a, end_theta_a, num_points=_NUM_POINTS):
        """Calculates blade states for a range of theta_a values

        Args:
            start_theta_a (float): In radians
            end_theta_a (float): In radians
            num_points (int, optional): Number of points to calculate blade state for. Defaults to NUM_POINTS.

        Returns:
            (BladeState): List of blade states over the given range of theta_a values
        """
        theta_as = np.arange(
            start_theta_a, end_theta_a, (end_theta_a - start_theta_a) / num_points
        )
        return [self.calc_blade_state(theta_a) for theta_a in theta_as]

    def calc_blade_state(self, theta_a):
        AB, theta_b, _ = self.calc_closed_loop_equations(
            theta_a, self.AC, self.BC, self.pinned_radius
        )

        A = Coordinate(
            0, self.pinned_radius + self.get_L(self.pinned_radius, self.AC, theta_a)
        )

        B = A - Coordinate(AB * math.cos(theta_b), AB * math.sin(theta_b))

        C = A - Coordinate(
            self.AC * math.cos(theta_a),
            -self.AC * math.sin(theta_a),
        )

        A.rotate(self.rotation_angle)
        B.rotate(self.rotation_angle)
        C.rotate(self.rotation_angle)

        return BladeState(A, B, C)

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
    def get_L(pinned_radius, AC, theta_a):
        return (
            -pinned_radius
            - math.sqrt(pinned_radius**2 - (AC * math.cos(theta_a)) ** 2)
            - AC * math.sin(theta_a)
        )

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

        L = Blade.get_L(pinned_radius, AC, theta_a)

        eq_3 = math.acos((L**2 + AB**2 - BC**2) / (2 * L * AB)) - (
            -np.pi / 2 + theta_b
        )

        return eq_1, eq_2, eq_3
