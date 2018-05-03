#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random

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


STAY_IN_BOUNDS = True 
CROSS_RED_BLUE = False
FOLLOW_YELLOW_GREEN = True
HEAD_SOUTH = True

MAX_OUTERCOUNT = 6
MAX_INNERCOUNT = 30
MIN_SPEED = 200
MAX_SPEED = 300
DELAY = 0.1
SLOW_TURN_SPEED = 50
FAST_TURN_SPEED = 150
TURN_DELAY = 2.5
ESCAPE_DELAY = 1.5
CRAWL_SPEED = 100
WIGGLE_FACTOR = 0.2

hit_first_color = False
following_line = False
col = "UNKNOWN"
prev_col = "UNKNOWN"

mRt = LargeMotor('outB')
mLt = LargeMotor('outC')


#colors=('unknown','black','blue','green','yellow','red','white','brown')

for outercount in range(MAX_OUTERCOUNT):
  for innercount in range(MAX_INNERCOUNT):
    sleep(DELAY)
    prev_col = col
    col = getCurrentColor()
    print(col)
    print(colorDictionary[col])

    # If looking for yellow/green strip to follow 
    if (FOLLOW_YELLOW_GREEN and not(following_line)):
      if (not(hit_first_color) and (col == "GREEN" or col == "YELLOW")):
        # Hit first of two colors 
        hit_first_color = True
        mRt.run_forever(speed_sp= -SLOW_TURN_SPEED)
        mLt.run_forever(speed_sp= -SLOW_TURN_SPEED)
      elif hit_first_color:
        if (col != "YELLOW" and col != "GREEN"):
          col = prev_col   # ignore bad color reading? 
        else:
          if ((prev_col == "YELLOW" and col == "GREEN")
          or (prev_col == "GREEN" and col == "YELLOW")):
          # Hit second of two colors 
            prev_col = col
            if ((col == "GREEN" and HEAD_SOUTH)
            or (col == "YELLOW" and not(HEAD_SOUTH))):
              sign = -1
            else:
              sign = 1
            mRt.run_forever(speed_sp=  1.5 * sign * SLOW_TURN_SPEED)
            mLt.run_forever(speed_sp= -1.5*sign * SLOW_TURN_SPEED)
            while prev_col == col:
              sleep(DELAY)
              col = getCurrentColor()
              if (col != "GREEN" and col != "YELLOW"):
                col = prev_col
              print(colorDictionary[col])
            following_line = True  # now on yellow/green and following
            hit_first_color = False

    # If on and following yellow/green strip
    if (FOLLOW_YELLOW_GREEN and following_line):
      if (col != "GREEN" and col != "YELLOW"):
        col = prev_col
      if ((col == "YELLOW" and HEAD_SOUTH) or
      (col == "GREEN" and not(HEAD_SOUTH))):
        mRt.run_forever(speed_sp= -CRAWL_SPEED*WIGGLE_FACTOR)
        mLt.run_forever(speed_sp= -CRAWL_SPEED)
      if ((col == "GREEN" and HEAD_SOUTH) or
      (col == "YELLOW" and not(HEAD_SOUTH))):
        mRt.run_forever(speed_sp= -CRAWL_SPEED)
        mLt.run_forever(speed_sp= -CRAWL_SPEED*WIGGLE_FACTOR)

    # Take evasive action when hitting boundary the shouldn't be crossed 
    while (STAY_IN_BOUNDS and (col == "WHITE" or
    (not(CROSS_RED_BLUE) and (col == "RED" or col == "BLUE")))):
      mRt.run_forever(speed_sp=  FAST_TURN_SPEED)
      mLt.run_forever(speed_sp= -FAST_TURN_SPEED)
      sleep(TURN_DELAY)
      mRt.run_forever(speed_sp= -MIN_SPEED)
      mLt.run_forever(speed_sp= -MIN_SPEED)
      sleep(ESCAPE_DELAY)
      col = getCurrentColor()
      print(colorDictionary[col])

    # Change direction once in a while (literally - outer while loop)
    if (innercount == 0 and not(following_line)):
      leftSpeed  = - random.randint(MIN_SPEED, MAX_SPEED)
      rightSpeed = - random.randint(MIN_SPEED, MAX_SPEED)
      mRt.run_forever(speed_sp= leftSpeed)
      mLt.run_forever(speed_sp= rightSpeed)
      lineup_counter = 0

# All done
sleep(DELAY)
mRt.stop(stop_action="hold")
mLt.stop(stop_action="hold")
sleep(DELAY)
