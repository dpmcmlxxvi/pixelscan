=========
pixelscan
=========

.. image:: https://travis-ci.org/dpmcmlxxvi/pixelscan.svg?branch=master
    :target: https://travis-ci.org/dpmcmlxxvi/pixelscan
    :alt: Code Status

.. image:: https://coveralls.io/repos/dpmcmlxxvi/pixelscan/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/dpmcmlxxvi/pixelscan?branch=master
    :alt: Code Coverage

.. image:: https://badge.fury.io/py/pixelscan.svg
    :target: https://pypi.python.org/pypi/pixelscan
    :alt: Code Package

The **pixelscan** library provides functions to scan pixels on a grid in a
variety of spatial patterns. The library consists of scan generators and
coordinate transformations. Scan generators are Python generators that return
pixel coordinates in a particular spatial pattern. Coordinate transformations
are iterators that apply spatial transformations to the coordinates created by
the scan generators. Transformation can be chained to yield very generic
transformations.

***************
Documentation
***************

See the library API documentation `here <http://dpmcmlxxvi.github.io/pixelscan>`_.

***************
Usage
***************

The typical calling syntax is

.. code-block:: python

   for x, y in transformation(generator(...), ...):
      foo(x,y)

For example, the following scans pixels in a clockwise circular pattern
from the origin up to a radius of one

.. code-block:: python

   for x, y in snap(circlescan(0, 0, 0, 1)):
      print(x, y)

and will generate the following points 

.. code-block:: python

   (0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)

To skip every other pixel a skip transformation can be applied

.. code-block:: python

   for x, y in snap(skip(circlescan(0, 0, 0, 1), step=2)):
      print(x, y)

which will generate the following points

.. code-block:: python

   (0,0), (1,1), (1,-1), (-1,-1), (-1,1)

***************
Scan Generators
***************

The following are the currently available generators

