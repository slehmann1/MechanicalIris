import unittest
from dataclasses import dataclass

import numpy as np

from iris import Iris


@dataclass
class IrisParams:
    innerRadius: float
    outerRadius: float
    bladeWidth: float


class TestIris(unittest.TestCase):
    _PERMISSIBLE_ERROR = 0.2
    _SHOULD_DRAW = False

    def test_bx_range(self):
        # Inner radius, outer radius,
        irises = [
            IrisParams(0, 1, 0.5),
            IrisParams(50, 100, 30),
            IrisParams(0.5, 1, 0.3),
            IrisParams(90, 100, 30),
            IrisParams(0.8, 1, 0.3),
        ]
        for params in irises:
            iris = Iris(
                4, np.pi, params.innerRadius, params.outerRadius, params.bladeWidth
            )
            if self._SHOULD_DRAW:
                iris.drawIris()
            self.assertAlmostEqual(
                iris.blades[0].Bx_range[0],
                params.innerRadius + params.bladeWidth,
                delta=(params.outerRadius + params.bladeWidth)
                * self._PERMISSIBLE_ERROR,
            )
            self.assertAlmostEqual(
                iris.blades[0].Bx_range[1],
                params.outerRadius + params.bladeWidth,
                delta=(params.outerRadius + params.bladeWidth)
                * self._PERMISSIBLE_ERROR,
            )
