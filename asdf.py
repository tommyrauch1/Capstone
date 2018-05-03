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
  "RED" : [6, 0, 0],
  "WHITE" : [19, 32, 31],
  "BLUE" : [0, 0, 5],
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
	mLt.run_to_rel_pos(position_sp=1070, speed_sp = 200, stop_action = "brake")
	print("Left Motor Running")
	mRt.run_to_rel_pos(position_sp=-1070, speed_sp = 200, stop_action = "brake")
	print("Right motor running")
	mRt.wait_while('running')
	mRt.wait_while('running')
	print("finished rotating")
	sleep(1)
#TODO: rotate in opposite directions to avoid drifting around the arena
def run(col) :
	inbounds = True
	print("Starting")
	mLt.run_forever(speed_sp = -200)
	mRt.run_forever(speed_sp = -200)
	while inbounds : 
		col = getCurrentColor()
		print(col)
		if col == "WHITE" :
			mLt.stop()
			mRt.stop()
			rotate()
			print("resuming movement")
			mLt.run_forever(speed_sp = -300)
			mRt.run_forever(speed_sp = -300)
		sleep(0.1)

col = getCurrentColor()
run(col)