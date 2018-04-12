#!/usr/bin/python
from ev3dev.ev3 import *
from threading import Thread

def Scan():
	global objectSpotted
	ir = InfraredSensor()
	eyeMotor = LargeMotor('outC')
	objectSpotted = False
	dir = 175
	while(objectSpotted == False):
		eyeMotor.stop()
		eyeMotor.run_to_rel_pos(position_sp=dir, speed_sp=75, stop_action="brake")
		distance = ir.value()
		if(ir.value() < 30):
			objectSpotted = True
			eyeMotor.stop()
			print("spotted")
		dir *= -1
		eyeMotor.wait_while('running')

def Slap():
	slapMotor = LargeMotor('outA')
	slapMotor.run_to_rel_pos(position_sp=180, speed_sp=1000, stop_action="hold")
	slapMotor.wait_while('running')
	slapMotor.run_to_rel_pos(position_sp=-180, speed_sp=1000, stop_action="hold")

#scanThread = Thread(target=Scan)
#slapThread = Thread(target=Slap)
#scanThread.start()
global objectSpotted
objectSpotted = False
while(objectSpotted == False) :
	Scan()
Slap()
