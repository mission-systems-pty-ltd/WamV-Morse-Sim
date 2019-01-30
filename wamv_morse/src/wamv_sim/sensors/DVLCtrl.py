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

import logging; logger = logging.getLogger("morse." + __name__)
from morse.middleware.moos import MOOSNotifier

class DVLNotifier(MOOSNotifier):
    """ Notify DVL """

    def default(self, ci = 'unused'):

        # Time stamp for outgoing data
        ts = self.data['timestamp']

        # logger.debug('DVLNotifier is publising!')
        self.notify('MORSE_DVL_WORLD_VEL_X', self.data['Wx'], ts)
        self.notify('MORSE_DVL_WORLD_VEL_Y', self.data['Wy'], ts)
        self.notify('MORSE_DVL_WORLD_VEL_Z', self.data['Wz'], ts)
        self.notify('MORSE_DVL_BODY_VEL_X',  self.data['Bx'], ts)
        self.notify('MORSE_DVL_BODY_VEL_Y',  self.data['By'], ts)
        self.notify('MORSE_DVL_BODY_VEL_Z',  self.data['Bz'], ts)
        self.notify('MORSE_DVL_HEADING',     self.data['heading'], ts)
        self.notify('MORSE_DVL_ALTITUDE',    self.data['z'], ts)
        self.notify('MORSE_DVL_DEPTH',       self.data['depth'], ts)
