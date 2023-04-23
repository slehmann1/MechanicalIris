import functools
import math
from dataclasses import dataclass

import matplotlib.patches as patch
import numpy as np
from scipy.optimize import Bounds, least_squares, minimize

import geometry
from geometry import Coordinate


@dataclass
class BladeState:
    A: Coordinate
    B: Coordinate
    C: Coordinate
    D: Coordinate

    def rotated_copy(self, angle):
        return BladeState(
            *[coord.rotated_copy(angle) for coord in [self.A, self.B, self.C, self.D]]
        )


class Blade:
    _NUM_POINTS = 50
    _COLOUR = "black"
    _BLADE_WIDTH = 10

    # Domain limits are rounded from values of 243.434 and 296.565
    _DOMAIN_LIMITS = (245 * np.pi / 180, 295 * np.pi / 180)

    def __init__(
        self,
        rotation_angle,
        blade_angle,
        pinned_radius,
        blade_radius,
        BC,
        blade_width=None,
    ):
        """An individual blade of an iris

        Args:
            rotation_angle (float): Rotation angle of the entire blade within the iris
            blade_angle (float): Angle that is subtended tip to tail of the entire blade
            pinned_radius (float): Radius at which the blade is pinned
            blade_radius (float): Radius of the blade arc
            BC (float): Length from point B to point C
            blade_width (float, optional): Width of the blade from the internal radius to the outer radius. Defaults to None.
            internal_radius (float, optional): Minimum internal radius of the iris when closed. Defaults to None.
        """
        if blade_width is None:
            blade_width = self._BLADE_WIDTH
        self.rotation_angle = rotation_angle
        self.blade_angle = blade_angle
        self.pinned_radius = pinned_radius
        self.blade_radius = blade_radius
        self.BC = BC
        self.blade_width = blade_width
        self.theta_a_range, self.Bx_range = self.calc_Bx_range()

    def set_theta_a_domain(self, inner_radius=None, outer_radius=None):
        """Determines the range of theta_a values that are valid for the blade to rotate through

        Returns:
            (float, float): Theta_a domain in radians
        """
        lower_limit, upper_limit = self.theta_a_range

        if inner_radius:
            a_bx_bound = self.calc_theta_a(inner_radius)
            if a_bx_bound > lower_limit:
                lower_limit = a_bx_bound

        if outer_radius:
            a_bx_bound = self.calc_theta_a(outer_radius)
            if a_bx_bound < upper_limit:
                upper_limit = a_bx_bound

        self.theta_a_range = [lower_limit, upper_limit]

        return (lower_limit, upper_limit)

    def draw(self, axs, blade_state):
        center, radius = geometry.get_circle(
            blade_state.A, blade_state.B, blade_state.C
        )

        # Midline
        axs.add_patch(
            patch.Arc(
                (center.x, center.y),
                radius * 2,
                radius * 2,
                theta1=(blade_state.C - center).angle() * 180 / np.pi,
                theta2=(blade_state.D - center).angle() * 180 / np.pi,
                color=self._COLOUR,
                linestyle="dashed",
            )
        )

        # Inner radius
        axs.add_patch(
            patch.Arc(
                (center.x, center.y),
                radius * 2 - self.blade_width,
                radius * 2 - self.blade_width,
                theta1=(blade_state.C - center).angle() * 180 / np.pi,
                theta2=(blade_state.D - center).angle() * 180 / np.pi,
                color=self._COLOUR,
            )
        )

        # Outer radius
        axs.add_patch(
            patch.Arc(
                (center.x, center.y),
                radius * 2 + self.blade_width,
                radius * 2 + self.blade_width,
                theta1=(blade_state.C - center).angle() * 180 / np.pi,
                theta2=(blade_state.D - center).angle() * 180 / np.pi,
                color=self._COLOUR,
            )
        )

        # End slot
        axs.add_patch(
            patch.Arc(
                (blade_state.D.x, blade_state.D.y),
                self.blade_width,
                self.blade_width,
                theta1=(blade_state.D - center).angle() * 180 / np.pi,
                theta2=(blade_state.D - center).angle() * 180 / np.pi + 180,
                color=self._COLOUR,
            )
        )

        # End slot
        axs.add_patch(
            patch.Arc(
                (blade_state.C.x, blade_state.C.y),
                self.blade_width,
                self.blade_width,
                theta1=(blade_state.C - center).angle() * 180 / np.pi + 180,
                theta2=(blade_state.C - center).angle() * 180 / np.pi,
                color=self._COLOUR,
            )
        )

        axs.scatter(
            [
                state.x
                for state in [
                    blade_state.A,
                    blade_state.B,
                    blade_state.C,
                    blade_state.D,
                ]
            ],
            [
                state.y
                for state in [
                    blade_state.A,
                    blade_state.B,
                    blade_state.C,
                    blade_state.D,
                ]
            ],
            color=self._COLOUR,
        )

    def calc_blade_state(self, theta_a):
        AB, theta_b, _ = self.calc_closed_loop_equations(theta_a)

        AC = self.get_AC(AB, theta_a)
        A = Coordinate(0, self.pinned_radius + self.get_L(AC, theta_a))

        B = A - Coordinate(AB * math.cos(theta_b), AB * math.sin(theta_b))

        C = A - Coordinate(
            -AC * math.cos(theta_a),
            -AC * math.sin(theta_a),
        )
        center, radius = geometry.get_circle(A, B, C)

        D = geometry.get_chord_coord(C, center, self.blade_angle, radius)

        A.rotate(self.rotation_angle)
        B.rotate(self.rotation_angle)
        C.rotate(self.rotation_angle)
        D.rotate(self.rotation_angle)

        return BladeState(A, B, C, D)

    def calc_blade_states(self, start_theta_a, end_theta_a, num_points=_NUM_POINTS):
        """Calculates blade states for a range of theta_a values

        Args:
            start_theta_a (float): In radians
            end_theta_a (float): In radians
            num_points (int, optional): Number of points to calculate blade state for. Defaults to NUM_POINTS.

        Returns:
            (BladeState): List of blade states over the given range of theta_a values
        """
        step_size = (end_theta_a - start_theta_a) / num_points
        theta_as = np.arange(start_theta_a, end_theta_a + step_size, step_size)
        return [self.calc_blade_state(theta_a) for theta_a in theta_as]

    def calc_closed_loop_equations(self, theta_a):
        """Calculates values of AB, theta_b, and theta_c given a theta_a value

        Args:
            theta_a (float): In radians

        Returns:
            (AB, theta_b, theta_c): Thetas measured in radians
        """
        return least_squares(
            functools.partial(self.closed_loop_equations, theta_a=theta_a),
            (self.BC, np.pi * 3 / 4, np.pi / 4),
            bounds=(
                (self.pinned_radius, np.pi / 2, 0),
                (80, np.pi, np.pi / 2),
            ),
        ).x

    def get_L(self, AC, theta_a):
        return (
            -self.pinned_radius
            - math.sqrt(self.pinned_radius**2 - (AC * math.cos(theta_a)) ** 2)
            - AC * math.sin(theta_a)
        )

    def get_AC(self, AB, theta_b):
        A = Coordinate(0, 0)
        B = Coordinate(-AB * math.cos(theta_b), -AB * math.sin(theta_b))
        center = geometry.get_circle_center(A, B, self.blade_radius, True)
        alpha = 2 * math.asin(self.BC / 2 / self.blade_radius)
        C = geometry.get_chord_coord(B, center, alpha, self.blade_radius)
        return (C - A).magnitude()

    def get_AB(self, AC, theta_c):
        A = Coordinate(0, 0)
        C = Coordinate(-AC * math.cos(theta_c), -AC * math.sin(theta_c))
        center = geometry.get_circle_center(A, C, self.blade_radius, True)
        alpha = 2 * math.asin(self.BC / 2 / self.blade_radius)
        B = geometry.get_chord_coord(C, center, -alpha, self.blade_radius)
        return (B - A).magnitude()

    def closed_loop_equations(self, guess, theta_a):
        """Closed-loop equations for crank-slider mechanism of a blade

        Args:
            guess (AB, theta_b, theta_c): Initial guesses for AB, theta_c, and theta_b
            theta_a (float): In radians

        Returns:
            (Equation 1, Equation 2, Equation 3): Closed loop equations
        """
        AB, theta_b, theta_c = guess
        AC = self.get_AC(AB, theta_b)

        eq_1 = (
            AC * math.cos(theta_a)
            + self.BC * math.cos(theta_c)
            + AB * math.cos(theta_b)
        )
        eq_2 = (
            AC * math.sin(theta_a)
            + self.BC * math.sin(theta_c)
            + AB * math.sin(theta_b)
        )
        L = self.get_L(AC, theta_a)

        try:
            eq_3 = math.acos((L**2 + AB**2 - self.BC**2) / (2 * L * AB)) - (
                -np.pi / 2 + theta_b
            )
        except:
            return eq_1, eq_2, np.inf

        # print(
        #    f"L: {L} AB: {AB} BC: {self.BC} Theta_A: {theta_a*180/np.pi} Theta_B: {theta_b*180/np.pi} Theta_C: {theta_c*180/np.pi}"
        # )

        return eq_1, eq_2, eq_3

    def calc_Bx(self, theta_a):
        """Calculates the x position of point B
        Args:
            theta_a (float): Measured in rad
        Returns:
            float: X position of point B in an unrotated state
        """
        # TODO: DETERMINE AB UPPER RANGE
        res = least_squares(
            functools.partial(self.closed_loop_equations, theta_a=theta_a),
            (self.BC, np.pi * 3 / 4, np.pi / 4),
            bounds=(
                (0, np.pi / 2, 0),
                (80, np.pi, np.pi / 2),
            ),
        ).x
        return res[0] * math.cos(res[1])

    def calc_theta_a(self, Bx):
        # Bx = -1
        print(f"FINDING {Bx} {self._DOMAIN_LIMITS[0], self._DOMAIN_LIMITS[1]}")
        return minimize(
            lambda theta_a: abs(abs(self.calc_Bx(theta_a)) - Bx),
            4.7,
            bounds=(Bounds(self._DOMAIN_LIMITS[0], self._DOMAIN_LIMITS[1])),
        ).x[0]

    def calc_Bx_range(self):
        """Calculates the range of x values that point B can take

        Returns:
            ((float, float), (float, float)): ((min_theta_a, max_theta_a), (min_Bx, max_Bx)) theta_a is measured in rad
        """
        min_theta_a = minimize(
            lambda theta_a: -self.calc_Bx(theta_a),
            4.0,
            bounds=(Bounds(self._DOMAIN_LIMITS[0], self._DOMAIN_LIMITS[1])),
        ).x[0]
        max_theta_a = minimize(
            self.calc_Bx,
            4.0,
            bounds=(Bounds(self._DOMAIN_LIMITS[0], self._DOMAIN_LIMITS[1])),
        ).x[0]

        min_Bx = -self.calc_Bx(min_theta_a)
        max_Bx = -self.calc_Bx(max_theta_a)

        print(f"Min BX {min_Bx} Max BX {max_Bx}")

        return (min_theta_a, max_theta_a), (min_Bx, max_Bx)
