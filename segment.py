# -*- coding: utf-8 -*-


from math import atan, pi

# Constantes
# Type d'événement
# Triés par ordre de priorité, 0 à traiter en premier.
CROSS = 0
START = 1
END = 2

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	# end def

	def __repr__(self):
		return "x= %.4f, y= %.4f" %(self.x, self.y)
	# end def
# end class

class Event(Point):
	def __init__(self, x, y, type):
		if type not in [CROSS, START, END]:
			raise IOError("Event must be associated with a type : CROSS, START or END")
		# end if
		self.type = type
		return Point.__init__(self, x, y)
	# end def

	def __repr__(self):
		type_name = self.fetch_type_name()
		return "Event type " + type_name + ". Position : " + Point.__repr__(self)
	# end def

	def fetch_type_name(self):
		if self.type == CROSS : return "CROSS"
		if self.type == START : return "START"
		if self.type == END : return "END"
		return "Error type"
	# end def

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
		if self.type > eve2.type : return True
		# Si on est encore là, les deux points on exactement la même priorité.
		return False
	# end def
# end class

class Cross(Event):
	"""Point avec les segments associé"""
	def __init__(self, x, y, list_seg=[]):
		if len(list_seg) < 2:
			raise IOError("A cross must be contain at least 2 segments")
		# end if
		self.segs = list_seg
		return Event.__init__(self, x, y, CROSS)
	# end def

	def __repr__(self):
		txt = "Cross position : %.4f %.4f\n%d segments associated :" %(self.x, self.y, len(self.segs))
		for seg in self.segs:
			txt += "\n" + Segment.__repr__(seg)
		return txt
	# end def
# end class

class Segment(object):
	def __init__(self, start_x, start_y, end_x, end_y):
		self.start = Event(start_x, start_y, START)
		self.end = Event(end_x, end_y, END)

		# Calcul de l'angle
		# Si segment verticale, on évite la div par 0.
		if self.start.x == self.end.x :
			self.angle = pi/2
		else :
			self.angle = atan((self.end.y - self.start.y) / float((self.end.x - self.start.x)))
			if self.start.x > self.end.x :
				# On ajoute pi
				self.angle += pi
		# end if
		#self.angle = ajustage(self.angle)
	# end def

	def __repr__(self):
		return "Start : %.4f %.4f\nEnd : %.4f %.4f\nAngle : %.4f radians" %(self.start.x, self.start.y, self.end.x, self.end.y, self.angle)
		# end def
# end class
