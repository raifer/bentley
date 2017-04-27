#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import heapq
import y_cord
from sortedcontainers import SortedList

from geo.segment import load_segments
from geo.point import CROSS, START, END
from geo.tycat import tycat


class Bentley(object):
    def __init__(self, filename):
        """Initialise les structures de l'algo"""

        # Chargement des segments et de l'ajusteur.
        self.adjuster, self.segments = load_segments(filename)

        # Initialisation des la liste des évènement dans un tas (heap).
        self.events = []
        for seg in self.segments:
            # Il est plus performant d'insérer les points de début de segment avant les points de fin
            heapq.heappush(self.events, seg.endpoints[0])
            heapq.heappush(self.events, seg.endpoints[1])
        # end for

        # Switch pour les trois methodes qui gèrent les évènements.
        self.compute_event = {
            START: self.compute_start_event,
            END: self.compute_end_event,
            CROSS: self.compute_cross_event
        }  # end dict

        # Création de la liste des segments actifs triés par abscisse.
        self.alive_segments = SortedList()

        # Création du set des croisements.
        self.cross_set = set()

    def run(self):
        while True:
            try:
                eve = heapq.heappop(self.events)
            except IndexError:
                break

                # On déplace la droite d'étude.
            y_cord.y = eve.y
            print("\nNew event : %s" % eve)
            # On apelle une des trois fonction selon le type d'évènement.
            self.compute_event[eve.type_eve](eve)
            print(self.alive_segments)
            # end while

        return self.segments, self.cross_set

    # end def

    def compute_start_event(self, eve):
        print("Compute event type START")
        # Récupération du segment lié au point.
        seg = eve.l_segments[0]

        # On rend le segment vivant.
        i = self.alive_segments.bisect(seg)
        self.alive_segments.insert(i, seg)

        # On recherche les croisement avec les nouveaux voisins. On regarde si les croisements trouvés sont dans la
        # cross_set Si oui, on met à jour la liste des segments dans le croisement., ce qui mettra à jour également
        # l'évènement associé!

        if i > 0:
            # Si le segment n'est pas tout à gauche, on cherche un croisement potentiel avec son voisin de gauche.
            segment_gauche = self.alive_segments[i - 1]
            cross = seg.intersection_with(segment_gauche)

            if cross and cross not in self.cross_set:
                # Si le croisement n'est pas présent, on l'ajoute à la liste
                self.cross_set.add(cross)
                if cross > eve:
                    # Si le croisement est dans le futur, on l'ajoute aussi aux événements
                    heapq.heappush(self.events, cross)

        if i < len(self.alive_segments) - 1:
            # De même avec le voisin de droite.
            segment_droite = self.alive_segments[i + 1]
            cross = seg.intersection_with(segment_droite)
            if cross and cross not in self.cross_set:
                print(cross)
                self.cross_set.add(cross)
                if cross > eve:
                    heapq.heappush(self.events, cross)

    # end def

    def compute_end_event(self, eve):
        print("Compute event type END")
        seg = eve.l_segments[0]
        i = self.alive_segments.index(seg)

        if 0 < i < len(self.alive_segments) - 1:
            # Si le segment qui se termine se trouvait entre deux segments, on cherche un croisement potentiel entre
            # ces deux segments
            seg_gauche = self.alive_segments[i - 1]
            seg_droite = self.alive_segments[i + 1]

            cross = seg_gauche.intersection_with(seg_droite)
            if cross and cross not in self.cross_set:
                self.cross_set.add(cross)
                if cross > eve:
                    heapq.heappush(self.events, cross)

        # On retire le segment qui vient de se terminer de la liste des segments vivants
        self.alive_segments.pop(i)
    # end def

    def compute_cross_event(self, eve):

        print("Compute event type CROSS")

        # On récupère les deux segments qui se croisent à partir de l'événement.
        seg1 = eve.l_segments[0]
        seg2 = eve.l_segments[1]

        # À ce moment-ci, la liste des segments vivants n'est pas ordonnée puisque les deux segments se croisant
        # n'ont pas encore été intervertis. Cela est problématique puisque l'on ne peut pas utiliser la fonction
        # "index" avec une liste désordonnée. On utilise donc le booléen "before_cross" qui indiquent aux segments
        # que leur fonction __gt__ doit renvoyer le contraire de ce qu'elle renverrait normalement. En d'autres
        # termes, pour trouver l'indice des segments dans liste désordonnée, il faut indiquer que l'on effectue les
        # comparaisons entre segments avant l'intersection.

        seg1.before_cross = True
        seg2.before_cross = True

        i1 = self.alive_segments.index(seg1)
        i2 = self.alive_segments.index(seg2)

        seg1.before_cross = False
        seg2.before_cross = False

        if abs(i1 - i2) != 1:
            raise IOError("Les deux segments ne sont pas voisins.")

        # On inverse les positions des deux segments qui se croisent
        self.alive_segments[i1], self.alive_segments[i2] = self.alive_segments[i2], self.alive_segments[i1]

        # On cherche les potentiels croisements avec les nouveaux voisins des deux segments qui viennent de se croiser
        i_gauche = min(i1, i2)
        i_droite = max(i1, i2)

        segment_gauche = self.alive_segments[i_gauche]
        segment_droite = self.alive_segments[i_droite]

        if i_gauche > 0:
            segment_gauche_gauche = self.alive_segments[i_gauche - 1]
            cross = segment_gauche.intersection_with(segment_gauche_gauche)

            if cross and cross not in self.cross_set:
                self.cross_set.add(cross)
                if cross > eve:
                    heapq.heappush(self.events, cross)

        if i_droite < len(self.alive_segments) - 1:
            segment_droite_droite = self.alive_segments[i_droite + 1]
            cross = segment_droite.intersection_with(segment_droite_droite)

            if cross and cross not in self.cross_set:
                self.cross_set.add(cross)
                if cross > eve:
                    heapq.heappush(self.events, cross)

    # end def


# end class
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
        print(intersections)
        # end for


# end def

if __name__ == '__main__':
    main()

# tycat(segments)
# TODO: merci de completer et de decommenter les lignes suivantes
# results = lancer bentley ottmann sur les segments et l'ajusteur
# ...
# tycat(segments, intersections)
# print("le nombre d'intersections (= le nombre de points differents) est", ...)
# print("le nombre de coupes dans les segments (si un point d'intersection apparait dans
# plusieurs segments, il compte plusieurs fois) est", ...)
