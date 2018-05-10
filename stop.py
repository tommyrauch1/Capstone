#!/usr/bin/env python3
from ev3dev.ev3 import *
import threading
import math
from time import sleep

RIGHT_MOTOR  = LargeMotor('outA')
LEFT_MOTOR   = LargeMotor('outC')
mFlip = LargeMotor('outA')

RIGHT_MOTOR.stop(stop_action='brake')
LEFT_MOTOR.stop(stop_action='brake')
mFlip.stop(stop_action='brake')