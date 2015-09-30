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

+----------+-----------------------------------------------------------+
|   Name   | Description                                               |
+==========+===========================================================+
|circlescan|Generates pixels in a clockwise circular pattern           |
+----------+-----------------------------------------------------------+
| .. image:: examples/circlescan.png                                   |
+----------+-----------------------------------------------------------+
|  gridscan|Generates pixels in rectangular grid pattern               |
+----------+-----------------------------------------------------------+
| .. image:: examples/gridscan.png                                     |
+----------+-----------------------------------------------------------+
|  ringscan|Generates pixels in a ring pattern (squares or diamonds)   |
+----------+-----------------------------------------------------------+
| .. image:: examples/chebyshev.png                                    |
+----------------------------------------------------------------------+
| .. image:: examples/manhattan.png                                    |
+----------+-----------------------------------------------------------+
|  snakecan|Generates pixels in a snake pattern along the x then y axis|
+----------+-----------------------------------------------------------+
| .. image:: examples/snakescan.png                                    |
+----------+-----------------------------------------------------------+
|  walkscan|Generates pixels in a random pattern using a random walk   |
+----------+-----------------------------------------------------------+
| .. image:: examples/walkscan.png                                     |
+----------+-----------------------------------------------------------+

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

Transformations such as the **rotation** can yield non-grid points.
They can be snapped to a grid point using the **snap** transformation.

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
