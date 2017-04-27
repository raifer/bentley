"""
segment between two points.
"""
import struct
from geo.point import Point
from geo.point import START, END, CROSS
from geo.quadrant import Quadrant
from geo.coordinates_hash import CoordinatesHash
import y_cord
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

    def __init__(self, points):
        """
        create a segment from an array of two points.
        """
        print(points)

        self.endpoints = points
        self.est_horizontal = False

        if points[0].y == points[1].y:

            self.est_horizontal = True
            if points[0].x < points[1].x:
                # On met les points dans le bon ordre.
                points.reverse()
                # end if
        else:
            self.pente = (self.end.x - self.start.x) / (self.end.y - self.start.y)

        if points[0].y > points[1].y:
            # On met le segment dans le "bon sens"
            points[0], points[1] = points[1], points[0]
        # end if
        points[0].type_eve = START
        points[1].type_eve = END

        # Ajout du pointeur sur le segment dans les points.
        # Permet de remonter au segment à partir de l'eve.
        self.endpoints[0].l_segments = [self]
        self.endpoints[1].l_segments = [self]
        # On crée un angle None, il sera calculé à la volée si besoin.
        self.__angle__ = None
        self.__current_x__ = self.start.x
        self.__current_y__ = y_cord.y
        self.before_cross = False

    # end def

    def current_x(self, other):

        if not self.est_horizontal:
            # Dans le cas d'un segment horizontal, on met à jour le x courant dès que y change

            if y_cord.y != self.__current_y__:
                self.__current_y__ = y_cord.y
                self.__current_x__ = self.start.x + self.pente * (self.__current_y__ - self.start.y)

        else:
            #  Dans le cas d'un segment horizontal, on met à jour le x courant à chaque intersection
            if self.before_cross and other.before_cross:
                if not other.est_horizontal:
                    self.__current_x__ = other.current_x(self)

        return self.__current_x__

    @property
    def start(self):
        return self.endpoints[0]

    @property
    def end(self):
        return self.endpoints[1]

    def __gt__(self, other):

        x1 = self.current_x(other)
        x2 = other.current_x(self)

        if abs(x1 - x2) > 0.000001:
            return x1 > x2

        elif self.before_cross and other.before_cross:
            return self.angle < other.angle

        else:
            # Si les deux abscisses sont suffisamment proches, on est au niveau d'une intersection. On compare donc les
            # angles.
            return self.angle > other.angle

    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment([p.copy() for p in self.endpoints])

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

    def intersection_with(self, other):
        """
        intersect two 2d segments.
        only return point if included on the two segments.
        """
        i = self.line_intersection_with(other)
        if i is None:
            return  # parallel lines

        if self.contains(i) and other.contains(i):
            # On crée un Point de type CROSS
            intersection = Point(i.coordinates, type_eve=CROSS)
            intersection.l_segments = [self, other]
            return intersection

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
        if not self.__angle__:
            if self.end.y != self.start.y:
                self.__angle__ = (self.end.x - self.start.x) / float((self.end.y - self.start.y))
            elif self.end.x > self.start.x:
                self.__angle__ = inf
            else:
                self.__angle__ = -inf
        return self.__angle__

    def __str__(self):
        return "Segment([" + str(self.endpoints[0]) + ", " + \
               str(self.endpoints[1]) + "])"

    def __repr__(self):
        return "[" + repr(self.endpoints[0]) + ", " + \
               repr(self.endpoints[1]) + "])"


def load_segments(filename):
    """
    loads given .bo file.
    returns a vector of segments.
    """
    coordinates_struct = struct.Struct('4d')
    segments = []
    adjuster = CoordinatesHash()

    with open(filename, "rb") as bo_file:
        packed_segment = bo_file.read(32)
        while packed_segment:
            coordinates = coordinates_struct.unpack(packed_segment)
            raw_points = [Point(coordinates[0:2]), Point(coordinates[2:])]
            adjusted_points = [adjuster.hash_point(p) for p in raw_points]
            segments.append(Segment(adjusted_points))
            packed_segment = bo_file.read(32)

    return adjuster, segments


# La ligne suivante définit automatiquement les méthodes de comparaisons (__eq__, __lt__, etc.) pour la classe Segment
Segment = total_ordering(Segment)
