#!/usr/bin/python

# AUTHOR
#   Daniel Pulido <dpmcmlxxvi@gmail.com>
# COPYRIGHT
#   Copyright (c) 2015 Daniel Pulido <dpmcmlxxvi@gmail.com>
# LICENSE
#   MIT License (http://opensource.org/licenses/MIT)

"""
Test the various methods to scan grid points
"""

from pixelscan import *

import unittest

class TestPixelscan(unittest.TestCase):
    """
    Set of pixelscan tests that run eah scan generator and compares the output
    point coordinates with truth coordinates.
    """

    def test_circlescan(self):
        truth = [(0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1),\
                (-1,0), (-1,1), (0,2), (1,2), (2,1), (2,0), (2,-1),\
                (1,-2), (0,-2), (-1,-2), (-2,-1), (-2,0), (-2,1), (-1,2)]
        x0, y0, r1, r2 = 0, 0, 0, 2
        points = snap(circlescan(x0, y0, r1, r2))
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_circlescan_skip(self):
        truth = [(0,0), (1,1), (1,-1), (-1,-1), (-1,1), (1,2), (2,0), (1,-2),\
                (-1,-2), (-2,0), (-1,2)]
        x0, y0, r1, r2 = 0, 0, 0, 2
        points = snap(skip(circlescan(x0, y0, r1, r2), step=2))
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_gridscan(self):
        truth = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = gridscan(x0, y0, x1, y1)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_gridscan_sample(self):
        random.seed(0)
        truth = [(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = sample(gridscan(x0, y0, x1, y1), probability=0.5)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_gridscan_skip(self):
        truth = [(1,0), (0,1)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = skip(gridscan(x0, y0, x1, y1), start=1, stop=3, step=2)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_gridscan_step(self):
        truth = [(0,0), (2,0), (0,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = gridscan(x0, y0, x1, y1, stepx=2, stepy=2)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_randomscan(self):
        random.seed(0)
        truth = [(5,0), (0,2), (4,2), (4,3), (2,5)]
        x0, y0, x1, y1, npoints = 0, 0, 5, 5, 5
        points = randomscan(x0, y0, x1, y1, npoints)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_ringscan_chebyshev(self):
        truth = [(0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0),\
                (-1,1), (0,2), (1,2), (2,2), (2,1), (2,0), (2,-1), (2,-2),\
                (1,-2), (0,-2), (-1,-2), (-2,-2), (-2,-1), (-2,0), (-2,1),\
                (-2,2), (-1,2)]
        x0, y0, r1, r2 = 0, 0, 0, 2
        points = ringscan(x0, y0, r1, r2, metric=chebyshev)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_ringscan_manhattan(self):
        truth = [(0,0), (0,1), (1,0), (0,-1), (-1,0), (0,2), (1,1), (2,0),\
                (1,-1), (0,-2), (-1,-1), (-2,0), (-1,1)]
        x0, y0, r1, r2 = 0, 0, 0, 2
        points = ringscan(x0, y0, r1, r2, metric=manhattan)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_ringscan_manhattan_skip(self):
        truth = [(0,0), (1,0), (-1,0), (1,1), (1,-1), (-1,-1), (-1,1)]
        x0, y0, r1, r2 = 0, 0, 0, 2
        points = skip(ringscan(x0, y0, r1, r2, metric=manhattan), step=2)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan(self):
        truth = [(0,0), (1,0), (2,0), (2,1), (1,1), (0,1), (0,2), (1,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = snakescan(x0, y0, x1, y1)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_skip(self):
        truth = [(0,0), (2,0), (1,1), (0,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = skip(snakescan(x0, y0, x1, y1), step=2)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_reflection(self):
        truth = [(0,0), (-1,0), (-2,0), (-2,-1), (-1,-1), (0,-1), (0,-2),\
                (-1,-2), (-2,-2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = reflection(snakescan(x0, y0, x1, y1), rx=True, ry=True)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_swap(self):
        truth = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,0), (2,1), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = swap(snakescan(x0, y0, x1, y1))
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_rotation(self):
        truth = [(0,0), (0,1), (0,2), (-1,2), (-1,1), (-1,0), (-2,0), (-2,1),\
                (-2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = snap(rotation(snakescan(x0, y0, x1, y1), angle=90))
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_translation(self):
        truth = [(1,1), (2,1), (3,1), (3,2), (2,2), (1,2), (1,3), (2,3), (3,3)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = translation(snakescan(x0, y0, x1, y1), tx=1, ty=1)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_scale(self):
        truth = [(0,0), (2,0), (4,0), (4,2), (2,2), (0,2), (0,4), (2,4), (4,4)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = scale(snakescan(x0, y0, x1, y1), sx=2, sy=2)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

if __name__ == "__main__":
    unittest.main()
