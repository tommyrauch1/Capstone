#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random



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
  None : [100, 100, 100],
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
	

inBounds = True

for x in range(0,100) :
	if(inBounds == False) :
		turnRight()
	mRt.run_timed(time_sp = 1000, speed_sp = 500)
	mLt.run_timed(time_sp = 1000, speed_sp = 500)
