#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import global_eve
from sortedcontainers import SortedList

from geo.segment import load_segments
from geo.point import CROSS, START, END
from geo.tycat import tycat


class BentleySortedList(object):
    def __init__(self, filename=None, segments=None):
        """Initialise les structures de l'algo"""

        # Chargement des segments et de l'ajusteur.
        if filename:
            self.adjuster, self.segments = load_segments(filename=filename)
        elif segments:
            self.adjuster, self.segments = load_segments(segments_de_base=segments)

        # Initialisation des la liste des évènement dans un tas (heap).
        self.events = SortedList()
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
        self.alive_segments = SortedList(load=1000)

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
            # print("\nNew event : %s" % eve)
            # On apelle une des trois fonction selon le type d'évènement.
            try:
                self.compute_event[eve.type_eve](eve)
            except:
                print([segment.tuple() for segment in eve.l_segments])
                raise

        return self.segments, self.cross_set

    # end def

    def traiter_croisement(self, cross, pas_contact):
        """
        Traite le croisement "cross".
        """

        if cross and cross not in self.cross_set_complet:
            # Si le croisement n'est pas présent dans la liste complète, on l'y ajoute.
            self.cross_set_complet.add(cross)

            if pas_contact:
                # Si le croisement n'est pas un croisement de type "contact", on l'ajoute à la liste définitive.
                self.cross_set.add(cross)

                if cross > global_eve.eve:
                    # Si le croisement est dans le "futur" par rapport à l'événement courant,
                    # on l'ajoute à la liste des événements.
                    heapq.heappush(self.events, cross)

    def compute_start_event(self, eve):

        # print("Compute event type START")

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
            self.traiter_croisement(cross, pas_contact)

        if i < len(self.alive_segments) - 1:
            # De même avec le voisin de droite.
            segment_droite = self.alive_segments[i + 1]
            cross, pas_contact = seg.intersection_with(segment_droite, self.adjuster)
            self.traiter_croisement(cross, pas_contact)

    # end def

    def compute_end_event(self, eve):

        # print("Compute event type END")

        seg = eve.l_segments[0]

        if seg.est_horizontal:
            seg.__current_x__ = eve.coordinates[0]

        seg.before_cross = True
        i = self.alive_segments.index(seg)
        seg.before_cross = False

        if 0 < i < len(self.alive_segments) - 1:
            # Si le segment qui se termine se trouvait entre deux segments, on cherche un croisement potentiel entre
            #  ces deux segments
            seg_gauche = self.alive_segments[i - 1]
            seg_droite = self.alive_segments[i + 1]

            cross, pas_contact = seg_gauche.intersection_with(seg_droite, self.adjuster)
            self.traiter_croisement(cross, pas_contact)

        # On retire le segment qui vient de se terminer de la liste des segments vivants
        self.alive_segments.pop(i)

    # end def

    def compute_cross_event(self, eve):

        # print("Compute event type CROSS")

        # On récupère les deux segments qui se croisent à partir de l'événement.
        seg1 = eve.l_segments[0]
        seg2 = eve.l_segments[1]

        seg1._current_y = eve.coordinates[1]
        seg2._current_y = eve.coordinates[1]
        seg1._current_x = eve.coordinates[0]
        seg2._current_x = eve.coordinates[0]

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
            self.traiter_croisement(cross, pas_contact)

        if i_droite < len(self.alive_segments) - 1:
            segment_droite_droite = self.alive_segments[i_droite + 1]
            cross, pas_contact = segment_droite.intersection_with(segment_droite_droite, self.adjuster)
            self.traiter_croisement(cross, pas_contact)
