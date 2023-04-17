import unittest

import numpy as np

from blade import Blade


class TestBlade(unittest.TestCase):
    def test_calc_AB(self):
        # Tested against values generated with Solidworks
        self.assertAlmostEqual(
            Blade.calc_closed_loop_equations(285 * np.pi / 180, 100, 60, 45)[0],
            68.21810978,
            4,
        )
        self.assertAlmostEqual(
            Blade.calc_closed_loop_equations(285 * np.pi / 180, 100, 60, 45)[1],
            140.88704529 * np.pi / 180,
            4,
        )
        self.assertAlmostEqual(
            Blade.calc_closed_loop_equations(285 * np.pi / 180, 100, 60, 45)[2],
            63.20413705 * np.pi / 180,
            4,
        )

    def test_get_AC(self):
        self.assertAlmostEqual(
            Blade.get_AC(62.52845541, 53.609793, 117.85005696 * np.pi / 180, 84.373947),
            109.082695551,
            delta=0.00001,
        )

    def test_get_AB(self):
        self.assertAlmostEqual(
            Blade.get_AB(
                109.082695551, 53.609793, 77.57752752 * np.pi / 180, 84.373947
            ),
            62.52845541,
            delta=0.00001,
        )

    def test_calc_blade_state(self):
        blade = Blade(0, 45, 50.5, 60)
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
