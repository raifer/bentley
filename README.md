# Algorithme de bentley ottmann

* Groupe 6
* Balthazar Potet et Mathieu Barbe

## Lancement de l'algorithme sur les fichiers de tests .bo

./bo.py \[--no_output] \<fichier bo>

exemple : ./bo.py tests/random_100.bo

--no_output : cette option supprime toute sortie (à utiliser pour les tests de performance)

### Sortie du programme

Par défaut, le programme affiche les segments à traiter et les intersections trouvées, ainsi que
le nombre de segments et le nombre d'intersections.

## Fichiers de l'archive

bentley.py : Contient la classe Bentley, qui implémente l'algorithme.

bo.py : Permet de lancer l'algorithme à partir des fichier segments.

global_eve.py : Script de liaison pour la variable globale eve.

rapport.md : Source du rapport du projet.

README.md : Ce fichier, documentation de base du projet.

tests/ : Contient les fichiers de segment bo.

geo/ : Scripts pythons pour le traitement des objets géométriques.

alternatives/ : Implémentations alternatives pour les tests de performance.

Pour réaliser notre projet, nous avons modifié les fichiers sources présents dans le dossier geo.
