import pstats
import cProfile
from bentley import Bentley

def temps_moyen(filename, nb_iterations):

    for _ in range(nb_iterations):
        cProfile.run('./bo.py '+'--nographic filename', filename+'stat')
        p = pstats.Stats(filename+'_stat')


p = pstats.Stats('output_carnifex')
p.strip_dirs()
p.sort_stats('time')
p.print_stats()
