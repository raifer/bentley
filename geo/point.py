"""
points (any dimension).
"""
from math import sqrt
from geo.quadrant import Quadrant

CROSS = 0
START = 1
END = 2

class Point:
    """
    a point is defined as a vector of any given dimension.

    for example:

    - create a point at x=2, y=5:

    my_point = Point([2, 5])

    - find distance between two points:

    distance = point1.distance_to(point2)
    """
    def __init__(self, coordinates, type_eve=None):
        """
        build new point using an array of coordinates.
        """
        self.coordinates = coordinates
        self.type_eve = type_eve

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def copy(self):
        """
        return copy of given point.
        """
        return Point(list(self.coordinates))

    def distance_to(self, other):
        """
        euclidean distance between two points.
        """
        total = 0
        for c_1, c_2 in zip(self.coordinates, other.coordinates):
            diff = c_1 - c_2
            total += diff * diff
        return sqrt(total)

    def bounding_quadrant(self):
        """
        return min quadrant containing point.
        this method is defined on any displayable object.
        """
        return Quadrant(self.coordinates, self.coordinates)

    def svg_content(self):
        """
        svg display for tycat.
        """
        return '<use xlink:href="#c" x="{}" y="{}"/>\n'.format(*self.coordinates)

    def cross_product(self, other):
        """
        cross product between 2 2d vectors.
        """
        x_1, y_1 = self.coordinates
        x_2, y_2 = other.coordinates
        return -y_1*x_2 + x_1*y_2

    def __eq__(self, other):
        """
        strict equality operator
        """
        return self.coordinates == other.coordinates

    def __gt__(self, eve2):
        """ Trié par (du plus petit au plus grand :
        y
        si y identique, inverse de x
        si x et y identique, on a :
        croisement < debut < fin
        Les plus petit événement sont exploités en premier"""

        if self.y > eve2.y: return True
        if self.y < eve2.y : return False
        # Si on est encore là, l'ordonné est identique.
        if self.x < eve2.x : return True
        if self.x > eve2.x : return False
        # Si on est encore là, abcisse et ordonné identique
        if self.type_eve > eve2.type_eve : return True
        # Si on est encore là, les deux points on exactement la même priorité.
        return False
        # end def

    def __hash__(self):
        return hash(tuple(self.coordinates))

    def __add__(self, other):
        """
        addition operator. (useful for translations)
        """
        return Point([i + j for i, j in zip(self.coordinates, other.coordinates)])

    def __sub__(self, other):
        """
        substraction operator. (useful for translations)
        """
        return Point([i - j for i, j in zip(self.coordinates, other.coordinates)])

    def __mul__(self, factor):
        """
        multiplication by scalar operator. (useful for scaling)
        """
        return Point([c*factor for c in self.coordinates])

    def __truediv__(self, factor):
        """
        division by scalar operator. (useful for scaling)
        """
        return Point([c/factor for c in self.coordinates])

    def __str__(self):
        """
        print code generating the point.
        """
        return "Point([" + ', '.join(str(c) for c in self.coordinates) + "])"

    def __repr__(self):
        return "(" + ', '.join(str(c) for c in self.coordinates) + ")"
