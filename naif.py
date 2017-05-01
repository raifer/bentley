#!/usr/bin/env python3
"""
Implémente un algorithme naïf de recherche d'intersections.
"""

import sys
from itertools import combinations
from geo.tycat import tycat
from geo.segment import load_segments


def trouver_intersections(filename):

    adjuster, segments = load_segments(filename=filename)

    cross_set_complet = set()
    cross_set = set()

    for seg1, seg2 in combinations(segments,2):
            cross, pas_contact = seg1.intersection_with(seg2, adjuster)
            if cross and cross not in cross_set_complet:
                cross_set_complet.add(cross)
                if pas_contact:
                    cross_set.add(cross)

    return segments, cross_set


def main(filenames=None, no_graphic=False):
    """
    launch test on each file.
    """
    debut_arg = 1

    if sys.argv[1:] and sys.argv[1] == "--no_graphic":
        no_graphic = True
        debut_arg += 1

    if filenames is None:
        filenames = []

    for filename in filenames + sys.argv[debut_arg:]:

        segments, intersections = trouver_intersections(filename)

        if not no_graphic:
            tycat(segments)
            tycat(segments, intersections)

if __name__ == '__main__':
    main()

