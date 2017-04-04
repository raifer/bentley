# -*- coding: utf-8 -*-


from math import atan, pi

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
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
# end class


		
seg = Segment(0,0,0,1)
print("angle : %.3f" %(seg.angle*1))