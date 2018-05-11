from ev3dev.ev3 import *
from time import sleep
import random

#TODO: Test grabby sensor and get ball color values, calibrate other colors

#line sensor
c1 = ColorSensor('in1')

c1.mode='RGB-RAW'

mRt = LargeMotor('outA')
mLt = LargeMotor('outC')

colorDictionary = {
  "RED" : [146, 23, 32],
  #"RED_ALT" : [71, 17, 13],
  "WHITE" : [228, 208, 302],
  "BLUE" : [19, 33, 108],
  "GRAY" : [41, 35, 55],
  "YELLOW" : [166, 110, 45],
  "YELLOW_ALT" : [121, 90, 25],
  "GREEN" : [30, 67, 39],
  None : [0, 0, 0],
  }

#Returns the key (name of the color) of the color immediately below the color sensor 
def getCurrentColor(sensorNum) :
	#following line context
	if sensorNum == 2 :
		arr = [c2.value(0), c2.value(1), c2.value(2)]
		for key, val in colorDictionary.items() : 
			if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :
				return key

	#Ball detection context
	elif sensorNum == 1 :
		arr = [c1.value(0), c1.value(1), c1.value(2)]
		if arr[0] >= 150 and arr[1] >= 150 and arr[2] >= 150 :
			return "WHITE"
		elif arr[0] > 110 and arr[1] < 60 :
			return "RED"
		for key, val in colorDictionary.items() : 
			if inThree(arr[0], val[0]) and inThree(arr[1], val[1]) and inThree(arr[2], val[2]) :
				return key
	else :
		print("invalid number")
		return "GRAY"

#helper function
def inThree(a, b) :
	if(abs(a - b) <= 12) :
		return True
	return False

def closeClaw(speed, rotSpeed, c2):
		mD=LargeMotor('outD')
		#print(c2.value(0))
		mD.run_timed(time_sp=250, speed_sp=-250, stop_action = 'hold')
		mD.wait_while('running')
		time.sleep(4)
		#print(c2.value(0))
		#print(c2.value(1))
		#print(c2.value(2))
		if not verifyBall(c2):
			openClaw()
			search()
		else :
			findGreen(speed, rotSpeed)

def openClaw():
		mD=LargeMotor('outD')
		mD.run_timed(time_sp=350,speed_sp=250)
		mD.wait_while('running')
		search()

#returns random number of degrees to rotate
def getRotation() :
	n = random.randint(35, 180)
	degrees = degreesToEngineDegrees(n)
	return degrees

#calculates how many degrees the engines must rotate for the robot to rotate n degrees
def degreesToEngineDegrees(n) :
	degConst = .246575
	dist = float(n)
	degrees = dist / degConst 
	degrees = int(degrees)
	return degrees

def reverse() :
	print("reversing")
	mRt.stop(stop_action = 'brake')
	mLt.stop(stop_action = 'brake')
	mRt.run_timed(time_sp = 2000, speed_sp = -200)
	mLt.run_timed(time_sp = 2000, speed_sp = -200)
	mRt.wait_while('running')
	mLt.wait_while('running')

#positive distance is to the left
def rotate(turnSpeed, dist) :
	#print("rotating")
	# mRt.stop(stop_action = 'brake')
	# mLt.stop(stop_action = 'brake')
	# print(str(dist))
	# mRt.run_to_rel_pos(position_sp = dist, speed_sp = turnSpeed, stop_action='brake')
	#mLt.run_to_rel_pos(position_sp = (dist * -1), speed_sp = turnSpeed, stop_action = 'brake')
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	print("rotating")
	mRt.run_to_rel_pos(position_sp=dist, speed_sp = turnSpeed, stop_action = "brake")
	mLt.run_to_rel_pos(position_sp=-dist, speed_sp = turnSpeed, stop_action = "brake")
	print("Right motor running")
	print("finished rotating")
	sleep(6)

def verifyBall(c2) :
	col = c2.value(0)
	if col > 150 :
		print("Verified")
		return True
	else :
		print("Not Verified")
		return False

