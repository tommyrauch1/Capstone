#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random



#stay in bounds done
#see ball 
#grab ball


mRt = LargeMotor('outB')
mLt = LargeMotor('outC')

mLt.run_to_rel_pos(position_sp=1070, speed_sp = 200, stop_action = "brake")
mRt.run_to_rel_pos(position_sp=-1070, speed_sp = 200, stop_action = "brake")