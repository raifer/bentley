#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import heapq

from geo.segment import load_segments
from geo.point import CROSS, START, END
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
    alive_segments = []
    
    # Création de la liste des croisements.
    cross_list = []
    
    # Switch pour les trois type d'évènement
    compute_event = {
        START : compute_start_event,
        END : compute_end_event,
        CROSS : compute_cross_event
    } # end dict
    
    while True:
        try :
            eve = heapq.heappop(events)
        except IndexError :
            break
    
        g_y = eve.y
        print("Event : %s" %eve)
        compute_event[eve.type_eve](eve, alive_segments, cross_list):)
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

def compute_start_event(eve, alive_segments, cross_list):
    print("Compute event type START")
    # Récupération du segment lié au point.
    seg = eve.l_segments[0]
    
    # On rend le segment vivant.
    #######
    
    # On recherche les croisement avec les nouveaux voisins.
    #######
    # On regarde si les croisements trouvés sont dans la cross_list
    # Si oui, on met à jour la liste des segments dans le croisement., ce qui metra à jour également l'évènement associé!
    
    # Si pas présent:
    ## on l'ajoute à la cross_list
    ## Si le croisement est dans le future, on peut aussi l'ajouter à la liste des évènements. 
    
    
# end def

def compute_end_event(eve) :
    print("Compute event type END")
# end def

def compute_cross_event(eve) :
    print("Compute event type CROSS")
    print("nombre de segments : %d" %(len(eve.l_segments)))
    for seg in eve.l_segments :
        print(seg)
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
