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


def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        bentley = Bentley(filename)
        print("segments :", bentley.segments)
        tycat(bentley.segments)
        segments, intersections = bentley.run()
        tycat(segments, intersections)
        print("Nombre d'intersections :", len(intersections))
        # end for

if __name__ == '__main__':
    main()
