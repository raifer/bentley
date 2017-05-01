#!/usr/bin/env python3
import sys
from time import time

import bo
import naif
FILENAMES = ["carnifex_h_0.5.bo", "flat_simple.bo", "simple_three.bo", "triangle_0.8.bo", "triangle_b_1.0.bo",
             "triangle_h_0.5.bo", "fin.bo", "random_100.bo", "simple.bo", "triangle_0.1.bo", "triangle_b_0.5.bo",
             "triangle_h_0.1.bo", "triangle_h_1.0.bo"]


def temps_moyen_bo(filename, nb_iterations):
    """
    Renvoie le temps moyen d'éxecution de l'algorithme de Bentley-Ottmann sur filename.
    """
    times = []

    for i in range(nb_iterations):
        print(i)
        t1 = time()
        bo.main([filename], no_graphic=True)
        t2 = time()
        times.append(t2 - t1)

    return sum(times) / nb_iterations


def temps_moyen_naif(filename, nb_iterations):
    """
    Renvoie le temps moyen d'éxecution de l'algorithme de Bentley-Ottmann sur filename.
    """
    times = []

    for i in range(nb_iterations):
        print(i)
        t1 = time()
        naif.main([filename], no_graphic=True)
        t2 = time()
        times.append(t2 - t1)

    return sum(times) / nb_iterations


def main():
    for filename in sys.argv[1:]:
        print(temps_moyen_bo(filename, 10))


if __name__ == '__main__':
    main()
