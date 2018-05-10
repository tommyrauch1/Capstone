#!/usr/bin/env python3
from ev3dev.ev3 import *
import threading
import math
from time import sleep

r  = LargeMotor('outA')
l   = LargeMotor('outC')
print("Forward")
r.run_timed(time_sp = 3000, speed_sp = 500)
l.run_timed(time_sp = 3000, speed_sp = 500)

r.wait_while('running')
l.wait_while('running')

r.stop()
l.stop()

print("Turning")

r.run_timed(time_sp = 3000, speed_sp = 500)
l.run_timed(time_sp = 3000, speed_sp = -500)
