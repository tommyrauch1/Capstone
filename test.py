from ev3dev.ev3 import *
from time import sleep

mRt = LargeMotor('outA')
mLt = LargeMotor('outC')

dist = 1080
turnSpeed = 130

mRt.run_to_rel_pos(position_sp = dist, speed_sp = turnSpeed, stop_action='brake')
mLt.run_to_rel_pos(position_sp = (dist * -1), speed_sp = turnSpeed, stop_action = 'brake')