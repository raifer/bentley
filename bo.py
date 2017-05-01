#!/usr/bin/env python3
"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""
import sys
from geo.tycat import tycat
from bentley import Bentley


def main(filenames=None, no_output=False):
    """
    launch test on each file.
    """
    debut_arg = 1

    if "--no_output" in sys.argv[1:]:
        no_output = True
        debut_arg += 1

    if filenames is None:
        filenames = []

    for filename in filenames + sys.argv[debut_arg:]:

        bentley = Bentley(filename)

        if not no_output:
            tycat(bentley.segments)

        segments, intersections = bentley.run()
        
        if not no_output:
            tycat(segments, intersections)
            print("Nombre de segments :", len(segments))
            print("Nombre d'intersections :", len(intersections))

    return segments, intersections

if __name__ == '__main__':
    main()
