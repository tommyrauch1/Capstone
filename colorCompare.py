#!/usr/bin/env python3
from ev3dev.ev3 import *

def inThree(a, b) :
	if(abs(a - b) <= 3) :
		return True
	return False

global WHITE #59 78 63
global RED #38 8 3
global BLUE #2 8 16
#red blue white gray yellow green
RED = [13, 2, 0]
WHITE = [23, 37, 35]
BLUE = [0, 3, 7]
GRAY = [0, 6, 3]
YELLOW = [16, 17, 0]
GREEN = [0, 15, 1]

cl = ColorSensor()
cl.mode='RGB-RAW'
arr = [cl.value(0), cl.value(1), cl.value(2)]

colArr = [RED, WHITE, BLUE, GRAY, YELLOW, GREEN]
asdf = False
for val in colArr : 
	if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :
		asdf = True
		for x in val:
			print(str(x))
if asdf == False :
	for n in arr :
		print("!!!" + str(n))