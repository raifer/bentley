#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import heapq

from geo.segment import load_segments
from geo.tycat import tycat

def bentley(filename):
    """
    run bentley ottmann
    """
    adjuster, segments = load_segments(filename)
    events = init(segments)
    for eve in events :
        print(eve)
    # end for
    tycat(segments)
    #TODO: merci de completer et de decommenter les lignes suivantes
    #results = lancer bentley ottmann sur les segments et l'ajusteur
    #...
    #tycat(segments, intersections)
    #print("le nombre d'intersections (= le nombre de points differents) est", ...)
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)

def init(segments):
    """
        Init events heap struct with start and end of each segments
    """
    
    events = []
    for seg in segments :
        heapq.heappush(events, seg.endpoints[0])
        heapq.heappush(events, seg.endpoints[1])
    # end for
    return events
# end def

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        bentley(filename)
    # end for
# end def

main()
