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

print("FORWARDS")
mLt.run_forever(speed_sp=100)
mRt.run_forever(speed_sp=100)
sleep(2)

mLt.stop()
mRt.stop()

mLt.run_forever(speed_sp=-100)
mRt.run_forever(speed_sp=-100)