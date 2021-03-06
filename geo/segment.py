"""
segment between two points.
"""
import struct
from geo.point import Point
from geo.point import START, END, CROSS
from geo.quadrant import Quadrant
from geo.coordinates_hash import CoordinatesHash
import global_eve
from math import inf
from functools import total_ordering


class Segment:
    """
    oriented segment between two points.

    for example:

    - create a new segment between two points:

        segment = Segment([point1, point2])

    - create a new segment from coordinates:

        segment = Segment([Point([1.0, 2.0]), Point([3.0, 4.0])])

    - compute intersection point with other segment:

        intersection = segment1.intersection_with(segment2)

    """

    def __init__(self, points, adjuster):
        """
        create a segment from an array of two points.
        """

        self.adjuster = adjuster
        self.endpoints = points
        self.est_horizontal = False

        if points[0].coordinates[1] == points[1].coordinates[1]:
            self.est_horizontal = True
            if points[0].coordinates[0] < points[1].coordinates[0]:
                # On met les points dans le bon ordre.
                points.reverse()

        elif points[0].coordinates[0] == points[1].coordinates[0]:
            self.pente = 0

        else:
            self.pente = (self.end.coordinates[0] - self.start.coordinates[0]) / (
            self.end.coordinates[1] - self.start.coordinates[1])

        if points[0].coordinates[1] > points[1].coordinates[1]:
            # On met le segment dans le "bon sens"
            points[0], points[1] = points[1], points[0]

        points[0].type_eve = START
        points[1].type_eve = END

        # Les points du segment ont un pointeur vers le segment auquel ils appartiennent, cela permet de remonter au
        # segment à partir d'un événement.
        self.endpoints[0].l_segments = [self]
        self.endpoints[1].l_segments = [self]

        # L'angle avec l'horizontal est initialisé à None, il sera calculé à la volée si besoin.
        self._angle = None

        # Ces coorodonnées sont mises à jour à chaque changement d'événement.
        self._current_x = self.start.coordinates[0]
        self._current_y = self.start.coordinates[1]

        # Ce paramètre permet d'assurer que les comparaisons entre segments au niveau des intersections se font dans le
        # bon sens.
        self.before_cross = False

    def tuple(self):
        """
        Renvoie le segment sous forme de tuple.
        """
        return self.start.coordinates[0], self.start.coordinates[1], self.end.coordinates[0], self.end.coordinates[1]

    def current_x(self):
        """
        Renvoie l'abscisse du segment en fonction de l'événement actuel.
        """
        if not self.est_horizontal:
            # Dans le cas d'un segment horizontal, on met à jour le x courant dès que y change

            if global_eve.eve.coordinates[1] != self._current_y:
                self._current_y = global_eve.eve.coordinates[1]
                self._current_x = self.start.coordinates[0] + self.pente * (
                    self._current_y - self.start.coordinates[1])

        else:
            self._current_x = global_eve.eve.coordinates[0]

        # self._current_x, self._current_y = self.adjuster.hash_point(Point((self._current_x, self._current_y))).coordinates

        return self._current_x

    @property
    def start(self):
        return self.endpoints[0]

    @property
    def end(self):
        return self.endpoints[1]

    def __gt__(self, other):
        """
        Méthode de comparaison des segments, le résultat dépend de l'événement courant.
        """

        x1 = self.current_x()
        x2 = other.current_x()

        if abs(x1 - x2) > 0.0000001:
            # Les deux segments ne se croisent pas, on compare leurs abscisses courantes.
            return x1 > x2

        elif (global_eve.eve.coordinates[0] - x1) > 0.1:
            # Les deux segments comparés se croisent, mais leur intersection sera traitée dans le futur.
            return self.angle < other.angle

        elif (x1 - global_eve.eve.coordinates[0]) > 0.1:
            # Les deux segments comparés se croisent, mais leur intersection a déjà été traitée.
            return self.angle > other.angle

        elif self.before_cross or other.before_cross:
            # Les deux segments comparés se croisent et leur intersection est en train d'être traitée; leurs positions
            # dans la liste des segments vivant n'ont pas encore été échangées.
            return self.angle < other.angle

        else:
            # Les deux segments comparés se croisent et leur intersection est en train d'être traitée; leurs positions
            # dans la liste des segments vivant ont été échangées.
            return self.angle > other.angle

    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment([p.copy() for p in self.endpoints], self.adjuster)

    def length(self):
        """
        return length of segment.
        example:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def bounding_quadrant(self):
        """
        return min quadrant containing self.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.endpoints:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(
            *self.endpoints[0].coordinates,
            *self.endpoints[1].coordinates)

    def intersection_with(self, other, adjuster):
        """
        intersect two 2d segments.
        only return point if included on the two segments.
        also return a boolean set to True if the point belongs to one of the segments' endpoints.
        """
        i = self.line_intersection_with(other)

        if i is None:
            return None, None  # parallel lines

        i = adjuster.hash_point(i)

        if self.contains(i) and other.contains(i):

            # On crée un Point de type CROSS
            intersection = Point(i.coordinates, type_eve=CROSS)
            intersection.l_segments = [self, other]
            if i not in self.endpoints and i not in other.endpoints:
                return intersection, True
            else:
                return intersection, False

        else:
            return None, None

    def line_intersection_with(self, other):
        """
        return point intersecting with the two lines passing through
        the segments.
        none if lines are almost parallel.
        """
        # solve following system :
        # intersection = start of self + alpha * direction of self
        # intersection = start of other + beta * direction of other
        directions = [s.endpoints[1] - s.endpoints[0] for s in (self, other)]
        denominator = directions[0].cross_product(directions[1])
        if abs(denominator) < 0.000001:
            # almost parallel lines
            return
        start_diff = other.endpoints[0] - self.endpoints[0]
        alpha = start_diff.cross_product(directions[1]) / denominator
        return self.endpoints[0] + directions[0] * alpha

    def contains(self, possible_point):
        """
        is given point inside us ?
        be careful, determining if a point is inside a segment is a difficult problem
        (it is in fact a meaningless question in most cases).
        you might get wrong results for points extremely near endpoints.
        """
        distance = sum(possible_point.distance_to(p) for p in self.endpoints)
        return abs(distance - self.length()) < 0.000001

    @property
    def angle(self):
        """
        Calcul l'"angle" (en réalité sa tangente) du segment avec l'horizontal.
        """
        if not self._angle:
            if self.end.coordinates[1] != self.start.coordinates[1]:
                self._angle = (self.end.coordinates[0] - self.start.coordinates[0]) / float(
                    (self.end.coordinates[1] - self.start.coordinates[1]))
            elif self.end.coordinates[0] > self.start.coordinates[0]:
                self._angle = inf
            else:
                self._angle = -inf

        return self._angle

    def __str__(self):
        return "Segment([" + str(self.endpoints[0]) + ", " + \
               str(self.endpoints[1]) + "])"

    def __repr__(self):
        return "[" + repr(self.endpoints[0]) + ", " + \
               repr(self.endpoints[1]) + "])"


def load_segments(filename=None, segments_de_base=None):
    """
    loads given .bo file.
    returns a vector of segments.
    """
    coordinates_struct = struct.Struct('4d')
    segments = []
    adjuster = CoordinatesHash()

    if filename is not None:

        with open(filename, "rb") as bo_file:
            packed_segment = bo_file.read(32)
            while packed_segment:
                coordinates = coordinates_struct.unpack(packed_segment)
                raw_points = [Point(coordinates[0:2]), Point(coordinates[2:])]
                adjusted_points = [adjuster.hash_point(p) for p in raw_points]
                segments.append(Segment(adjusted_points, adjuster))
                packed_segment = bo_file.read(32)

    elif segments_de_base is not None:
        for segment in segments_de_base:
            coordinates = segment
            raw_points = [Point(coordinates[0:2]), Point(coordinates[2:])]
            adjusted_points = [adjuster.hash_point(p) for p in raw_points]
            segments.append(Segment(adjusted_points, adjuster))

    return adjuster, segments


# La ligne suivante définit automatiquement les méthodes de comparaisons (__eq__, __lt__, etc.) pour la classe Segment,
# à partir de sa méthode __gt__.
Segment = total_ordering(Segment)
