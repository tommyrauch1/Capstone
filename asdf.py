#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random


#chmod 777 *
#stay in bounds done
#see ball 
#grab ball


mRt = LargeMotor('outB')
mLt = LargeMotor('outC')

cl = ColorSensor()
cl.mode='RGB-RAW'

colorDictionary = {
  "RED" : [15, 3, 1],
  "WHITE" : [19, 32, 31],
  "BLUE" : [0, 3, 10],
  "GRAY" : [0, 0, 0],
  "YELLOW" : [16, 17, 0],
  "GREEN" : [0, 15, 1],
  None : [0, 0, 0],
  }

#Returns the key (name of the color) of the color immediately below the color sensor 
def getCurrentColor() :
  arr = [cl.value(0), cl.value(1), cl.value(2)]
  asdf = False
  for key, val in colorDictionary.items() : 
    if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :
      return key

#helper function
def inThree(a, b) :
  if(abs(a - b) <= 3) :
    return True
  return False

def turnLeft() :
	mRt.stop()
	mLt.stop()
	mLt.run_to_rel_pos(position_sp=900, speed_sp = 200, stop_action = "brake")
	sleep(1000)

def turnRight() :
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp=900, speed_sp = 200, stop_action = "brake")
	sleep(1000)

#numbers need to be calibrated to individual robots, rotates the robot 180 degrees
def rotate() :
	print("rotating")
	mLt.run_to_rel_pos(position_sp=1060, speed_sp = 200, stop_action = "brake")
	print("Left Motor Running")
	mRt.run_to_rel_pos(position_sp=-1060, speed_sp = 200, stop_action = "brake")
	print("Right motor running")
	print("finished rotating")
	sleep(7)


#TODO: elongate flippy prongs
#TODO: rotate in opposite directions to avoid drifting around the arena
#TODO: follow line rather than turn. This is somewhat low of a priority
def run(col) :
	turnSpeedSlow = 80
	turnSpeedFast = 160
	turnRadius = 300
	inbounds = True
	print("Starting")
	mLt.run_forever(speed_sp = -200)
	mRt.run_forever(speed_sp = -200)
	while inbounds : #and touch is not touched?
		col = getCurrentColor()
		print(col)
		if col == "WHITE" :
			mLt.stop()
			mRt.stop()
			rotate()
			print("resuming movement")
			mLt.run_forever(speed_sp = -200)
			mRt.run_forever(speed_sp = -200)
		elif col == "BLUE" :
			mRt.stop()
			mLt.stop()
			mRt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeedFast)
			mLt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeedFast)
		elif col == "GRAY" or col == None :
			mRt.stop()
			mLt.stop()
			mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeedFast)
			mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeedFast)

		sleep(0.05)

col = getCurrentColor()
run(col)