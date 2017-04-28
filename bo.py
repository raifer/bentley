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
    debut_arg = 1
    no_graphic = False

    if sys.argv[1:] and sys.argv[1] == "--no_graphic":
        no_graphic = True
        debut_arg += 1

    for filename in sys.argv[debut_arg:]:

        bentley = Bentley(filename)

        if not no_graphic:
            tycat(bentley.segments)

        segments, intersections = bentley.run()
        if not no_graphic:
            tycat(segments, intersections)

if __name__ == '__main__':
    main()
