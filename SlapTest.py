#!/usr/bin/python
from ev3dev.ev3 import *
from time import sleep

mA = LargeMotor('outA')

mA.run_to_rel_pos(position_sp=180, speed_sp=1000, stop_action="brake")
sleep(1)
