#!/usr/bin/python
from ev3dev.ev3 import *
from threading import Thread

def Scan(dir):
	ir = InfraredSensor()
	eyeMotor = LargeMotor('outC')
	objectSpotted = False
	while(!objectSpotted):
		eyeMotor.run_to_rel_pos(position_sp=dir, speed_sp=100, stop_action="brake")
		distance = ir.value()
		if(ir.value < 100):
			objectSpotted = True
	return objectSpotted

def Slap(dir):
	slapMotor = LargeMotor('outA')
	slapMotor.run_to_rel_pos(position_sp=dir, speed_sp=1000, stop_action="brake")

scanThread = Thread(target=Scan)
slapThread = Thread(target=Slap)
