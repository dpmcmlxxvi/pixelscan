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
Usage
***************

The typical calling syntax is

.. code-block:: python

   for x, y in transformation(generator(...), ...):
      foo(x,y)

For example, the following scans pixels in a clockwise circular pattern
from the origin up to a radius of 1

.. code-block:: python

   for x, y in snap(circlescan(0, 0, 0, 1)):
      print x, y

and will generate the following points 

.. code-block:: python

   (0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)

To skip every other pixel a skip transformation can be applied

.. code-block:: python

   for x, y in skip(snap(circlescan(0, 0, 0, 1), step=2)):
      print x, y

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
| .. image:: examples/circlescan.png |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0, y0, r1, r2 = 0, 0, 0, 2                            |
|                                    |    for x, y in snap(circlescan(x0, y0, r1, r2)):          |
|                                    |        print x, y                                         |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0 = Circle x center                                   |
|                                    |    y0 = Circle y center                                   |
|                                    |    r1 = Initial radius                                    |
|                                    |    r2 = Final radius                                      |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    ( 0, 0) ( 0, 1) ( 1, 1) ( 1, 0) ( 1,-1) ( 0,-1)        |
|                                    |    (-1,-1) (-1, 0) (-1, 1) ( 0, 2) ( 1, 2) ( 2, 1)        |
|                                    |    ( 2, 0) ( 2,-1) ( 1,-2) ( 0,-2) (-1,-2) (-2,-1)        |
|                                    |    (-2, 0) (-2, 1) (-1, 2)                                |
+------------------------------------+-----------------------------------------------------------+
|  gridscan                          |Generates pixels in rectangular grid pattern               |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/gridscan.png   |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0, y0, x1, y1 = 0, 0, 2, 2                            |
|                                    |    for x, y in gridscan(x0, y0, x1, y1):                  |
|                                    |        print x, y                                         |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0 = Initial x coordinate                              |
|                                    |    y0 = Initial y coordinate                              |
|                                    |    x1 = Final x coordinate                                |
|                                    |    y1 = Final y coordinate                                |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    (0,0) (1,0) (2,0) (0,1) (1,1) (2,1) (0,2) (1,2) (2,2)  |
+------------------------------------+-----------------------------------------------------------+
|  ringscan - chebyshev              |Generates pixels in a ring pattern (squares)               |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/chebyshev.png  |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0, y0, r1, r2 = 0, 0, 0, 2                            |
|                                    |    for x, y in ringscan(x0, y0, r1, r2, metric=chebyshev):|
|                                    |        print x, y                                         |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0 = Circle x center                                   |
|                                    |    y0 = Circle y center                                   |
|                                    |    r1 = Initial radius                                    |
|                                    |    r2 = Final radius                                      |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    ( 0, 0) ( 0, 1) ( 1, 1) ( 1, 0) ( 1,-1) ( 0,-1)        |
|                                    |    (-1,-1) (-1, 0) (-1, 1) ( 0, 2) ( 1, 2) ( 2, 2)        |
|                                    |    ( 2, 1) ( 2, 0) ( 2,-1) ( 2,-2) ( 1,-2) ( 0,-2)        |
|                                    |    (-1,-2) (-2,-2) (-2,-1) (-2, 0) (-2, 1) (-2,2) (-1,2)  |
+------------------------------------+-----------------------------------------------------------+
|  ringscan - manhattan              |Generates pixels in a ring pattern (diamonds)              |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/manhattan.png  |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0, y0, r1, r2 = 0, 0, 0, 2                            |
|                                    |    for x, y in ringscan(x0, y0, r1, r2, metric=manhattan):|
|                                    |        print x, y                                         |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0 = Circle x center                                   |
|                                    |    y0 = Circle y center                                   |
|                                    |    r1 = Initial radius                                    |
|                                    |    r2 = Final radius                                      |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    ( 0, 0) ( 0, 1) ( 1, 0) ( 0,-1) (-1, 0) ( 0, 2)        |
|                                    |    ( 1, 1) ( 2, 0) ( 1,-1) ( 0,-2) (-1,-1) (-2, 0) (-1, 1)|
+------------------------------------+-----------------------------------------------------------+
|  snakecan                          |Generates pixels in a snake pattern along the x then y axis|
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/snakescan.png  |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0, y0, x1, y1 = 0, 0, 2, 2                            |
|                                    |    for x, y in snakescan(x0, y0, x1, y1):                 |
|                                    |        print x, y                                         |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0 = Initial x coordinate                              |
|                                    |    y0 = Initial y coordinate                              |
|                                    |    x1 = Final x coordinate                                |
|                                    |    y1 = Final y coordinate                                |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    ( 0, 0) ( 1, 0) ( 2, 0) ( 2, 1) ( 1, 1) ( 0, 1)        |
|                                    |    ( 0, 2) ( 1, 2) ( 2, 2)                                |
+------------------------------------+-----------------------------------------------------------+
|  walkscan                          |Generates pixels in a random pattern using a random walk   |
+------------------------------------+-----------------------------------------------------------+
| .. image:: examples/walkscan.png   |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    random.seed(0)                                         |
|                                    |    x0, y0, stop = 0, 0, 8                                 |
|                                    |    for x, y in skip(walkscan(x0, y0), stop=stop):         |
|                                    |        print x, y                                         |
|                                    |                                                           |
|                                    |where                                                      |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    x0   = Initial x coordinate                            |
|                                    |    y0   = Initial y coordinate                            |
|                                    |    stop = Index to sto iteration (0-based)                |
|                                    |                                                           |
|                                    |produces the following points:                             |
|                                    |                                                           |
|                                    |  .. code-block:: python                                   |
|                                    |                                                           |
|                                    |    ( 0, 0) ( 0, 1) ( 0, 2) ( 1, 2) ( 2, 2) ( 2, 1)        |
|                                    |    ( 3, 1) ( 3, 2) ( 4, 2)                                |
+------------------------------------+-----------------------------------------------------------+

**************************
Coordinate Transformations
**************************

The following are the currently available transformations

+-----------+-----------------------------------------------------------+
|    Name   | Description                                               |
+===========+===========================================================+
|       clip|Clips the coordinates at the given boundary                |
+-----------+-----------------------------------------------------------+
| reflection|Reflects the coordinates along the x and/or y axis         |
+-----------+-----------------------------------------------------------+
|  reservoir|Randomly samples the pixels using reservoir sampling       |
+-----------+-----------------------------------------------------------+
|   rotation|Rotates the coordinates about the origin counter-clockwise |
+-----------+-----------------------------------------------------------+
|     sample|Randomly samples the pixels with a given probability       |
+-----------+-----------------------------------------------------------+
|      scale|Scales the coordinates with a given scale factors          |
+-----------+-----------------------------------------------------------+
|       skip|Skips the pixels with the given step size                  |
+-----------+-----------------------------------------------------------+
|       snap|Snap the x and y coordinates to a grid point               |
+-----------+-----------------------------------------------------------+
|       swap|Swap the x and y coordinates                               |
+-----------+-----------------------------------------------------------+
|translation|Translates the coordinates by the given offsets            |
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
