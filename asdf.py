#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math
import random

mRt = LargeMotor('outB')
mLt = LargeMotor('outC')

mRt.stop()
mLt.stop()