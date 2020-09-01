#!/usr/bin/python

# AUTHOR
#   Daniel Pulido <dpmcmlxxvi@gmail.com>
# COPYRIGHT
#   Copyright (c) 2015 Daniel Pulido <dpmcmlxxvi@gmail.com>
# LICENSE
#   MIT License (http://opensource.org/licenses/MIT)

"""
Various patterns to scan pixels on a grid. Rectangular patterns are scanned
first along the x-coordinate then the y-coordinate. Radial patterns are
scanned clockwise. Transformation filters are available to apply
standard transformations (e.g., rotation, scale, translation) on the
coordinates.
"""

import math
import random
import sys

from math import frexp, copysign
from sys import float_info

# ======================================================================
# Distance metrics
# ----------------------------------------------------------------------


def chebyshev(point1, point2):
    """Computes distance between 2D points using chebyshev metric

    :param point1: 1st point
    :type point1: list
    :param point2: 2nd point
    :type point2: list
    :returns: Distance between point1 and point2
    :rtype: float
    """

    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def manhattan(point1, point2):
    """Computes distance between 2D points using manhattan metric

    :param point1: 1st point
    :type point1: list
    :param point2: 2nd point
    :type point2: list
    :returns: Distance between point1 and point2
    :rtype: float
    """

    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def hilbertrot(n, x, y, rx, ry):
    """Rotates and flips a quadrant appropriately for the Hilbert scan
    generator. See https://en.wikipedia.org/wiki/Hilbert_curve.
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        return y, x
    return x, y

# ======================================================================
# Scan transformations
# ----------------------------------------------------------------------


class clip(object):
    """Clip coordinates that exceed boundary
    """
    def __init__(self,
                 scan,
                 minx=-sys.maxsize,
                 maxx=sys.maxsize,
                 miny=-sys.maxsize,
                 maxy=sys.maxsize,
                 predicate=None,
                 abort=False):

        """
        :param scan: Pixel scan generator
        :type scan: function
        :param minx: Minimum x-coordinate (default = -sys.maxsize)
        :type minx: int
        :param maxx: Maximum x-coordinate (default =  sys.maxsize)
        :type maxx: int
        :param miny: Minimum y-coordinate (default = -sys.maxsize)
        :type miny: int
        :param maxy: Maximum y-coordinate (default =  sys.maxsize)
        :type maxy: int
        :param predicate: Optional function that takes 2 arguments (x and y)
                          and returns true if coordinate should be kept
                          otherwise false (default = None)
        :type predicate: function
        :param abort: Abort iteration if boundary is crossed
        :type abort: bool
        """
        self.scan = scan
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.predicate = predicate
        self.abort = abort

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        while True:
            x, y = next(self.scan)
            if self.predicate is not None and not self.predicate(x, y):
                if self.abort:
                    raise StopIteration("Boundary crossed!")
            elif (x < self.minx or
                  x > self.maxx or
                  y < self.miny or
                  y > self.maxy):
                if self.abort:
                    raise StopIteration("Boundary crossed!")
            else:
                return x, y


class reflection(object):
    """Reflect coordinates about x and y axes
    """
    def __init__(self, scan, rx=False, ry=False):
        """
        :param scan: Pixel scan generator
        :type scan: function
        :param rx: True if x-coordinate should be reflected (default=False)
        :type rx: bool
        :param ry: True if y-coordinate should be reflected (default=False)
        :type ry: bool
        """
        self.scan = scan
        self.rx = rx
        self.ry = ry

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        x, y = next(self.scan)
        xr = -x if self.rx else x
        yr = -y if self.ry else y
        return xr, yr


class reservoir(object):

    def __init__(self, scan, npoints):
        """Randomly sample points using the reservoir sampling method. This is
        only useful if you need exactly 'npoints' sampled. Otherwise use the
        'sample' transformation to randomly sample at a given rate. This method
        requires storing 'npoints' in memory and precomputing the random
        selection so it may be slower than 'sample'.

        :param scan: Pixel scan generator
        :type scan: function
        :param npoints: Sample size
        :type npoints: int
        """
        # Validate inputs
        if npoints <= 0:
            raise ValueError("Sample size must be positive")

        self.reservoir = []
        self.count = 0

        # Populate reservoir
        for index, point in enumerate(scan):
            if index < npoints:
                self.reservoir.append(point)
            else:
                j = random.randint(0, index)
                if j < npoints:
                    self.reservoir[j] = point

        # Shuffle the reservoir in case population was small and the
        # points were not sufficiently randomized
        random.shuffle(self.reservoir)

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        if self.count < len(self.reservoir):
            self.count += 1
            return self.reservoir[self.count-1]

        raise StopIteration("Reservoir exhausted")


class rotation(object):
    """Rotate coordinates by given angle. If the final transformation axes do
    not align with the x and y axes then it may yield duplicate coordinates
    during scanning.
    """

    def __init__(self, scan, angle=0):
        """
        :param scan: Pixel scan generator
        :type scan: function
        :param angle: Counter-clockwise angle in degrees (default=0)
        :type angle: float
        """
        self.scan = scan
        self.angle = angle * (math.pi / 180.0)

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        x, y = next(self.scan)
        ca, sa = math.cos(self.angle), math.sin(self.angle)
        xr = ca * x - sa * y
        yr = sa * x + ca * y
        return xr, yr


class sample(object):
    """Randomly sample points at the given probability.
    """
    def __init__(self, scan, probability=1):
        """
        :param scan: Pixel scan generator
        :type scan: function
        :param probability: Sampling probability in interval [0,1] (default=1)
        :type probability: float
        """
        if probability < 0 or probability > 1:
            raise ValueError("Sampling probability must be in range [0,1]")
        self.scan = scan
        self.probability = probability

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        if self.probability == 1:
            x, y = next(self.scan)
        else:
            while True:
                x, y = next(self.scan)
                if random.random() <= self.probability:
                    break
        return x, y


class scale(object):
    """Scale coordinates by given factor
    """

    def __init__(self, scan, sx=1, sy=1):
        """
        :param scan: Pixel scan generator
        :type scan: function
        :param sx: x-coordinate scale factor (default=1)
        :type sx: float
        :param sy: y-coordinate scale factor (default=1)
        :type sy: float
        """
        if sx <= 0:
            raise ValueError("X-scale must be positive")
        if sy <= 0:
            raise ValueError("Y-scale must be positive")
        self.scan = scan
        self.sx = sx
        self.sy = sy

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        x, y = next(self.scan)
        xr = self.sx * x
        yr = self.sy * y
        return xr, yr


class skip(object):
    """Skip points at the given step size
    """
    def __init__(self, scan, start=0, stop=sys.maxsize, step=1):
        """
        :param scan: Pixel scan generator
        :type scan: function
        :param start: Iteration starting 0-based index (default = 0)
        :type start: int
        :param stop: Iteration stopping 0-based index (default = sys.maxsize)
        :type stop: int
        :param step: Iteration step size (default = 1)
        :type step: int
        """
        if start < 0:
            raise ValueError("Start must be non-negative")
        if stop < 0:
            raise ValueError("Stop must be non-negative")
        if stop < start:
            raise ValueError("Stop must be greater than start")
        if step <= 0:
            raise ValueError("Step must be positive")
        self.scan = scan
        self.start = start
        self.stop = stop
        self.step = step
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        while True:
            x, y = next(self.scan)
            self.index += 1
            if (self.index < self.start):
                continue
            if (self.index > self.stop):
                raise StopIteration("skip stopping")
            if ((self.index-self.start) % self.step != 0):
                continue
            return x, y


class snap(object):
    """Snap x and y coordinates to a grid point
    """
    def __init__(self, scan):
        """
        :param scan: Pixel scan generator
        :type scan: function
        """
        self.scan = scan

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        x, y = next(self.scan)
        xs = int(round(x))
        ys = int(round(y))
        return xs, ys


class swap(object):
    """Swap x and y coordinates
    """
    def __init__(self, scan):
        """
        :param scan: Pixel scan generator
        :type scan: function
        """
        self.scan = scan

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        x, y = next(self.scan)
        return y, x


class translation(object):
    """Translate coordinates by given offset
    """

    def __init__(self, scan, tx=0, ty=0):
        """
        :param scan: Pixel scan generator
        :type scan: function
        :param sx: x-coordinate translation offset (default = 0)
        :type sx: float
        :param sy: y-coordinate translaation offset (default = 0)
        :type sy: float
        """
        self.scan = scan
        self.tx = tx
        self.ty = ty

    def __iter__(self):
        return self

    def __next__(self):
        """Next point in iteration
        """
        x, y = next(self.scan)
        xr = x + self.tx
        yr = y + self.ty
        return xr, yr

# ======================================================================
# Scan patterns
# ----------------------------------------------------------------------


def circlescan(x0, y0, r1, r2):
    """Scan pixels in a circle pattern around a center point

    :param x0: Center x-coordinate
    :type x0: float
    :param y0: Center y-coordinate
    :type y0: float
    :param r1: Initial radius
    :type r1: float
    :param r2: Final radius
    :type r2: float
    :returns: Coordinate generator
    :rtype: function
    """

    # Validate inputs
    if r1 < 0:
        raise ValueError("Initial radius must be non-negative")
    if r2 < 0:
        raise ValueError("Final radius must be non-negative")

    # List of pixels visited in previous diameter
    previous = []

    # Scan distances outward (1) or inward (-1)
    rstep = 1 if r2 >= r1 else -1
    for distance in range(r1, r2 + rstep, rstep):

        if distance == 0:

            yield x0, y0

        else:

            # Computes points for first octant and the rotate by multiples of
            # 45 degrees to compute the other octants
            a = 0.707107
            rotations = {0: [[1, 0], [0, 1]],
                         1: [[a, a], [-a, a]],
                         2: [[0, 1], [-1, 0]],
                         3: [[-a, a], [-a, -a]],
                         4: [[-1, 0], [0, -1]],
                         5: [[-a, -a], [a, -a]],
                         6: [[0, -1], [1, 0]],
                         7: [[a, -a], [a, a]]}
            nangles = len(rotations)

            # List of pixels visited in current diameter
            current = []

            for angle in range(nangles):
                x = 0
                y = distance
                d = 1 - distance
                while x < y:
                    xr = rotations[angle][0][0]*x + rotations[angle][0][1]*y
                    yr = rotations[angle][1][0]*x + rotations[angle][1][1]*y
                    xr = x0 + xr
                    yr = y0 + yr

                    # First check  if point was in previous diameter
                    # since our scan pattern can lead to duplicates in
                    # neighboring diameters
                    point = (int(round(xr)), int(round(yr)))
                    if point not in previous:
                        yield xr, yr
                        current.append(point)

                    # Move pixel according to circle constraint
                    if (d < 0):
                        d += 3 + 2 * x
                    else:
                        d += 5 - 2 * (y-x)
                        y -= 1
                    x += 1

            previous = current


def gridscan(xi, yi, xf, yf, stepx=1, stepy=1):
    """Scan pixels in a grid pattern along the x-coordinate then y-coordinate

    :param xi: Initial x-coordinate
    :type xi: int
    :param yi: Initial y-coordinate
    :type yi: int
    :param xf: Final x-coordinate
    :type xf: int
    :param yf: Final y-coordinate
    :type yf: int
    :param stepx: Step size in x-coordinate
    :type stepx: int
    :param stepy: Step size in y-coordinate
    :type stepy: int
    :returns: Coordinate generator
    :rtype: function
    """

    if stepx <= 0:
        raise ValueError("X-step must be positive")
    if stepy <= 0:
        raise ValueError("Y-step must be positive")

    # Determine direction to move
    dx = stepx if xf >= xi else -stepx
    dy = stepy if yf >= yi else -stepy

    for y in range(yi, yf + dy, dy):
        for x in range(xi, xf + dx, dx):
            yield x, y


def hilbertscan(size, distance):
    """Scan pixels in a Hilbert curve pattern in the first quadrant. Modified
    algorithm from https://en.wikipedia.org/wiki/Hilbert_curve.

    :param size: Size of enclosing square
    :type size: int
    :param distance: Distance along curve (Must be smaller than  size**2 - 1)
    :type distance: int
    :returns: Coordinate generator
    :rtype: function
    """

    size = 2 * (1 << (size-1).bit_length())
    if (distance > size**2 - 1):
        raise StopIteration("Invalid distance!")

    for d in range(distance):
        t = d
        x = 0
        y = 0
        s = 1
        while (s < size):
            rx = float_and(1, t / 2)
            ry = float_and(1, float_xor(t, rx))
            x, y = hilbertrot(s, x, y, rx, ry)
            x += s * rx
            y += s * ry
            t /= 4
            s *= 2
        yield x, y


def ringscan(x0, y0, r1, r2, metric=chebyshev):
    """Scan pixels in a ring pattern around a center point clockwise

    :param x0: Center x-coordinate
    :type x0: int
    :param y0: Center y-coordinate
    :type y0: int
    :param r1: Initial radius
    :type r1: int
    :param r2: Final radius
    :type r2: int
    :param metric: Distance metric
    :type metric: function
    :returns: Coordinate generator
    :rtype: function
    """

    # Validate inputs
    if r1 < 0:
        raise ValueError("Initial radius must be non-negative")
    if r2 < 0:
        raise ValueError("Final radius must be non-negative")
    if not hasattr(metric, "__call__"):
        raise TypeError("Metric not callable")

    # Define clockwise step directions
    direction = 0
    steps = {0: [1, 0],
             1: [1, -1],
             2: [0, -1],
             3: [-1, -1],
             4: [-1, 0],
             5: [-1, 1],
             6: [0, 1],
             7: [1, 1]}
    nsteps = len(steps)

    center = [x0, y0]

    # Scan distances outward (1) or inward (-1)
    rstep = 1 if r2 >= r1 else -1
    for distance in range(r1, r2 + rstep, rstep):

        initial = [x0, y0 + distance]
        current = initial

        # Number of tries to find a valid neighrbor
        ntrys = 0

        while True:

            # Short-circuit special case
            if distance == 0:
                yield current[0], current[1]
                break

            # Try and take a step and check if still within distance
            nextpoint = [current[i] + steps[direction][i] for i in range(2)]
            if metric(center, nextpoint) != distance:

                # Check if we tried all step directions and failed
                ntrys += 1
                if ntrys == nsteps:
                    break

                # Try the next direction
                direction = (direction + 1) % nsteps
                continue

            ntrys = 0
            yield current[0], current[1]

            # Check if we have come all the way around
            current = nextpoint
            if current == initial:
                break

        # Check if we tried all step directions and failed
        if ntrys == nsteps:
            break


def snakescan(xi, yi, xf, yf):
    """Scan pixels in a snake pattern along the x-coordinate then y-coordinate

    :param xi: Initial x-coordinate
    :type xi: int
    :param yi: Initial y-coordinate
    :type yi: int
    :param xf: Final x-coordinate
    :type xf: int
    :param yf: Final y-coordinate
    :type yf: int
    :returns: Coordinate generator
    :rtype: function
    """

    # Determine direction to move
    dx = 1 if xf >= xi else -1
    dy = 1 if yf >= yi else -1

    # Scan pixels first along x-coordinate then y-coordinate and flip
    # x-direction when the end of the line is reached
    x, xa, xb = xi, xi, xf
    for y in range(yi, yf + dy, dy):
        for x in range(xa, xb + dx, dx):
            yield x, y

        # Swap x-direction
        if x == xa or x == xb:
            dx *= -1
            xa, xb = xb, xa


def walkscan(x0, y0, xn=0.25, xp=0.25, yn=0.25, yp=0.25):
    """Scan pixels in a random walk pattern with given step probabilities. The
    random walk will continue indefinitely unless a skip transformation is used
    with the 'stop' parameter set or a clip transformation is used with the
    'abort' parameter set to True. The probabilities are normalized to one.

    :param x0: Initial x-coordinate
    :type x0: int
    :param y0: Initial y-coordinate
    :type y0: int
    :param xn: Probability of moving in the negative x direction
    :type xn: float
    :param xp: Probability of moving in the positive x direction
    :type xp: float
    :param yn: Probability of moving in the negative y direction
    :type yn: float
    :param yp: Probability of moving in the positive y direction
    :type yp: float
    """

    # Validate inputs
    if xn < 0:
        raise ValueError("Negative x probabilty must be non-negative")
    if xp < 0:
        raise ValueError("Positive x probabilty must be non-negative")
    if yn < 0:
        raise ValueError("Negative y probabilty must be non-negative")
    if yp < 0:
        raise ValueError("Positive y probabilty must be non-negative")

    # Compute normalized probability
    total = xp + xn + yp + yn
    xn /= total
    xp /= total
    yn /= total
    yp /= total

    # Compute cumulative probability
    cxn = xn
    cxp = cxn + xp
    cyn = cxp + yn

    # Initialize position
    x, y = x0, y0

    while True:

        yield x, y

        # Take random step
        probability = random.random()
        if probability <= cxn:
            x -= 1
        elif probability <= cxp:
            x += 1
        elif probability <= cyn:
            y -= 1
        else:
            y += 1

# Following imported to support floating point bitwise operations in Python 3
# https://code.activestate.com/recipes/577967-floating-point-bitwise-operations


"""
This module defines bitwise operations on floating point numbers by pretending
that they consist of an infinite sting of bits extending to the left as well as
to the right. More precisely the infinite string of bits
b = [...,b[-2],b[-1],b[0],b[1],b[2],...] represents the number
x = sum( b[i]*2**i for i in range(-inf,inf) ). Negative numbers are represented
in one's complement. The identity 0.111... == 1.0 creates an ambiquity in the
representation. To avoid it positive numbers are defined to be padded with
zeros in both directions while negative numbers are padded with ones in both
directions. This choice leads to the useful identity ~a == -a and allows
+0 == ...000.000... to be the |-identity and -0 == ...111.111... to be the
&-identity. Unfortunately the choice breaks compatibility with integer bitwise
operations involving negative numbers."""

__author__ = "Pyry Pakkanen"
__copyright__ = "Copyright 2011"
__credits__ = ["Pyry Pakkanen"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Pyry Pakkanen"
__email__ = "frostburn@suomi24.fi"
__status__ = "initial release"

(fmax, max_exp, max_10_exp, fmin, min_exp, min_10_exp, dig, mant_dig, epsilon,
 radix, rounds) = float_info


def ifrexp(x):
    """Get the mantissa and exponent of a floating point number as integers."""
    m, e = frexp(x)
    return int(m*2**mant_dig), e


def float_not(a):
    """~a"""
    return -a


def float_and(a, b):
    """a & b"""
    if a == 0.0:
        if copysign(1.0, a) == 1.0:
            return 0.0
        else:
            return b
    if b == 0.0:
        return float_and(b, a)

    if a < 0 and b < 0:
        return -float_or(-a, -b)

    if abs(a) >= abs(b):
        return float_and_(a, b)
    else:
        return float_and_(b, a)


def float_or(a, b):
    """a | b"""
    if a == 0.0:
        if copysign(1.0, a) == 1.0:
            return b
        else:
            return -0.0
    if b == 0.0:
        return float_or(b, a)

    if a < 0 and b < 0:
        return -float_and(-a, -b)

    if abs(a) >= abs(b):
        return float_or_(a, b)
    else:
        return float_or_(b, a)


def float_xor(a, b):
    """a ^ b"""
    if a == 0.0:
        if copysign(1.0, a) == 1.0:
            return b
        else:
            return -b
    if b == 0.0:
        return float_xor(b, a)

    if a < 0:
        if b < 0:
            return float_xor(-a, -b)
        else:
            return -float_xor(-a, b)
    if b < 0:
        return -float_xor(a, -b)

    if abs(a) >= abs(b):
        return float_xor_(a, b)
    else:
        return float_xor_(b, a)

# The helper functions assume that exponent(a) >= exponent(b).
# The operation lambda x: ~(-x) converts between two's complement and one's
# complement representation of a negative number. One's complement is more
# natural for floating point numbers because the zero is signed.


def float_and_(a, b):
    ma, ea = ifrexp(a)
    mb, eb = ifrexp(b)

    mb = mb >> (ea-eb)

    if ma < 0:
        return (mb & ~(-ma))*2**(ea-mant_dig)
    if mb < 0:
        return (~(-mb) & ma)*2**(ea-mant_dig)
    return (mb & ma)*2**(ea-mant_dig)


def float_or_(a, b):
    ma, ea = ifrexp(a)
    mb, eb = ifrexp(b)

    mb = mb >> (ea-eb)

    if ma < 0:
        return (-(~(mb | ~(-ma))))*2**(ea-mant_dig)
    if mb < 0:
        return (-(~(~(-mb) | ma)))*2**(ea-mant_dig)
    return (mb | ma)*2**(ea-mant_dig)


def float_xor_(a, b):
    ma, ea = ifrexp(a)
    mb, eb = ifrexp(b)

    mb = mb >> (ea-eb)

    return (mb ^ ma)*2**(ea-mant_dig)
