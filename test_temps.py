#!/usr/bin/env python3
import sys
import bo
from time import time


def temps_moyen(filename, nb_iterations):
    """
    Renvoie le temps moyen d'éxecution de l'algorithme sur filename.
    """
    times = []

    for i in range(nb_iterations):
        print(i)
        t1 = time()
        bo.main([filename], True)
        t2 = time()
        times.append(t2 - t1)

    return sum(times)/nb_iterations


def main():
    for filename in sys.argv[1:]:
        print(temps_moyen(filename, 10))


if __name__ == '__main__':
    main()
