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
  "RED" : [130, 22, 25],
  #"RED_ALT" : [71, 17, 13],
  "WHITE" : [177, 157, 240],
  "BLUE" : [19, 35, 84],
  "GRAY" : [33, 34, 39],
  "YELLOW" : [144, 92, 38],
  "YELLOW_ALT" : [121, 90, 25],
  "GREEN" : [44, 83, 57],
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

def closeClaw(speed, rotSpeed):
		mD=LargeMotor('outD')
		print(c2.value(0))
		mD.run_timed(time_sp=250, speed_sp=-250, stop_action = 'hold')
		mD.wait_while('running')
		time.sleep(4)
		print(c2.value(0))
		#print(c2.value(1))
		#print(c2.value(2))
		if not verifyBall:
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
	degConst = .12587
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

def rotate(turnSpeed, dist) :
	print("rotating")
	mRt.stop(stop_action = 'brake')
	mLt.stop(stop_action = 'brake')
	print(str(dist))
	mRt.run_to_rel_pos(position_sp = dist, speed_sp = turnSpeed, stop_action='brake')
	#mLt.run_to_rel_pos(position_sp = (dist * -1), speed_sp = turnSpeed, stop_action = 'brake')

def verifyBall() :
	col = c2.value()
	if col > 150 :
		print("Verified")
		return True
	else :
		print("Not Verified")
		return False

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
	while c2.value(0) < 150 :
		col = getCurrentColor(1)
		print(col)
		if col == "BLUE" or col == "WHITE" :
			print("stopping")
			mRt.stop(stop_action='brake')
			mLt.stop(stop_action='brake')
			reverse()
			rotate(rotSpeed, 150)
		#elif col == "RED" :
			#whenRed()
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
			numDegrees = 150
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
	print("running")
	#numRed = 0
	#numBlue = 0
	mRt.run_timed(time_sp = 10, speed_sp = speed)
	mLt.run_timed(time_sp = 10, speed_sp = speed)
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
	print("sleeping engines")
	search(speed, rotSpeed)

driveSpeed = 200
rotationSpeed = 70
run(driveSpeed, rotationSpeed) 