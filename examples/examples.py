#!/usr/bin/python

from pixelscan.pixelscan import (chebyshev, circlescan, gridscan, hilbertscan,
    manhattan,  ringscan, skip, snap, snakescan, walkscan)

import random

def printpoints(filename, points):

    with open(filename, "w") as f:
        for x, y in points:
            f.write("{},{}\n".format(x, y))

def main():

    x0, y0, r1, r2 = 0, 0, 0, 2
    points = snap(circlescan(x0, y0, r1, r2))
    printpoints("circlescan.csv", points)

    x0, y0, x1, y1 = 0, 0, 2, 2
    points = gridscan(x0, y0, x1, y1)
    printpoints("gridscan.csv", points)

    size, distance = 4, 16
    points = hilbertscan(size, distance)
    printpoints("hilbertscan.csv", points)

    x0, y0, r1, r2 = 0, 0, 0, 2
    points = ringscan(x0, y0, r1, r2, metric=chebyshev)
    printpoints("chebyshev.csv", points)

    x0, y0, r1, r2 = 0, 0, 0, 2
    points = ringscan(x0, y0, r1, r2, metric=manhattan)
    printpoints("manhattan.csv", points)

    x0, y0, x1, y1 = 0, 0, 2, 2
    points = snakescan(x0, y0, x1, y1)
    printpoints("snakescan.csv", points)

    random.seed(0)
    x0, y0 = 0, 0
    points = skip(walkscan(x0, y0), stop=8)
    printpoints("walkscan.csv", points)

if __name__ == "__main__":
    main()