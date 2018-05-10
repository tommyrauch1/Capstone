#!/usr/bin/env python3
from ev3dev.ev3 import *
import threading
import math
from time import sleep


c1 = ColorSensor('in2')
c1.mode='RGB-RAW'
c2 = ColorSensor('in3')
c2.mode='RGB-RAW'

l1 = str(c1.value(0))
l2 = str(c1.value(1))
l3 = str(c1.value(2))

b1 = str(c2.value(0))
b2 = str(c2.value(1))
b3 = str(c2.value(2))

print("Line:	Ball:")
print(l1 + "	  " + b1)
print(l2 + "	  " + b2)
print(l3 + "	  " + b3)
