% Rapport de projet : Algorithme de Bentley-Ottmann
% Mathieu Barbe et Balthazar Potet
% 28/04/2017

# Introduction

Dans le but de détecter les intersections contenus dans un ensemble de segments, nous avons implémenté l'algorithme de Bentley-Ottmann à partir du langage de script Python.
Celui-ci fonctionne avec presque l'ensemble des fichiers de test fournis à l'exception de random_200.bo qui nous pose quelques soucis d'imprécision.
Nous avons fait l'effort de bien structurer notre programme ainsi que de commenter notre code dans l'objectif d'optimiser notre effort et vous faciliter la tâche si vous désirez étudier notre implémentation en détail.
Nous avons fait le choix d'énumérer seulement les intersections "réelles", c'est-à-dire que nous ne prenons pas en compte les intersections où une extrémité de segment intervient. Mais vous pourrez trouver dans le code la liste de tout les contacts entre segments si nécessaire.
Dans la suite de ce rapport, nous exposons le choix des structures de données, quelques points importants de notre implémentation, une études de l'éxécution de l'algorithme pour une optimisation et nous terminerons par des testes de performance.

# Structures de données

L'algorithme nécessite de manipuller trois types de données : les segments en vie, les événements à traiter et les intersections découverttes.
Le type de ces structures de données vont fortement influer sur la complexité de l'algorithme, et doivent donc être choisies avec soin.

## Liste des intersections

Le but de l'algorithme est de découvrir les intersections entre les segments, nous devrons donc les stoquer dans une liste, celle-ci sera également utile pour savoir si un croisement à déjà été trouvé dans le passé.
L'ordre des intersections trouvées n'a pas d'importance, cependant il est nécessaire de pouvoir vérifier rapidement la présence d'un élément.
C'est pourquoi une recherche efficace est nécessaire. 
Nous avons donc choisi d'utiliser une table de hachage, implémentée en python par le type set().

* Type python : set
* Nom de la variable : cross_set

## Liste des événements

Les événements sont les étapes de l'algorithme, ils doivent être traités dans un ordre précis (selon leur position et leur type). 
De plus, de nouveaux événements sont créés en cours d'exécution et doivent être triés lors de leur insertion. Comme les événements doivent être traités dans l'ordre, nous n'avons besoin à chaque étape que de l'élément de plus grande priorité, et nous n'avons donc pas à faire de recherche sur un autre élément. La liste de priorité permet de faire chacune de ces opérations de manière efficace : insertion triée en O(log(n)) et suppression de l'élément de plus grande priorité en O(log(n)).

* Type python : heapq
* Nom de la variable : events

## Stockage des segments en vie
Les segments en vie sont les segments qui peuvent potentiellement se croiser entre eux. Il est important de connaître leur ordre (pour un y donné) afin de connaître les voisins d'un segment donné. De plus, des segments peuvent être ajoutés, retirés ou intervertis à chaque étape. Nous avons donc besoin de trouver rapidement la position d'un segment dans la structure de donnée. Un AVL fait ces opérations de manière efficace : insertion, recherche et suppression en O(log(n)).

* Type python : SortedList
* Nom de la variable : alive_segments

# Implémentation

Pour implémenter l'algorithme, nous avons créé une class Bentley qui prend en paramètres un nom de fichier "bo" ou directement une liste de segments. 
Ce dernier paramètre nous aura permis d'isoler des erreurs et de les résoudres plus facilement. Voici les grandes étapes de notre implémentation :

1. Chargement des segments dans une liste à partir de la méthode 'load_segments' 
2. Création d'un couple d'événements, 'START' et 'END' pour chaque segment. Ceux-ci seront ajoutés au tas des événement 'events' qui s'occupera de les trier.
3. Boucle principale sur les événements 'START', 'CROSS' et 'END'
    * Pour chaque événement, on met à jour une variable globale 'eve' qui contient l'événement en cours. Cette technique nous sera indispensable pour ordonner les segments actifs entre eux.
    * On traite l'événement dans une des trois méthodes compute_*_event.
    * START
        - On récupère le segment concerné par cette événement,
        - On l'ajoute à la liste des segments actifs qui soccupera de le placer à la bonne place à l'aide de la méthode __gt__ de la class segment,
        - On recherche les croisements avec ces voisins.
        - Si nouveau croisement, On l'ajoute à la liste des croisement et on créer un nouvelle événement.
    * CROSS
        - On récupère les segments incriminés par le croisement,
        - Dans un premier temps, on se place avant le croisement, pour cela, on tag les segment 'befor_cross', Cette information sera utilisé lors de leurs comparaisons d'angle.
        - On recherche la position des segments dans la liste des actifs,
        - On supprime le tag,
        - On inverse les segments,
        - on recherche les nouveaux croisements avec les voisins,
        - si on trouve un nouveau croisement, on l'ajoute à la liste et on créer un nouvelle événement.
    * END
        - on récupère le segment concerné par l'événement,
        - on le supprime de la liste des actif,
        - on recherche un croisement entre ces deux anciens voisins,
        - si l'on découvre une nouvelle intersection, on l'ajoute à la liste et on créer un nouvelle événement.
         
         
         Voici quelques détails concernant les class utilisées dans notre implémentation .
         
         ## Liste des segments actifs

Les segments actif et leur ordonnancement prennent  une part majeur dans la complexité de l’algorithme. Nous avons pu le confirmer lors de nos tests de performance. C’est pourquoi le choix de la structure de donné fut important. Afin de trier les segments entre eux, une méthode __gt__ a été implémenté dans la class segment.
Cette méthode sera en grande partie utilisée par la liste des segments actifs lors d’une recherche d'indice ou d'un ajout, nous avons donc porté un soin particulié à son écriture.

## Événements

Nous avons considéré que chaque point pouvait être vu comme un événement. L'objet point a donc été modifié pour répondre à nos besoin, voici nos ajouts :

* Type d'événement :
    - None : point classique, ce n'est pas un événement,
    - START : Début d'un segment,
    - END : Fin d'un segment,
    - CROSS : Croisement entre deux segments;
* liste des segments concerné par l’événement. (Dans un premier temps nous avions pris en compte que plus de deux segments pouvaient se croiser en un seul point, mais se ne fut pas le cas);
* méthode __gt__.

Les événements doivent-être ordonnés dans un ordre rigoureu pour que l'algorithme se déroule correctement.
Afin de réaliser cette comparaison, nous avons ajouté une fonction \__gt__ (gretter than" dans la class point.
Celle-ci sera principalement utilisé par le tas qui ordonnancera les événements lors de leur insertion.
Voici l'ordre que nous avons implémenté :

* Inverse de l'ordonnée de l'événement;
* abscisse de l'événement;
* type END;
* type CROSS;
* type START.


# Performances temporelles
Nous avons utilisé l'option cProfile pour analyser les performances temporelles de notre code afin d'identifier les fonctions consommant le plus de temps au total (notamment la méthode \__gt__ de la clase Segment) pour les optimiser. Les temps moyens sont mesurés à l'aide de time(). Tous les tests sont effectués avec l'option --no_graphic du script bo.py afin que l'affichage ne fausse pas les mesures.
