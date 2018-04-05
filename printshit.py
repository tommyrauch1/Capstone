#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

print("Dank memes cant melt steel beams")

mB = LargeMotor('outA')
mC = LargeMotor('outC')

mB.run_forever(speed_sp=450)
mC.run_forever(speed_sp=450)

sleep(10)

mB.stop(stop_action='brake')
mC.stop(stop_action='brake')