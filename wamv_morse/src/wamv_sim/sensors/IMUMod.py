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

from morse.modifiers.abstract_modifier import AbstractModifier

class IMUModifier(AbstractModifier):
    def initialize(self):
        """ initialization of parameters ... """

    def modify(self):
        # Place where the data modification occurs

        # Convert to NED frame
        self.data['angular_velocity'].y = -self.data['angular_velocity'].y
        self.data['angular_velocity'].z = -self.data['angular_velocity'].z

        self.data['linear_acceleration'].y = -self.data['linear_acceleration'].y
        self.data['linear_acceleration'].z = -self.data['linear_acceleration'].z
