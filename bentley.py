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
    
    # Global_y représente l'ordonné de l'évennement en cours d'étude.
    global g_y
    
    adjuster, segments = load_segments(filename)
    events = init_events(segments)
    # Création de la liste des segments actifs triés par abscisse.
    actifs_segments = []
    # Création de la liste des croisements.
    cross_list = []
    
    while True:
        try :
            eve = heapq.heappop(events)
        except IndexError :
            break
    
        g_y = eve.y
        print(eve)
    # end while
    
    print("End Bentley")
    #tycat(segments)
    #TODO: merci de completer et de decommenter les lignes suivantes
    #results = lancer bentley ottmann sur les segments et l'ajusteur
    #...
    #tycat(segments, intersections)
    #print("le nombre d'intersections (= le nombre de points differents) est", ...)
    #print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
    # plusieurs segments, il compte plusieurs fois) est", ...)

def init_events(segments):
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
