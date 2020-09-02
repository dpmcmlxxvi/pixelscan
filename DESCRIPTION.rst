The **pixelscan** library provides functions to scan pixels on a grid in a
variety of spatial patterns. The library consists of scan generators and
coordinate transformations. Scan generators are Python generators that return
pixel coordinates in a particular spatial pattern. Coordinate transformations
are iterators that apply spatial transformations to the coordinates created by
the scan generators. Transformation can be chained to yield very generic
transformations.
