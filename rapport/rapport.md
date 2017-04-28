% Rapport de projet : Algorithme de Bentley-Ottmann
% Mathieu Barbe et Balthazar Potet
% 28/04/2017


# Structures de données
L'algorithme nécessite de stocker trois types de données : les segments en vie, les événements à traiter et les intersections trouvées.
Les structures de données utilisées pour stocker ces données influencent fortement les performances de l'algorithme, et doivent donc être choisies avec soin.

## Stockage des intersections
L'ordre des intersections trouvées n'a pas d'importance, cependant il faut pouvoir détecter rapidement la présence d'une intersection, c'est pourquoi une recherche efficace
est nécessaire. Nous avons donc choisi d'utiliser une table de hachage, implémentée en python par le type set().

* Type python : set
* Nom de la variable : cross_set

## Stockage des événements
Les événements sont les étapes de l'algorithme, ils doivent être traités dans un ordre précis (selon leur position et leur type). De plus, de nouveaux événements sont créés
en cours d'exécution et doivent être triés lors de leur insertion. Comme les événements doivent être traités dans l'ordre, nous n'avons besoin à chaque étape que de
l'élément de plus grande priorité, et nous n'avons donc pas à faire de recherche sur un autre élément. La liste de priorité permet de faire chacune de ces opérations de manière
efficace : insertion triée en O(log(n)) et suppression de l'élément de plus grande priorité en O(log(n)).

* Type python : heapq
* Nom de la variable : events

## Stockage des segments en vie
Les segments en vie sont les segments qui peuvent potentiellement se croiser entre eux. Il est important de connaître leur ordre (pour un y donné) afin de connaître les voisins d'un segment donné. De plus, des segments peuvent être ajoutés, retirés ou intervertis à chaque étape. Nous avons donc besoin de trouver rapidement la position d'un segment dans la
structure de donnée. Un AVL fait ces opérations de manière efficace : insertion, recherche et suppression en O(log(n)).

* Type python : SortedList
* Nom de la variable : alive_segments

# Performances temporelles
Nous avons utilisé l'option cProfile pour analyser les performances temporelles de notre code (dans le module test_temps.py). Tous les tests sont effectués avec l'option --no_graphic
du script bo.py.

* Fichier : carnifex_h_0.5.bo
