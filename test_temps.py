#!/usr/bin/env python3

"""
Plusieurs tests temporels. Doit être exécuté dans le dossier /bentley/ pour fonctionner correctement.
"""

from time import time
from matplotlib import pyplot

import bo
import bo_cross_list
import naif

FILENAMES = ["flat_simple.bo", "simple_three.bo", "triangle_0.8.bo", "triangle_b_1.0.bo", "carnifex_h_0.5.bo",
             "triangle_h_0.5.bo", "fin.bo", "random_100.bo", "simple.bo", "triangle_0.1.bo", "triangle_b_0.5.bo",
             "triangle_h_0.1.bo", "triangle_h_1.0.bo"]

FILENAMES = ["./tests/" + filename for filename in FILENAMES]


def temps_moyen_bo(filename, nb_iterations):
    """
    Renvoie le temps moyen d'éxecution de l'algorithme de Bentley-Ottmann sur filename.
    """

    segments, intersections = [], []
    times = []

    for i in range(nb_iterations):
        t1 = time()
        segments, intersections = bo.main([filename], no_graphic=True)
        t2 = time()
        times.append(t2 - t1)

        # Si une éxecution a pris trop de temps, on arrête le test.
        if t2 - t1 > 120:
            break

    return len(segments), len(intersections), sum(times) / nb_iterations


def temps_moyen_bo_cross_list(filename, nb_iterations):
    """
    Renvoie le temps moyen d'éxecution de l'algorithme de Bentley-Ottmann sur filename.
    """

    segments, intersections = [], []
    times = []

    for i in range(nb_iterations):
        t1 = time()
        segments, intersections = bo_cross_list.main([filename], no_graphic=True)
        t2 = time()
        times.append(t2 - t1)

        # Si une éxecution a pris trop de temps, on arrête le test.
        if t2 - t1 > 120:
            break

    return len(segments), len(intersections), sum(times) / nb_iterations


def temps_moyen_naif(filename, nb_iterations):
    """
    Renvoie le temps moyen d'éxecution de l'algorithme de Bentley-Ottmann sur filename.
    """
    segments, intersections = [], []
    times = []

    for i in range(nb_iterations):
        t1 = time()
        segments, intersections = naif.main([filename], no_graphic=True)
        t2 = time()
        times.append(t2 - t1)

    return len(segments), len(intersections), sum(times) / nb_iterations


def comparer(nb_iterations, *args):
    """
    Compare les algorithmes passés en argument sur tous les tests possibles
    """
    temps_moyens = []

    for func in args:
        temps_moyens.append([])
        nbs_segments = []
        nbs_intersections = []

        for filename in FILENAMES:
            nb_segments, nb_intersections, temps_moyen = func(filename, nb_iterations)
            temps_moyens[-1].append(temps_moyen)
            nbs_segments.append(nb_segments)
            nbs_intersections.append(nb_intersections)

        pyplot.plot(nbs_segments, temps_moyens[-1], "o")

    pyplot.legend([func.__name__ for func in args])
    pyplot.xlabel("Nombres de segments")
    pyplot.ylabel("Temps d'éxecution (s)")

    pyplot.show()


def main():
    comparer(1, temps_moyen_bo, temps_moyen_naif)


if __name__ == '__main__':
    main()
