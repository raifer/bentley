% Rapport de projet : Algorithme de Bentley-Ottmann
% Mathieu Barbe et Balthazar Potet
% 28/04/2017

# Introduction

Dans le but de détecter les intersections contenus dans un ensemble de segments, nous avons implémenté l'algorithme de Bentley-Ottmann à partir du langage de script Python.
Celui-ci fonctionne avec presque l'ensemble des fichiers de test fournis à l'exception de random_200.bo qui nous pose quelques soucis d'imprécision.
Nous avons fait le choix d'énumérer seulement les intersections "réelles", c'est-à-dire que nous ne prenons pas en compte les intersections où une extrémité de segment intervient. Mais vous pourrez trouver dans le code la liste de tout les contacts entre segments si nécessaire.
Dans ce rapport, nous exposons quelques points importants de notre implémentation, le choix des structures de données, une études de l'éxécution de l'algorithme pour une optimisation et nous terminerons par des testes de performance.

# Implémentation

## Les segments actifs

Les segments actif et leur ordonnancement prennent  une part majeur dans la complexité de l’algorithme. Nous avons pu le confirmer lors de nos tests de performance. C’est pourquoi le choix de la structure de donné fut important. Afin de trier les segments entre eux, une méthode __gt__ a été implémenté dans la class segment.

Cette méthode sera surtout utilisé par la liste des segments actifs lors d’une recherche ou d’un ajout d’un élément.

## Événements

Les événements doivent-être ordonnés dans un ordre précis pour que l'algorithme se déroule correctement :

* Inverse de l'ordonnée de l'événement;
* abscisse de l'événement;
* type END;
* type CROSS;
* type START.

Nous avons considéré que chaque point pouvait être vu comme un événement. L'objet point a donc été modifié pour répondre à nos besoin:

* Type d'événement :
    - None : point classique, ce n'est pas un événement.
    - START : Début d'un segment.
    - END : Fin d'un segment.
    - CROSS : Croisement entre deux segments.
* Liste des segments concerné par l’événement.

Afin de comparer les événement entre eux, nous avons ajouté une fonction \__gt__ (gretter than".
Celle-ci sera principalement utilisé par le tas qui ordonnancera les événements.


# Structures de données
L'algorithme nécessite de stocker trois types de données : les segments en vie, les événements à traiter et les intersections trouvées. Les structures de données utilisées pour stocker ces données influencent fortement les performances de l'algorithme, et doivent donc être choisies avec soin.

## Stockage des intersections
L'ordre des intersections trouvées n'a pas d'importance, cependant il faut pouvoir détecter rapidement la présence d'une intersection, c'est pourquoi une recherche efficace est nécessaire. Nous avons donc choisi d'utiliser une table de hachage, implémentée en python par le type set().

* Type python : set
* Nom de la variable : cross_set

## Stockage des événements
Les événements sont les étapes de l'algorithme, ils doivent être traités dans un ordre précis (selon leur position et leur type). De plus, de nouveaux événements sont créés en cours d'exécution et doivent être triés lors de leur insertion. Comme les événements doivent être traités dans l'ordre, nous n'avons besoin à chaque étape que de l'élément de plus grande priorité, et nous n'avons donc pas à faire de recherche sur un autre élément. La liste de priorité permet de faire chacune de ces opérations de manière efficace : insertion triée en O(log(n)) et suppression de l'élément de plus grande priorité en O(log(n)).

* Type python : heapq
* Nom de la variable : events

## Stockage des segments en vie
Les segments en vie sont les segments qui peuvent potentiellement se croiser entre eux. Il est important de connaître leur ordre (pour un y donné) afin de connaître les voisins d'un segment donné. De plus, des segments peuvent être ajoutés, retirés ou intervertis à chaque étape. Nous avons donc besoin de trouver rapidement la position d'un segment dans la structure de donnée. Un AVL fait ces opérations de manière efficace : insertion, recherche et suppression en O(log(n)).

* Type python : SortedList
* Nom de la variable : alive_segments

# Performances temporelles
Nous avons utilisé l'option cProfile pour analyser les performances temporelles de notre code afin d'identifier les fonctions consommant le plus de temps au total (notamment la méthode \__gt__ de la clase Segment) pour les optimiser. Les temps moyens sont mesurés à l'aide de time(). Tous les tests sont effectués avec l'option --no_graphic du script bo.py afin que l'affichage ne fausse pas les mesures.
