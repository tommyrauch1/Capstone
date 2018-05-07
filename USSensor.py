#!/usr/bin/python
from ev3dev.ev3 import *
from threading import Thread
import math

slapMotor = LargeMotor('outA')
ir = UltrasonicSensor()
ir.mode='US-DIST-CM'
eyeMotor = LargeMotor('outC')

def getSensorDistance(a, b) :
	distance = sqrt((a*a), (b*b))
	return distance

def finishRotation(num) :
	distanceToRotate = (7 - num) * 25
	eyeMotor.run_to_rel_pos(position_sp = distanceToRotate, speed_sp = 75, stop_action = "brake")
	sleep(5)

#need to figure out how to design this. What is the viewing angle of sensor? Will require testing (point at arm, increase distance until nothing 
#is seen in range). Essentially, do i want to ignore a certain range or a few cm either side of the number
#def withinRange() :

def Scan():
	objectSpotted = False
	dist = 25
	num = 0
	armLength = 0
	sensorHeight = 0
	viewDistance = getSensorDistance(armLength, sensorHeight)
	#7 per direction
	while objectSpotted == False :
		eyeMotor.stop()
		eyeMotor.run_to_rel_pos(position_sp=dist, speed_sp=75, stop_action="brake")
		distance = ir.value()
		print(str(distance))
		if(outSideOfRange()):
			objectSpotted = True
			eyeMotor.stop()
			print("spotted")
			finishRotation(num)
			return objectSpotted
		if num == 7 :
			num = 0
			dist = dist*-1
		else :
			num++
		eyeMotor.wait_while('running')
	return False

def Slap():
	slapMotor.run_to_rel_pos(position_sp=170, speed_sp=1000, stop_action="hold")
	slapMotor.wait_while('running')
	slapMotor.run_to_rel_pos(position_sp=-170, speed_sp=1000, stop_action="hold")
	slapMotor.wait_while('running')

def run() :
	flag = True
	while flag :
		if Scan() :
			Slap()