+------------------------------------+-----------------------------------------------------------+
|   Name                             | Description                                               |
+====================================+===========================================================+
|circlescan                          |Generates pixels in a clockwise circular pattern           |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/circlescan.png |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   x0, y0, r1, r2 = 0, 0, 0, 2                             |
|                                    |   for x, y in snap(circlescan(x0, y0, r1, r2)):           |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   x0 = Circle x center                                    |
|                                    |   y0 = Circle y center                                    |
|                                    |   r1 = Initial radius                                     |
|                                    |   r2 = Final radius                                       |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   ( 0, 0) ( 0, 1) ( 1, 1) ( 1, 0) ( 1,-1) ( 0,-1)         |
|                                    |   (-1,-1) (-1, 0) (-1, 1) ( 0, 2) ( 1, 2) ( 2, 1)         |
|                                    |   ( 2, 0) ( 2,-1) ( 1,-2) ( 0,-2) (-1,-2) (-2,-1)         |
|                                    |   (-2, 0) (-2, 1) (-1, 2)                                 |
+------------------------------------+-----------------------------------------------------------+
|gridscan                            |Generates pixels in rectangular grid pattern               |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/gridscan.png   |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   xi, yi, xf, yf = 0, 0, 2, 2                             |
|                                    |   for x, y in gridscan(xi, yi, xf, yf, stepx=1, stepy=1): |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   xi    = Initial x-coordinate                            |
|                                    |   yi    = Initial y-coordinate                            |
|                                    |   xf    = Final x-coordinate                              |
|                                    |   yf    = Final y-coordinate                              |
|                                    |   stepx = Step size in x-coordinate                       |
|                                    |   stepy = Step size in y-coordinate                       |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   (0,0) (1,0) (2,0) (0,1) (1,1) (2,1) (0,2) (1,2) (2,2)   |
+------------------------------------+-----------------------------------------------------------+
|hilbertscan                         |Generates pixels in a Hilbert curve pattern                |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/hilbertscan.png|.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   size, distance = 4, 16                                  |
|                                    |   for x, y in hilbertscan(size, distance):                |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   size     = Size of enclosing square                     |
|                                    |   distance = Distance along curve                         |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   (0,0), (0,1), (1,1), (1,0), (2,0), (3,0), (3,1), (2,1)  |
|                                    |   (2,2), (3,2), (3,3), (2,3), (1,3), (1,2), (0,2), (0,3)  |
+------------------------------------+-----------------------------------------------------------+
|ringscan - chebyshev                |Generates pixels in a ring pattern (squares)               |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/chebyshev.png  |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   x0, y0, r1, r2 = 0, 0, 0, 2                             |
|                                    |   for x, y in ringscan(x0, y0, r1, r2, metric=chebyshev): |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   x0     = Circle x center                                |
|                                    |   y0     = Circle y center                                |
|                                    |   r1     = Initial radius                                 |
|                                    |   r2     = Final radius                                   |
|                                    |   r2     = Final radius                                   |
|                                    |   metric = Distance metric                                |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   ( 0, 0) ( 0, 1) ( 1, 1) ( 1, 0) ( 1,-1) ( 0,-1)         |
|                                    |   (-1,-1) (-1, 0) (-1, 1) ( 0, 2) ( 1, 2) ( 2, 2)         |
|                                    |   ( 2, 1) ( 2, 0) ( 2,-1) ( 2,-2) ( 1,-2) ( 0,-2)         |
|                                    |   (-1,-2) (-2,-2) (-2,-1) (-2, 0) (-2, 1) (-2,2) (-1,2)   |
+------------------------------------+-----------------------------------------------------------+
|ringscan - manhattan                |Generates pixels in a ring pattern (diamonds)              |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/manhattan.png  |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   x0, y0, r1, r2 = 0, 0, 0, 2                             |
|                                    |   for x, y in ringscan(x0, y0, r1, r2, metric=manhattan): |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   x0 = Circle x center                                    |
|                                    |   y0 = Circle y center                                    |
|                                    |   r1 = Initial radius                                     |
|                                    |   r2 = Final radius                                       |
|                                    |   metric = Distance metric                                |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   ( 0, 0) ( 0, 1) ( 1, 0) ( 0,-1) (-1, 0) ( 0, 2)         |
|                                    |   ( 1, 1) ( 2, 0) ( 1,-1) ( 0,-2) (-1,-1) (-2, 0) (-1, 1) |
+------------------------------------+-----------------------------------------------------------+
|snakescan                           |Generates pixels in a snake pattern along the x then y axis|
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/snakescan.png  |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   xi, yi, xf, yf = 0, 0, 2, 2                             |
|                                    |   for x, y in snakescan(xi, yi, xf, yf):                  |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   xi = Initial x-coordinate                               |
|                                    |   yi = Initial y-coordinate                               |
|                                    |   xf = Final x-coordinate                                 |
|                                    |   yf = Final y-coordinate                                 |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   ( 0, 0) ( 1, 0) ( 2, 0) ( 2, 1) ( 1, 1) ( 0, 1)         |
|                                    |   ( 0, 2) ( 1, 2) ( 2, 2)                                 |
+------------------------------------+-----------------------------------------------------------+
|walkscan                            |Generates pixels in a random pattern using a random walk   |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/walkscan.png   |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   random.seed(0)                                          |
|                                    |   x0, y0, = 0, 0                                          |
|                                    |   for x, y in skip(walkscan(x0, y0, xn=0.25, xp=0.25,     |
|                                    |                             yn=0.25, yp=0.25), stop=8):   |
|                                    |       print x, y                                          |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |                                                           |
|                                    |.. code-block:: rest                                       |
|                                    |                                                           |
|                                    |   x0 = Initial x-coordinate                               |
|                                    |   y0 = Initial y-coordinate                               |
|                                    |   xn = Probability of moving in the negative x direction  |
|                                    |   xp = Probability of moving in the positive x direction  |
|                                    |   yn = Probability of moving in the negative y direction  |
|                                    |   yp = Probability of moving in the positive y direction  |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |.. code-block:: python                                     |
|                                    |                                                           |
|                                    |   ( 0, 0) ( 0, 1) ( 0, 2) ( 1, 2) ( 2, 2) ( 2, 1)         |
|                                    |   ( 3, 1) ( 3, 2) ( 4, 2)                                 |
+------------------------------------+-----------------------------------------------------------+

**************************
Coordinate Transformations
**************************

The following are the currently available transformations

