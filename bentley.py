# -*- coding: utf-8 -*-

import sys
import os

from segment import Point, Cross, Event, Segment, CROSS, START, END

seg1 = Segment(0,1,2,3)
print("segment 1 :")
print(seg1)
seg2 = Segment(10,11,20,21)
print("Segment 2 event start:")
print(seg2.start)

print("Segment 2 event end:")
print(seg2.end)


cr1 = Cross(5, 5, [seg1, seg2])
print("croisement 1 :")
print(cr1)

