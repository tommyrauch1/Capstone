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
  "RED" : [34, 7, 7],
  "WHITE" : [56, 76, 68],
  "BLUE" : [3, 10, 20],
  "GRAY" : [9, 14, 11],
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

def whenBlue(turnRadius, turnSpeed) :
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed)
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed)
	sleep(3)

def whenGray(turnRadius, turnSpeed) :
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed)
	mLt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed)
	sleep(3)

def whenRed(turnRadius, turnSpeed) : 
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed)
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed)
	sleep(3)


#TODO: elongate flippy prongs
#TODO: rotate in opposite directions to avoid drifting around the arena
#TODO: follow line rather than turn. This is somewhat low of a priority
#Start with blue on the right and gray on the left, dirFlag is 0
#Move faster, and reduce sleep times
def run(col) :
	turnSpeedSlow = 80
	turnSpeedFast = 160
	turnRadius = 130
	inbounds = True
	dirFlag = 0
	print("Starting")
	while inbounds : #and touch is not touched?
		mLt.run_forever(speed_sp = -200)
		mRt.run_forever(speed_sp = -200)
		col = getCurrentColor()
		print(col)
		if col == "WHITE" :
			mLt.stop()
			mRt.stop()
			rotate()
			print("resuming movement")
			mLt.run_forever(speed_sp = -200)
			mRt.run_forever(speed_sp = -200)
			turnSpeedFast *= -1
			turnSpeedSlow *= -1
			if dirFlag == 0 :
				dirFlag = 1
			else :
				dirFlag = 0

		elif col == "BLUE" and dirFlag == 0 :
			whenBlue(turnRadius, turnSpeedFast)

		elif col == "RED" and dirFlag == 1 :
			whenRed(turnRadius, turnSpeedFast)

		elif col == "GRAY" :
			if dirFlag == 0 :
				whenGray(turnRadius, turnSpeedFast)
			else :
				whenGray(turnRadius, -turnSpeedFast)

		sleep(0.05)



col = getCurrentColor()
run(col)