+-----------+-----------------------------------------------------------+
|    Name   | Description                                               |
+===========+===========================================================+
|clip       |Clips the coordinates at the given boundary                |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   clip(scan,                                                          |
|        minx      = int,                                               |
|        maxx      = int,                                               |
|        miny      = int,                                               |
|        maxy      = int,                                               |
|        predicate = function,                                          |
|        abort     = bool)                                              |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan      = Pixel scan generator                                    |
|   minx      = Minimum x-coordinate (default = -sys.maxint)            |
|   maxx      = Maximum x-coordinate (default =  sys.maxint)            |
|   miny      = Minimum y-coordinate (default = -sys.maxint)            |
|   maxy      = Maximum y-coordinate (default =  sys.maxint)            |
|   predicate = Optional function that takes 2 arguments (x and y)      |
|               and returns true if coordinate should be kept           |
|               otherwise false (default = None)                        |
|   abort     = Abort iteration if boundary is crossed                  |
+-----------+-----------------------------------------------------------+
|reflection |Reflects the coordinates along the x and/or y axis         |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   reflection(scan, rx = bool, ry = bool)                              |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan = Pixel scan generator                                         |
|   rx   = True if x-coordinate should be reflected (default=False)     |
|   ry   = True if y-coordinate should be reflected (default=False)     |
+-----------+-----------------------------------------------------------+
|reservoir  |Randomly samples the pixels using reservoir sampling       |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   reservoir(scan, npoints = int)                                      |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan    = Pixel scan generator                                      |
|   npoints = Sample size                                               |
+-----------+-----------------------------------------------------------+
|rotation   |Rotates the coordinates about the origin counter-clockwise |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   rotation(scan, angle = float)                                       |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan  = Pixel scan generator                                        |
|   angle = Counter-clockwise angle in degrees (default=0)              |
+-----------+-----------------------------------------------------------+
|sample     |Randomly samples the pixels with a given probability       |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   sample(scan, probability = float)                                   |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan        = Pixel scan generator                                  |
|   probability = Sampling probability in interval [0,1] (default=1)    |
+-----------+-----------------------------------------------------------+
|scale      |Scales the coordinates with a given scale factors          |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   scale(scan, sx = float, sy = float)                                 |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan = Pixel scan generator                                         |
|   sx   = x-coordinate scale factor (default=1)                        |
|   sy   = y-coordinate scale factor (default=1)                        |
+-----------+-----------------------------------------------------------+
|skip       |Skips the pixels with the given step size                  |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   skip(scan, start = int, stop = int, step = int)                     |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan  = Pixel scan generator                                        |
|   start = Iteration starting 0-based index (default = 0)              |
|   stop  = Iteration stopping 0-based index (default = sys.maxint)     |
|   step  = Iteration step size (default = 1)                           |
+-----------+-----------------------------------------------------------+
|snap       |Snap the x and y coordinates to the nearest grid point     |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   snap(scan)                                                          |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan = Pixel scan generator                                         |
+-----------+-----------------------------------------------------------+
|swap       |Swap the x and y coordinates                               |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   swap(scan)                                                          |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan = Pixel scan generator                                         |
+-----------+-----------------------------------------------------------+
|translation|Translates the coordinates by the given offsets            |
+-----------+-----------------------------------------------------------+
|Syntax:                                                                |
|                                                                       |
|.. code-block:: python                                                 |
|                                                                       |
|   translation(scan, tx = float, ty = float)                           |
|                                                                       |
|where                                                                  |
|                                                                       |
|.. code-block:: rest                                                   |
|                                                                       |
|   scan = Pixel scan generator                                         |
|   tx   = x-coordinate translation offset (default = 0)                |
|   ty   = y-coordinate translation offset (default = 0)                |
+-----------+-----------------------------------------------------------+


***************
Warnings
***************

Scan Generators such as **circlescan** and Coordinate Transformations such as
**rotation** can yield non-grid points. They can be snapped to a grid point
using the **snap** transformation.

***************
Changelog
***************

- v0.3.2
    - Fix deployment token

- v0.3.1
    - Fix pypi deployment twine bug

- v0.3.0
    - Switch coverage to coveralls
    - Clean up code health issues
    - Fix landscape syntax
    - Add health and version badges
    - Fix pylint options syntax
    - Replace link table with badge links

- v0.2.0
    - Add clip transformation
    - Add random walk generator
    - Replace random generators with reservoir transformation
    - Add continous integration and testing
    - Add automated deployment 

- v0.1.0
   - Initial release
