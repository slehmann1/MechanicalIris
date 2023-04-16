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
