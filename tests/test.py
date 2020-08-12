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

from pixelscan.pixelscan import *

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

    def test_gridscan_sample_exception(self):
        x0, y0, x1, y1 = 0, 0, 2, 2
        with self.assertRaises(ValueError):
            points = sample(gridscan(x0, y0, x1, y1), probability=2)

    def test_gridscan_sample_all(self):
        random.seed(0)
        truth = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = sample(gridscan(x0, y0, x1, y1), probability=1)
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

    def test_hilbertscan(self):
        truth = [(0,0), (0,1), (1,1), (1,0), (2,0), (3,0), (3,1), (2,1), \
                (2,2), (3,2), (3,3), (2,3), (1,3), (1,2), (0,2), (0,3)]
        size, distance = 4, 16
        points = hilbertscan(size, distance)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_reservoirscan(self):
        random.seed(0)
        truth = [(4,5), (2,0), (1,0), (2,1), (1,4)]
        x0, y0, x1, y1, npoints = 0, 0, 5, 5, 5
        points = reservoir(gridscan(x0, y0, x1, y1), npoints)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_ringscan_badmetric(self):
        def badmetric(x, y):
            return 3
        truth = [(0,0)]
        x0, y0, r1, r2 = 0, 0, 0, 2
        points = ringscan(x0, y0, r1, r2, metric=badmetric)
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

    def test_snakescan_clip(self):
        truth = [(2,1), (1,1), (1,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = clip(snakescan(x0, y0, x1, y1), minx=1, miny=1)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_clip_abort(self):
        truth = [(0,0), (1,0), (2,0), (2,1), (1,1), (0,1)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = clip(snakescan(x0, y0, x1, y1), maxy=1, abort=True)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_clip_predicate(self):
        def predicate(x, y):
            return True if y >= 1 else False
        truth = [(2,1), (1,1), (0,1), (0,2), (1,2), (2,2)]
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = clip(snakescan(x0, y0, x1, y1), predicate=predicate)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_clip_predicate_abort(self):
        def predicate(x, y):
            return True if y >= 1 else False
        truth = []
        x0, y0, x1, y1 = 0, 0, 2, 2
        points = clip(snakescan(x0, y0, x1, y1), predicate=predicate, abort=True)
        npoints = len([point for point in enumerate(points)])
        self.assertEqual(npoints, len(truth))

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
        points = rotation(snakescan(x0, y0, x1, y1), angle=90)
        for index, point in enumerate(points):
            x = int(round(point[0]))
            y = int(round(point[1]))
            self.assertEqual((x,y), truth[index])
        self.assertEqual(index+1, len(truth))

    def test_snakescan_rotation_snap(self):
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

    def test_walkscan_abort(self):
        random.seed(0)
        truth =[(0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (3,1), (3,2)]
        x0, y0 = 0, 0
        points = clip(walkscan(x0, y0), maxx=3, abort=True)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

    def test_walkscan_skip(self):
        random.seed(1)
        truth =[(0,0), (-1,0), (-1,1), (-1,2), (0,2), (1,2), (2,2), (2,1),\
                (2,2)]
        x0, y0 = 0, 0
        points = skip(walkscan(x0, y0), stop=8)
        for index, point in enumerate(points):
            self.assertEqual(point, truth[index])
        self.assertEqual(index+1, len(truth))

if __name__ == "__main__":
    unittest.main()
