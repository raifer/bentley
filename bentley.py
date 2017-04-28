#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import heapq
import global_eve
from sortedcontainers import SortedList

from geo.segment import load_segments
from geo.point import CROSS, START, END
from geo.tycat import tycat


class Bentley(object):
    def __init__(self, filename=None, segments=None):
        """Initialise les structures de l'algo"""

        # Chargement des segments et de l'ajusteur.
        if filename:
            self.adjuster, self.segments = load_segments(filename=filename)
        elif segments:
            self.adjuster, self.segments = load_segments(segments_de_base=segments)

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
        self.cross_set_complet = set()  # Set contenant aussi les croisements de type "contact"

    def run(self):
        while True:
            try:
                eve = heapq.heappop(self.events)
            except IndexError:
                break

            # On déplace la droite d'étude.
            global_eve.eve = eve
            print("\nNew event : %s" % eve)
            # On apelle une des trois fonction selon le type d'évènement.
            try:
                self.compute_event[eve.type_eve](eve)

                # tycat(self.segments, self.cross_set)
                # hop = input()

            except:
                raise
                # print("Unexpected error", sys.exc_info()[0])
                # tycat(list(self.alive_segments), eve.l_segments, self.cross_set, eve)
                # liste = list(self.alive_segments)
                # i0 = liste.index(eve.l_segments[0])
                # liste_autour = liste[i0-4:i0+4]
                # print("\n \nsegments autours\n", [segment.tuple() for segment in liste_autour])
                # print("\nsegments incriminés\n\n", eve.l_segments)
                # tycat(self.alive_segments)
                # tycat(self.segments, self.cross_set)

                # print(self.alive_segments)
                # end while

        return self.segments, self.cross_set

    # end def

    def traiter_croisement(self, cross, pas_contact, eve):
        """
        Traite le croisement "cross".
        """

        if cross and cross not in self.cross_set_complet:
            # Si le croisement n'est pas présent dans la liste complète, on l'y ajoute.
            self.cross_set_complet.add(cross)

            if pas_contact:
                # Si le croisement n'est pas un croisement de type "contact", on l'ajoute à la liste définitive.
                self.cross_set.add(cross)

                if cross > eve:
                    # Si le croisement est dans le "futur" par rapport à l'événement courant,
                    # on l'ajoute à la liste des événements.
                    heapq.heappush(self.events, cross)

    def compute_start_event(self, eve):

        print("Compute event type START")

        # Récupération du segment lié à l'événement.
        seg = eve.l_segments[0]

        # On rend le segment vivant.
        i = self.alive_segments.bisect(seg)
        self.alive_segments.insert(i, seg)

        # On cherche les nouveaux croisements potentiels

        if i > 0:
            # Si le segment n'est pas tout à gauche, on cherche un croisement potentiel avec son voisin de gauche.
            segment_gauche = self.alive_segments[i - 1]
            cross, pas_contact = seg.intersection_with(segment_gauche, self.adjuster)
            self.traiter_croisement(cross, pas_contact, eve)

        if i < len(self.alive_segments) - 1:
            # De même avec le voisin de droite.
            segment_droite = self.alive_segments[i + 1]
            cross, pas_contact = seg.intersection_with(segment_droite, self.adjuster)
            self.traiter_croisement(cross, pas_contact, eve)

    # end def

    def compute_end_event(self, eve):

        print("Compute event type END")

        seg = eve.l_segments[0]

        if seg.est_horizontal:
            seg.__current_x__ = eve.x

        seg.before_cross = True
        i = self.alive_segments.index(seg)
        seg.before_cross = False

        if 0 < i < len(self.alive_segments) - 1:
            # Si le segment qui se termine se trouvait entre deux segments, on cherche un croisement potentiel entre
            #  ces deux segments
            seg_gauche = self.alive_segments[i - 1]
            seg_droite = self.alive_segments[i + 1]

            cross, pas_contact = seg_gauche.intersection_with(seg_droite, self.adjuster)
            self.traiter_croisement(cross, pas_contact, eve)

        # On retire le segment qui vient de se terminer de la liste des segments vivants
        self.alive_segments.pop(i)

    # end def

    def compute_cross_event(self, eve):

        print("Compute event type CROSS")

        # On récupère les deux segments qui se croisent à partir de l'événement.
        seg1 = eve.l_segments[0]
        seg2 = eve.l_segments[1]

        if seg1.est_horizontal:
            seg1.__current_x__ = eve.x
        if seg2.est_horizontal:
            seg2.__current_x__ = eve.x

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
            cross, pas_contact = segment_gauche.intersection_with(segment_gauche_gauche, self.adjuster)
            self.traiter_croisement(cross, pas_contact, eve)

        if i_droite < len(self.alive_segments) - 1:
            segment_droite_droite = self.alive_segments[i_droite + 1]
            cross, pas_contact = segment_droite.intersection_with(segment_droite_droite, self.adjuster)
            self.traiter_croisement(cross, pas_contact, eve)


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


def debug():
    # (0.5672739207285618, 0.7182803253299785, 0.7333192810734472, 0.7770742917103786)
    bentley = Bentley(segments=[(0.5672739207285618, 0.7182803253299785, 0.7333192810734472, 0.7770742917103786),
                                (0.7074891581491014, 0.6981912444861718, 0.10673992991458858, 0.8114906491821592),
                                (0.9840143922321702, 0.6943102897392419, 0.009919246712381646, 0.7970903679299115),
                                (0.39331531337700265, 0.4954681370369596, 0.7588674049822455, 0.7513571983471277)])

    tycat(bentley.segments)
    segments, intersections = bentley.run()
    tycat(segments, intersections)
    print(intersections)


# end def

if __name__ == '__main__':
    main()
