#!/usr/bin/env python3

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

import matplotlib.pyplot as plt
from pymoos import pymoos
import numpy as np
import time
from math import degrees, radians, atan

ASCENT         = 1
DESCENT        = -1
comms = pymoos.comms()

def c():

    comms.register('NAV_X',0)
    comms.register('LOND_RATIO',0)
    comms.register('ALPHA_DEG',0)
    comms.register('NAV_PITCH',0)
    comms.register('PITCH_RATE',0)
    comms.register('NAV_SPEED',0)
    comms.register('MORSE_DVL_WORLD_VEL_X',0)
    comms.register('MORSE_DVL_WORLD_VEL_Z',0)
    comms.register('DESIRED_SPEED',0)
    comms.register('MODE',0)

    return True

def main():

    comms.set_on_connect_callback(c)
    comms.run('localhost',9000,'speed_pid')

    # Seems to need a little delay here...
    time.sleep(1)

    ##########################################################
    # Speed-to-pitch PID parameters
    Kp_sp = 60
    Ki_sp = 3
    Kd_sp = 150

    # Integral
    i_sp = 0

    # Pitch-to-trim PID parameters
    Kp_pt = 2
    Ki_pt = 0
    Kd_pt = 10

    # Integral
    i_pt = 0

    ##########################################################
    # Set time
    prev_time = pymoos.time()
    desired_speed = 0
    prev_speed_error = 0
    delta_time = 0
    VBE_trim = 0
    mode = DESCENT

    while True:
   
        time.sleep(1)

        msg_list = comms.fetch()
        
        for msg in msg_list:
            val = msg.double()
            if msg.name() == 'NAV_X':
                x = val
            elif msg.name() == 'LOND_RATIO':
                lond = val
            elif msg.name() == 'NAV_DEPTH':
                depth = val
            elif msg.name() == 'ALPHA_DEG':
                alpha = val
            elif msg.name() == 'NAV_PITCH':
                pitch = degrees(val)
            elif msg.name() == 'PITCH_RATE':
                pitch_rate = degrees(val)                
            elif msg.name() == 'NAV_SPEED':
                speed = val
            elif msg.name() == 'MORSE_DVL_WORLD_VEL_X':
                world_speed = val
            elif msg.name() == 'MORSE_DVL_WORLD_VEL_Z':
                sink_rate = val
            elif msg.name() == 'DESIRED_SPEED':
                desired_speed = val
            elif msg.name() == 'MODE':
                mode = val
            else:
        	    print('HELP')

        # Get the time
        current_time = msg.time()
        delta_time = current_time-prev_time
        prev_time = current_time

        if delta_time == 0:
            print("HALTED...")
            continue

        # Speed-to-pitch PID controller
        speed_error = desired_speed-speed        
        i_sp = i_sp + speed_error*delta_time
        d_sp = (speed_error-prev_speed_error)/delta_time

        prev_speed_error = speed_error

        P_sp = Kp_sp*speed_error
        I_sp = Ki_sp*i_sp
        D_sp = Kd_sp*d_sp

        desired_pitch = mode*(P_sp + I_sp + D_sp)

        # Pitch_to_trim PID controller
        pitch_error = desired_pitch-pitch        
        i_pt = i_pt + pitch_error*delta_time
        d_pt = -pitch_rate

        P_pt = Kp_pt*pitch_error
        I_pt = Ki_pt*i_pt
        D_pt = Kd_pt*d_pt

        desired_FA_trim = P_pt + I_pt + D_pt

        comms.notify('DESIRED_FA_TRIM',desired_FA_trim,pymoos.time());

if __name__ == "__main__":
    main()        
