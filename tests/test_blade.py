import math
import unittest

import numpy as np

from iris_calculator.blade import Blade


class TestBlade(unittest.TestCase):
    def test_calc_AB(self):
        # Tested against values generated with Solidworks
        blade = Blade(0, 45, 50.5, 60, 1.5)
        # AB
        self.assertAlmostEqual(
            blade.calc_closed_loop_equations(285 * np.pi / 180)[0],
            67.50524683,
            4,
        )
        # theta_b
        self.assertAlmostEqual(
            blade.calc_closed_loop_equations(285 * np.pi / 180)[1],
            141.44560829 * np.pi / 180,
            4,
        )
        # theta_c
        self.assertAlmostEqual(
            blade.calc_closed_loop_equations(285 * np.pi / 180)[2],
            63.058709 * np.pi / 180,
            4,
        )

    def test_calc_bx(self):
        blade = Blade(0, 55, 66, 75, 20, 1)
        self.assertAlmostEqual(
            blade.calc_Bx(277.73007783 * np.pi / 180), -59.7198989, delta=0.5
        )

    def test_calc_theta_a(self):
        blade = Blade(0, 55, 66, 75, 2)

        self.assertAlmostEqual(
            blade.calc_theta_a(59.7198989) * 180 / np.pi, 277.73007783, delta=5
        )
        self.assertAlmostEqual(blade.calc_theta_a(45) * 180 / np.pi, 264.65, delta=5)
        self.assertAlmostEqual(blade.calc_theta_a(20) * 180 / np.pi, 244.56, delta=5)

    def test_get_AC(self):
        blade = Blade(0, 45, 50.5, 60, 1)

        self.assertAlmostEqual(
            blade.get_AC(67.50524683, 141.44560829 * np.pi / 180),
            98.93245399,
            delta=0.00001,
        )

    def test_get_AB(self):
        blade = Blade(0, 45, 50.5, 60, 1)
        self.assertAlmostEqual(
            blade.get_AB(98.93245399, 141.44560829 * np.pi / 180),
            67.50524683,
            delta=0.00001,
        )

    def test_get_AB2(self):
        blade = Blade(0, 55, 66, 75, 20)
        self.assertAlmostEqual(
            blade.get_AB(126.96905281, 295.66873999 * np.pi / 180),
            83.974614,
            delta=0.00001,
        )

    def test_calc_blade_state(self):
        blade = Blade(0, 45, 50.5, 60, 1)
        state = blade.calc_blade_state(270 * np.pi / 180)
        self.assertAlmostEqual(state.A.x, 0)
        self.assertAlmostEqual(state.B.x, 39.68626967)
        self.assertAlmostEqual(state.C.x, 0)
        self.assertAlmostEqual(state.A.y, 53.73953386)
        self.assertAlmostEqual(state.B.y, 0)
        self.assertAlmostEqual(state.C.y, -45)

        state = blade.calc_blade_state(280 * np.pi / 180)
        self.assertAlmostEqual(state.A.x, 0)
        self.assertAlmostEqual(state.B.x, 48.43715046)
        self.assertAlmostEqual(state.C.x, 17.14741984)
        self.assertAlmostEqual(state.A.y, 55.64297094)
        self.assertAlmostEqual(state.B.y, 9.59036212)
        self.assertAlmostEqual(state.C.y, -41.60487944)
