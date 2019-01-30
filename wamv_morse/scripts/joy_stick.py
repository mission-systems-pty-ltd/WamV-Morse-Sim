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
import pygame
import time

comms = pymoos.comms()
pygame.init()

def c():

    return True

def main():

    comms.set_on_connect_callback(c)
    comms.run('localhost',9000,'joystick')
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Seems to need a little delay here...
    time.sleep(1)

    while True:

        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        # Initialize the joysticks
        pygame.joystick.init()
   
        #---------------------------------------------------------
        rudder =  100 * joystick.get_axis(2)
        thrust = -100 * joystick.get_axis(3)

        comms.notify('DESIRED_RUDDER',rudder,pymoos.time());
        comms.notify('DESIRED_THRUST',thrust,pymoos.time());

        clock.tick(20)

if __name__ == "__main__":
    main()        
