from ev3dev.ev3 import *
from time import sleep
import random

#TODO: Test grabby sensor and get ball color values, calibrate other colors

#line sensor
c1 = ColorSensor('in2')

#Claw sensor
c2 = ColorSensor('in3')

c1.mode='RGB-RAW'
c2.mode='RGB-RAW'

mRt = LargeMotor('outA')
mLt = LargeMotor('outC')

colorDictionary = {
  "RED" : [54, 15, 11],
  "RED_ALT" : [71, 17, 13],
  "WHITE" : [135, 186, 131],
  "BLUE" : [10, 22, 41],
  "GRAY" : [21, 29, 24],
  "YELLOW" : [82, 78, 20],
  "YELLOW_ALT" : [121, 90, 25],
  "GREEN" : [22, 64, 22],
  "BALL1" : [1, 1, 1, ],
  "BALL2" : [2, 2, 2],
  "BALL3" : [3, 3, 3],
  None : [0, 0, 0],
  }

#Returns the key (name of the color) of the color immediately below the color sensor 
def getCurrentColor(sensorNum) :
	#following line context
	if sensorNum = 2 :
		 arr = [c2.value(0), c2.value(1), c2.value(2)]
		#  if arr[0] < 18 :
		#  	return "BLUE"
		#  elif arr[0] < 33 :
		#  	return "GRAY"
		#  elif arr[0] < 90 :
		#  	return "RED"
		#  elif arr[0] > 100 :
		#  	return "WHITE"
		 # else :
		  for key, val in colorDictionary.items() : 
		  	if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :
		    return key

	#Ball detection context
	elif sensorNum = 1 :
		arr = [c1.value(0), c1.value(1), c1.value(2)]
		for key, val in colorDictionary.items() : 
		  	if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :
		    return key
	else :
		print("invalid number")
		return "GRAY"

#helper function
def inThree(a, b) :
  if(abs(a - b) <= 7) :
    return True
  return False

def closeClaw(speed, rotSpeed):
        mD=LargeMotor('outD')
        print(c2.value(0))
        if c2.value(0) > 100:
                mD.run_timed(time_sp=250, speed_sp=-250, stop_action = 'hold')
                mD.wait_while('running')
        else:
                print("tennis ball not found")
        time.sleep(4)
        print(c2.value(0))
        #print(c2.value(1))
        #print(c2.value(2))
        if not verifyBall:
            openClaw()

        else :
        	findGreen(speed, rotSpeed)

def openClaw():
        mD=LargeMotor('outD')
        mD.run_timed(time_sp=350,speed_sp=250)
        mD.wait_while('running')
        search()

#returns random number of degrees to rotate
def getRotation() :
	n = random.randint(1, 180)
	degrees = degreesToEngineDegrees(n)
	return degrees

#calculates how many degrees the engines must rotate for the robot to rotate n degrees
def degreesToEngineDegrees(n) :
	degrees = n * engineDegreesPerRobotDegrees
	return degrees

def rotate(turnSpeed, dist) :
	mRt.stop()
	mLt.stop()
	mRt.run_to_rel_pos(position_sp = dist, speed_sp = turnSpeed, stop_action='brake')
	mLt.run_to_rel_pos(position_sp = (dist * -1), speed_sp = turnSpeed, stop_action = 'brake')

def verifyBall() :
	col = getCurrentColor(2)
	if col == "BALL3" or col == "BALL2" or col == "BALL1" :
		return True
	else :
		return false

#only used in search function
def whenRed() :
	mRt.run_timed(time_sp = 2000, speed_sp = -300)
	mLt.run_timed(time_sp = 2000, speed_sp = -400)
	mRt.wait_while('running')
	mLt.wait_while('running')

#used in retreat function
def whenYellow(turnRadius, turnSpeed) :
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	mRt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

#used in retreat function
def whenGray(turnRadius, turnSpeed) :
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	mRt.run_to_rel_pos(position_sp = -turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp = turnRadius, speed_sp = turnSpeed, stop_action = "brake")
	sleep(1)

#Search for the ball
def search(speed, rotSpeed) :
	print("searching")
	mRt.run_forever(speed_sp = speed)
	mLt.run_forever(speed_sp = speed)
	while getCurrentColor(2) != "BALL3" and getCurrentColor(2) != "BALL2" and getCurrentColor(2) != "BALL1" :
		col = getCurrentColor(1)
		print(col)
		if col == "BLUE" or col == "WHITE" :
			numDegrees = getRotation()
			rotate(rotSpeed, numDegrees)
		elif col == "RED"
			whenRed()
		mRt.run_forever(speed_sp = speed)
		mLt.run_forever(speed_sp = speed)
		sleep(0.1)
	closeClaw()

#find the green line to retreat
def findGreen(speed, rotSpeed) :
	print("finding green")
	mRt.stop()
	mLt.stop()
	while getCurrentColor(1) != "GREEN" :
		col = getCurrentColor(1)
		mRt.run_forever(speed_sp = speed	)
		mLt.run_forever(speed_sp = speed)
		print(col)
		if col == "BLUE" or col == "WHITE" :
			numDegrees = getRotation()
			rotate(rotSpeed, numDegrees)
		elif col == "GREEN" :
			mRt.stop()
			mLt.stop()
			retreat(speed, rotSpeed)
	retreat(speed, rotSpeed)

def retreat(speed, rotSpeed) :
	print("Retreating")
	while inbounds:
		mLt.run_forever(speed_sp = -350)
		mRt.run_forever(speed_sp = -350)
		col = getCurrentColor()
		print(col)

		if col == "WHITE" :
			mLt.stop()
			mRt.stop()
			degrees = degreesToEngineDegrees(180)
			rotate(rotSpeed, degrees)

		elif col == "YELLOW":
			whenYellow(turnRadius, rotSpeed)

		elif (col == "RED" or col=="RED_ALT") :
			mRt.run_timed(time_sp = 3000, speed_sp = 300)
			mLt.run_timed(time_sp = 3000, speed_sp = 300)

		elif col == "GRAY" :
			whenGray(turnRadius, rotSpeed)

		sleep(0.1)

def run(speed, rotSpeed) :
	numRed = 0
	numBlue = 0
	mRt.run_forever(speed_sp = speed)
	mLt.run_forever(speed_sp = speed)
	onRed = False
	onBlue = False
	while numRed < 2 and numBlue < 2 :
		col = getCurrentColor(1)
		print(col)
		if (col == "RED" or col == "RED_ALT") and not onRed:
			numRed++
			onRed = True
		elif col == "BLUE" and not onBlue :
			numBlue++
			onBlue = True
		elif col == "GRAY" :
			onBlue = False
			onRed = False
		sleep(0.1)
	search(speed, rotSpeed)

driveSpeed = 350
rotationSpeed = 200
run(driveSpeed, rotationSpeed) 