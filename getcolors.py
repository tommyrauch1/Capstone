#!/usr/bin/env python3
from ev3dev.ev3 import *

cl = ColorSensor()
cl.mode='RGB-RAW'


red = cl.value(0)
green = cl.value(1)
blue = cl.value(2)
print("Red: " + str(red))
print("Green: " + str(green))
print("Blue: " + str(blue))