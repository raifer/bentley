#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import heapq

from geo.segment import load_segments
from geo.point import CROSS, START, END
from geo.tycat import tycat

class Bentley(object):

    def __init__(self, filename):
        """Initialise les structures de l'algo"""
        
        self.y = None
        
        # Chargement des segments et de l'ajusteur.
        self.adjuster, self.segments = load_segments(filename)
        
        # Initialisation des la liste des évènement dans un tas (heap).
        self.events = []
        for seg in self.segments :
            heapq.heappush(self.events, seg.endpoints[0])
            heapq.heappush(self.events, seg.endpoints[1])
        # end for
        
        # Switch pour les trois methodes qui gèrent les évènements.
        self.compute_event = {
            START : self.compute_start_event,
            END : self.compute_end_event,
            CROSS : self.compute_cross_event
        } # end dict
        
        # Création de la liste des segments actifs triés par abscisse.
        self.alive_segments = []
        
        # Création de la liste des croisements.
        self.cross_list = []
        
    def run(self):
        while True:
            try :
                eve = heapq.heappop(self.events)
            except IndexError :
                break
        
        # On déplace la droite d'étude.
            self.y = eve.y
            
            print("\nNew event : %s" %eve)
            # On apelle une des trois fonction celon le type d'évènement.
            self.compute_event[eve.type_eve](eve)
        # end while
    # end def

    def compute_start_event(self, eve):
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

    def compute_end_event(self, eve) :
        print("Compute event type END")
    # end def

    def compute_cross_event(self, eve) :
        print("Compute event type CROSS with %d segments" %(len(eve.l_segments)))
        for seg in eve.l_segments :
            print(seg)
        # end for
    # end def
# end class
def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        bentley = Bentley(filename)
        bentley.run()
    # end for
# end def

main()
#tycat(segments)
#TODO: merci de completer et de decommenter les lignes suivantes
#results = lancer bentley ottmann sur les segments et l'ajusteur
#...
#tycat(segments, intersections)
#print("le nombre d'intersections (= le nombre de points differents) est", ...)
#print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
# plusieurs segments, il compte plusieurs fois) est", ...)
