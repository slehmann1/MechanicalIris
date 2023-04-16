import unittest

import numpy as np

import geometry
from geometry import Coordinate


class TestGeometry(unittest.TestCase):
    def test_get_circle(self):
        center, radius = geometry.get_circle(
            Coordinate(1.1, 1), Coordinate(2.1, 4), Coordinate(5.1, 3)
        )
        self.assertAlmostEqual(center.x, 3.1, delta=0.001)
        self.assertAlmostEqual(center.y, 2, delta=0.001)
        self.assertAlmostEqual(radius, 2.23606798, delta=0.001)

    def test_angle(self):
        self.assertAlmostEqual(Coordinate(1, 1).angle(), np.pi / 4)
        self.assertAlmostEqual(Coordinate(-1, 1).angle(), 3 * np.pi / 4)
        self.assertAlmostEqual(Coordinate(-1, -1).angle(), 5 * np.pi / 4)
        self.assertAlmostEqual(Coordinate(1, -1).angle(), 7 * np.pi / 4)

    def test_rotate_coordinate(self):
        coord = Coordinate(1, 2)

        self.assertAlmostEquals(coord.angle(), 63.43494882 * np.pi / 180)

        coord.rotate(np.pi)
        self.assertAlmostEqual(coord.x, -1)
        self.assertAlmostEqual(coord.y, -2)

        self.assertAlmostEquals(coord.angle(), 243.43494882 * np.pi / 180)

        coord.rotate(-63.43494882 * np.pi / 180)
        self.assertAlmostEqual(coord.x, -2.236067977)
        self.assertAlmostEqual(coord.y, 0)
        self.assertAlmostEquals(coord.angle(), 180 * np.pi / 180)