#only used in search function
def whenRed() :
	mRt.run_timed(time_sp = 2000, speed_sp = -300)
	mLt.run_timed(time_sp = 2000, speed_sp = -300)
	mRt.wait_while('running')
	mLt.wait_while('running')

#used in retreat function
def whenYellow(turnRadius, turnSpeed) :
	turnRadius = 150
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	rotate(turnSpeed, 30)
	sleep(1)

#used in retreat function
def whenGray(turnRadius, turnSpeed) :
	turnRadius = 150
	mRt.stop(stop_action="brake")
	mLt.stop(stop_action="brake")
	rotate(turnSpeed, -30)
	sleep(1)

#Search for the ball
def search(speed, rotSpeed) :
	print("searching")
	#Claw sensor
	c2 = ColorSensor('in3')
	c2.mode='RGB-RAW'
	mRt.run_forever(speed_sp = speed)
	mLt.run_forever(speed_sp = speed)
	while c2.value(0) < 150 :
		col = getCurrentColor(1)
		print(col)
		if col == "RED" or col == "WHITE" :
			print("stopping")
			mRt.stop(stop_action='brake')
			mLt.stop(stop_action='brake')
			reverse()
			degrees = degreesToEngineDegrees(80)
			rotate(rotSpeed, degrees)
		mRt.run_forever(speed_sp = speed)
		mLt.run_forever(speed_sp = speed)
		sleep(0.1)
	closeClaw(speed, rotSpeed, c2)

#find the green line to retreat
def findGreen(speed, rotSpeed) :
	print("finding green")
	mRt.stop()
	mLt.stop()
	while getCurrentColor(1) != "GREEN" :
		col = getCurrentColor(1)
		mRt.run_forever(speed_sp = speed)
		mLt.run_forever(speed_sp = speed)
		print(col)
		if col == "RED" or col == "WHITE" :
			mRt.stop(stop_action='brake')
			mLt.stop(stop_action='brake')
			reverse()
			degrees = degreesToEngineDegrees(80)
			rotate(rotSpeed, degrees)
		sleep(0.1)
	mRt.stop()
	mLt.stop()
	retreat(speed, rotSpeed)

def retreat(speed, rotSpeed) :
	print("Retreating")
	inbounds = True
	while inbounds:
		mLt.run_forever(speed_sp = -350)
		mRt.run_forever(speed_sp = -350)
		col = getCurrentColor(1)
		print(col)
		if col == "WHITE" :
			#mRt.stop(stop_action='brake')
			#mLt.stop(stop_action='brake')
			#reverse()
			numDegrees = 250
			rotate(rotSpeed, numDegrees)
		elif col == "YELLOW":
			#mRt.stop(stop_action='brake')
			#mLt.stop(stop_action='brake')
			whenYellow(250, rotSpeed)

		elif col == "GRAY" :
			whenGray(250, rotSpeed)

		sleep(0.1)

def run(speed, rotSpeed) :
	print("running")
	#numRed = 0
	#numBlue = 0
	mRt.run_timed(time_sp = 11000, speed_sp = speed)
	mLt.run_timed(time_sp = 11000, speed_sp = speed)
	# onRed = False
	# onBlue = False
	# while numRed < 2 and numBlue < 2 :
	# 	col = getCurrentColor(1)
	# 	print(col)
	# 	if (col == "RED" or col == "RED_ALT") and not onRed:
	# 		numRed+=1
	# 		onRed = True
	# 	elif col == "BLUE" and not onBlue :
	# 		numBlue+=1
	# 		onBlue = True
	# 	elif col == "GRAY" :
	# 		onBlue = False
	# 		onRed = False
	# 	sleep(0.1)
	mRt.wait_while('running')
	mLt.wait_while('running')
	sleep(10)
	print("sleeping engines")
	search(speed, rotSpeed)

driveSpeed = 200
rotationSpeed = 70
retreat(150, rotationSpeed) 