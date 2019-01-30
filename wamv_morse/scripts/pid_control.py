#!/usr/bin/env python3.6

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ Mission Systems Pty Ltd ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Project: WamV-Morse-Sim
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Primary Author:
# david battle <david.battle@missionsystems.com.au>
# Other Author(s):
# none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Date Created:
# 29/01/2019
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from pymoos import pymoos
from math import radians, pi, atan2, sin, cos, degrees
import numpy as np
import time

# Control limits
rudder_scale = 100
thrust_scale = 100

Kp_yaw = -0.5
Kd_yaw = -0.7

Kp_speed = 3
Kd_speed = -.5

speed = 0
accel = 0

yaw = 0
yaw_rate = 0

# Init Pymoos comms
comms = pymoos.comms()

# Smallest angle from a to b
def angdiff(a,b):

    return atan2(sin(a-b),cos(a-b))

def onc():

    comms.register('MORSE_SIM_X',0)
    comms.register('MORSE_SIM_Y',0)
    comms.register('MORSE_DVL_BODY_VEL_X',0)
    comms.register('MORSE_IMU_ACCEL_X',0)
    comms.register('MORSE_SIM_YAW',0)
    comms.register('MORSE_IMU_GYRO_Z',0)

    return True

def onm():

    global nav_x
    global nav_y
    global yaw
    global yaw_rate
    global speed
    global accel

    msg_list = comms.fetch()

    for msg in msg_list:
   
        val = msg.double()

        if msg.name() == 'MORSE_SIM_X':
            nav_x = val

        elif msg.name() == 'MORSE_SIM_Y':
            nav_y = val

        elif msg.name() == 'MORSE_DVL_BODY_VEL_X':
            speed = val

        elif msg.name() == 'MORSE_IMU_ACCEL_X':
            accel = val

        elif msg.name() == 'MORSE_SIM_YAW':
            yaw = val

        elif msg.name() == 'MORSE_IMU_GYRO_Z':
            yaw_rate = val

    return True

def main():

    global desired_yaw
    global yaw_err
    global yaw
    global desired_speed
    global speed_err
    global speed

    # Kickoff Pymoos callbacks
    comms.set_on_connect_callback(onc)
    comms.set_on_mail_callback(onm)
    comms.run('localhost',9000,'pid')

    desired_yaw = radians(0)
    desired_speed = 2

    while True:

        # Set the speed of the control loop here.
        time.sleep(.05)

        # Yaw loop
        yaw_err = angdiff(desired_yaw, yaw)

        P = Kp_yaw * yaw_err
        D = Kd_yaw * yaw_rate

        rudder = P + D

        # Enforce rudder limits
        if rudder > 1:
            rudder = 1
        elif rudder < -1:
            rudder = -1

        desired_rudder = rudder * rudder_scale    

        comms.notify('DESIRED_RUDDER', desired_rudder, pymoos.time());

        # Speed loop
        speed_err = desired_speed - speed

        P = Kp_speed * speed_err
        D = Kd_speed * accel

        thrust = P + D

        # Enforce thrust limit
        if thrust > 1:
            thrust =1
        if thrust < -1:
            thrust = -1

        desired_thrust = thrust * thrust_scale

        comms.notify('DESIRED_THRUST', desired_thrust, pymoos.time());

        print("Desired_yaw: %.1f, Yaw: %.1f, Yaw error: %.1f" % (degrees(desired_yaw), degrees(yaw), degrees(yaw_err)))
        print("Desired_speed: %.1f, Speed: %.1f, Speed error: %.1f" % (desired_speed, speed, speed_err))

if __name__ == "__main__":
    main()        
