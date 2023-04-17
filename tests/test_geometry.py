import unittest

import numpy as np

import geometry
from geometry import Coordinate


class TestGeometry(unittest.TestCase):
    def test_get_circle(self):
        # Tested against SolidWorks geometry
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

    def test_get_circle_center(self):
        # Tested against SolidWorks geometry
        coord = geometry.get_circle_center(
            Coordinate(17.67829657, -44.43898377),
            Coordinate(29.21074847, 7.9156961),
            84.373947,
        )
        self.assertAlmostEqual(coord.x, -54.68532599, delta=0.00001)
        self.assertAlmostEqual(coord.y, -1.05155445, delta=0.00001)

    def test_get_chord_coord(self):
        coord = geometry.get_chord_coord(
            Coordinate(17.67829657, -44.43898377),
            Coordinate(-54.68532599, -1.05155445),
            37.04676356 * np.pi / 180,
            84.373947,
        )
        self.assertAlmostEqual(coord.x, 29.21074847, delta=0.00001)
        self.assertAlmostEqual(coord.y, 7.9156961, delta=0.00001)

        coord = geometry.get_chord_coord(
            Coordinate(29.21074847, 7.9156961),
            Coordinate(-54.68532599, -1.05155445),
            322.9532364 * np.pi / 180,
            84.373947,
        )
        self.assertAlmostEqual(coord.x, 17.67829657, delta=0.00001)
        self.assertAlmostEqual(coord.y, -44.43898377, delta=0.00001)
