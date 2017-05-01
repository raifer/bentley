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

from alternatives.bentley_cross_list import BentleyCrossList
from geo.tycat import tycat


def main(filenames=None, no_output=False):
    """
    launch test on each file.
    """
    debut_arg = 1

    if sys.argv[1:] and sys.argv[1] == "--no_output":
        no_output = True
        debut_arg += 1

    if filenames is None:
        filenames = []

    for filename in filenames + sys.argv[debut_arg:]:

        bentley = BentleyCrossList(filename)

        if not no_output:
            tycat(bentley.segments)

        segments, intersections = bentley.run()

        if not no_output:
            tycat(segments, intersections)

    return segments, intersections


if __name__ == '__main__':
    main()
