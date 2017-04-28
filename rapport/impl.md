# Implémentation
## Les segments actifs

Les segments actif et leur ordonnancement prennent  une part majeur dans la complexité de l’algorithme. Nous avons pu le confirmer lors de nos tests de performance. C’est pourquoi le choix de la structure de donné fut important. Afin de trier les segments entre eux, une méthode __gt__ a été implémenté dans la class segment.

Cette méthode sera surtout utilisé par la liste des segments actifs lors d’une recherche ou d’un ajout d’un élément.

## événements

Les événements doivent-être ordonnancé dans un ordre précis pour que l'algorithme se déroule correctement : 

* Inverse de l'ordonné de l'événement;
* abscisse de l'événement;
* type END
* type CROSS;
* type START.

Nous avons considéré que chaque point pouvait-être vue comme un événement. L'objet point a donc été modifier pour répondre à nos besoin:

* Type d'événement :
    - None : point classique, ce n'est pas un événement.
    - START : Début d'un segment.
    - END : Fin d'un segment.
    - CROSS : Croisement entre deux segments.
* Liste des segments concerné par l’événement.

Afin de comparer les événement entre eux, nous avons ajouté une fonction __gt__ (gretter than". 
Celle-ci sera principalement utilisé par le tas qui ordonnancera les événements. 
