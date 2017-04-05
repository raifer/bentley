# -*- coding: utf-8 -*-

import sys
import os

from segment import Point, Cross, Event, Segment, CROSS, START, END

seg1 = Segment(0,0,0,1)
print("seg1 :")
print(seg1)
seg2 = Segment(10,11,20,21)

cr1 = Cross(5, 5, [seg1, seg2])
print("cr1 :")
print(cr1)

ev1 = Event(1,1, CROSS, cr1)
print("ev1 :")
print(ev1)
