# Question

Un croisement peut-il contenir trois segment.


Algorithme de bentley ottmann

# Algo qui calcul les points d'intersection des segment

  version simple qui trouve les intersections en testant chaque segment deux à deux en n²
  
  Quand on travail en pyton on divise par 100 la performance par rapport au C.
  
 
# Algorithme de bentley ottmann
 
en svg, repère est en haut à gauche

# Définition  
## Evennement : 

Un événement peut-être :
* début et fin d'un segment
* intersection

## angle

Si besoin pour comparer l'ordre de deux segments à une ordonné donné ou ces segments sont très proche.
Le cas ou un segment commence sur un autre segment
l'angle d'un segment se mesure entre l'origine du cercle trigo et le segment 
A moins B
si angle de la diférence est négatif, A à le plus faible abscisse
 L'angle est calculé quand on charge le segment
 

 ## Ajusteur
 
  Le fichier passe dans l'ajusteur qui forme une table de hash, cela limite la précision des points pour éviter deux droites presque horizontale. 

## Etape

On récupère un fichier de segment
pour chaque segment 
on créer un segment avec ces deux points passé dans l'ajusteur
on ajoute les point dans l'ensemble evennement (il sont triées automatiquement par priorité) 

l'ensemble d'intersection est vide
ensemble des segment actif : vide

On prend l'événement de plus grande priorité
on le retire de l'ensemble des événement à traiter
trois cas possible
1. début de segment
2. fin de segment
3. croisement

1.
On retire l'événement à la liste des événement 
On ajoute le segment à la liste des segments actif
il se place tout seul entre ces deux voisins
si il a des voisin on regarde si il se croisent
Si oui on ajoute les croisement à la liste des croisement et des événement

2. 
On retire l'événement de la liste des événement
on retire le segment de la liste des segment actif
on récupère ces ancien voisins et on regarde si il se croisent
si oui, on ajoute le croisement à la liste des croisements et des événements

3.
on retire le croisement de la liste des événements
on inverse l'ordre des segment qui compose le croisement
on prend les deux segments qui borne l'ensemble des segments impactés par l'inversion
on prend leur nouveau voisin et on regarde si il se croisent 
si oui, on ajoute le croisement à la liste des croisement et à la liste des événements

# structure
## arbre des événement
Les événements sont triés par :
1. ordonné
2. inverse des abscisse 
3. fin de segment | intersection | début de segment

on prendra toujours l'événement de priorité max

## Liste des segments actif
ils sont triés par clef  lors de leur insertion
les clef sont des fonctions dépendante de y

on a besoin de connaitre lors d'une insertion, le segment inférieur et supérieur

il faut pouvoir demander voisin inférieur et voisin supérieur

## segment
### attribut
point debut
point fin
float angle = 
### methode
float get_angle(self) :
 angle = tan-1((self.fin.y - self.deb.y) / (self.fin.x - self.deb.x))
 if self.deb.x > self.fin.x :
  # On ajoute pi
  angle += pi
 # end if
 angle = ajustage(angle)
 return angle

## point
### attributs
float x
float y

## croisement
### attribut
point position
segment seg1
segment seg2

### methode
__init__(self, x, y, seg1, seg2)# bentley