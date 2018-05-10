from ev3dev.ev3 import *
from time import sleep

def closeClaw():
        mD=LargeMotor('outD')
        print(c2.value(0))
        if c2.value(0) > 100:
                mD.run_timed(time_sp=250, speed_sp=-250, stop_action = 'hold')
                mD.wait_while('running')
        else:
                print("tennis ball not found")
        time.sleep(4)
        print(c2.value(0))
        #print(c2.value(1))
        #print(c2.value(2))
        if c2.value() < 150:
                openClaw()
def openClaw():
        mD=LargeMotor('outD')
        mD.run_timed(time_sp=350,speed_sp=250)
        mD.wait_while('running')
        
c1 = ColorSensor('in2')
c2 = ColorSensor('in3')
c1.mode='RGB-RAW'
c2.mode='RGB-RAW'
#colors=('unknown','black','blue','green','yellow','red','white','brown')
closeClaw()
