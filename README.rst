=========
pixelscan
=========

.. image:: https://travis-ci.org/dpmcmlxxvi/pixelscan.svg?branch=master
    :target: https://travis-ci.org/dpmcmlxxvi/pixelscan

.. image:: http://codecov.io/github/dpmcmlxxvi/pixelscan/coverage.svg?branch=master
    :target: http://codecov.io/github/dpmcmlxxvi/pixelscan?branch=master

The **pixelscan** library provides functions to scan pixels on a grid in a
variety of spatial patterns. The library consists of scan generators and
coordinate transformations. Scan generators are Python generators that return
pixel coordinates in a particular spatial pattern. Coordinate transformations
are iterators that apply spatial transformations to the coordinates created by
the scan generators. Transformation can be chained to yield very generic
transformations.

+----------+------------------------------------------------+
| Source   | https://github.com/dpmcmlxxvi/pixelscan        |
+----------+------------------------------------------------+
| Package  | https://pypi.python.org/pypi/pixelscan         |
+----------+------------------------------------------------+
| Testing  | https://travis-ci.org/dpmcmlxxvi/pixelscan     |
+----------+------------------------------------------------+
| Coverage | https://codecov.io/github/dpmcmlxxvi/pixelscan |
+----------+------------------------------------------------+
| License  | http://opensource.org/licenses/MIT             |
+----------+------------------------------------------------+

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

   for x, y in circlescan(0, 0, 0, 1):
      print x, y

and will generate the following points 

.. code-block:: python

   (0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)

To skip every other pixel a skip transformation can be applied

.. code-block:: python

   for x, y in skip(circlescan(0, 0, 0, 1), step=2):
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
|  gridscan|Generates pixels in rectangular grid pattern               |
+----------+-----------------------------------------------------------+
|  ringscan|Generates pixels in a ring pattern (squares or diamonds)   |
+----------+-----------------------------------------------------------+
|  snakecan|Generates pixels in a snake pattern along the x then y axis|
+----------+-----------------------------------------------------------+
|  walkscan|Generates pixels in a random pattern using a random walk   |
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

- v0.1.0
   Initial release
