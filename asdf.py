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
mFlip = LargeMotor('outA')

#initialize touch sensor

cl = ColorSensor()
cl.mode='RGB-RAW'

ts = TouchSensor()

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

#numbers need to be calibrated to individual robots, rotates the robot 180 degrees
def rotate() :
	print("rotating")
	mLt.run_to_rel_pos(position_sp=1060, speed_sp = 200, stop_action = "brake")
	print("Left Motor Running")
	mRt.run_to_rel_pos(position_sp=-1060, speed_sp = 200, stop_action = "brake")
	print("Right motor running")
	print("finished rotating")
	sleep(6)


def whenBlue(turnRadius, turnSpeed) :
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

def whenGray(turnRadius, turnSpeed) :
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

def whenRed(turnRadius, turnSpeed) : 
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

def flip() :
	mRt.stop()
	mLt.stop()
	mFlip.run_to_rel_pos(position_sp = 100, speed_sp = 700 stop_action = "hold")
	mRt.run_timed(time_sp = 7000, speed_sp = -1000)
	mLt.run_timed(time_sp = 7000, speed_sp = -1000)
	#TODO reverse back to playing field
	sleep(7)
	mRt.run_timed(time_sp = 7000, speed_sp = 1000)
	mLt.run_timed(time_sp = 7000, speed_sp = 1000)
	run()

#TODO: elongate flippy prongs
#Start with blue on the right and gray on the left, dirFlag is 0
#Move faster, and reduce sleep times
def run(col) :
	turnSpeedSlow = 80
	turnSpeedFast = 160
	turnRadius = 130
	inbounds = True
	hasTouched = False
	dirFlag = 0
	print("Starting")
	while inbounds and not ts.value():
		mLt.run_forever(speed_sp = -500)
		mRt.run_forever(speed_sp = -500)
		col = getCurrentColor()
		print(col)
		if col == "WHITE" :
			mLt.stop()
			mRt.stop()
			rotate()
			print("resuming movement")
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

		sleep(0.02)
	flip()	



col = getCurrentColor()
run(col)