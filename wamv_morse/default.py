#! /usr/bin/env morseexec

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

""" Basic MORSE simulation scene for <wamv_sim> environment
"""
from morse.builder import *
from wamv_sim.builder.robots import Wamv
from math import pi
from helpers.compound import *
from wamv_sim.builder.actuators import Buoyancy
from wamv_sim.builder.actuators import Drag

wamv = Wamv()

# Environmental properties get attached to this robot
fakerobot = FakeRobot()

# Handles buoyancy for all objects
buoyancy = Buoyancy()
fakerobot.append(buoyancy)

# Handles drag for all objects
# Not functioning yet!
drag = Drag()
fakerobot.append(drag)

# Use these on compound robots
translate_compound(wamv,0,0,0)
rotate_compound(wamv,0,0,0)

wamv.thrusters.properties(Prop_diam = .3)
wamv.thrusters.properties(Max_rpm = 1000)
wamv.thrusters.properties(Thrust_rate = 0.25)
wamv.thrusters.properties(Thrust_scale = 100)
wamv.thrusters.properties(Rudder_scale = 100)

env = Environment('wamv_sim/environments/sea_surface_only.blend')

# SW corner JB
env.properties(latitude = -35.1118, longitude = 150.7133, altitude=0)
env.set_camera_location([-7.3602, -6.5155, 6.8010])
env.set_camera_rotation([0.8000,-0.0000,-0.9590])

# env.set_camera_location([-5.0, -5.0, 5.0])
# env.set_camera_rotation([1.0, 0.0, -1])
env.set_camera_clip(1,2000)
env.set_camera_speed(10)
env.show_framerate(True)
# env.fullscreen(True)
# env.show_physics(True)
# env.set_debug(True)

# Select the PiP camera
# env.select_display_camera(wamv.rear_camera)
