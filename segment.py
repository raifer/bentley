# -*- coding: utf-8 -*-


from math import atan, pi

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	# end def
	
	def __repr__(self):
		return "x= %.4f, y= %.4f" %(self.x, self.y)
	# end def
# end class

class Croisement(Point):
	"""Point avec les segments associé"""
	def __init__(self, x, y):
		self.segments = []
		return Point.__init__(self, x, y)
	# end def
# end class

class Evenement(Point):
	def __gt__(self, eve2):
		"""Trié par X puis par inverse Y"""
		# comparaison par abcisse si ordonné identique
		if self.y == eve2.y:
			if self.x == eve2.x :
				# Les deux événements sont au même point
				# Il faut gérer ici l'ordre si il sont de type diférent
				return False # temporaire
			# end if
			return self.x < eve2.x
		# end if
		else:
			return self.y > eve2.y
		# end else
	# end def
# end class

class Segment(object):
	def __init__(self, start_x, start_y, end_x, end_y):
		self.start = Point(start_x, start_y)
		self.end = Point(end_x, end_y)
		
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
		return "Start : %s\nEnd : %s\nAngle : %.4f radians" %(self.start, self.end, self.angle)
		# end def 
# end class


		
seg = Segment(0,0,0,1)
print(seg)

eve1 = Evenement(1,1)
eve2 = Evenement(2, 2)
print(eve1)
print(eve2)
print(eve1 > eve2)