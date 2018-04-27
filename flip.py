#!/usr/bin/env python3
from ev3dev.ev3 import *

global WHITE #59 78 63
global RED #38 8 3
global BLUE #2 8 16
#red blue white gray yellow green
RED = [13, 2, 0]
WHITE = [23, 37, 35]
BLUE = [0, 3, 7]
GRAY = [0, 6, 3]
YELLOW = [16, 17, 0]
GREEN = [0, 12, 1]


cl = ColorSensor()
cl.mode='RGB-RAW'

leftMotor = LargeMotor('outC')
rightMotor = LargeMotor('outB')

def run() :
	print("Back to run")
	if cl.value(0) <45 and cl.value(0) > 30:
		ifBlue()
	elif cl.value(0) >50 and cl.value(0) < 65:
		ifWhite()
	else:
		ifRed()

def printValues():
	red = cl.value(0)
	green = cl.value(1)
	blue = cl.value(2)
	print("Red: " + str(red))
	print("Green: " + str(green))
	print("Blue: " + str(blue))

def ifRed():
	print("ifRed")
	printValues()
	leftMotor.run_timed(time_sp = 500, speed_sp = -400)
	rightMotor.run_timed(time_sp = 500, speed_sp = -400)
	#put if statement here to see if it goes off the track
	leftMotor.wait_while('running')
	rightMotor.wait_while('running')
	run()

def ifBlue():
	print("ifBlue")
	printValues()
	rightMotor.run_to_rel_pos(position_sp=120, speed_sp = -400, stop_action = "brake")
	rightMotor.wait_while('running')
	run()

def ifWhite():	
	print("ifWhite")
	printValues()
	leftMotor.run_to_rel_pos(position_sp=120, speed_sp = -400, stop_action = "brake")
	leftMotor.wait_while('running')
	run()

run()





