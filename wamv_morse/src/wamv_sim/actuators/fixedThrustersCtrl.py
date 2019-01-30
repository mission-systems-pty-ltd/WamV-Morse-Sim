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
from morse.middleware.moos import MOOSSubscriber

class ThrustReader(MOOSSubscriber):
    """ Read thrust commands and update local data. """

    def initialize(self):

        # initialize the parent class
        MOOSSubscriber.initialize(self)

        # register for control variables from the database
        self.register_message_to_queue("DESIRED_RUDDER",'rudder_queue', self.on_msg)
        self.register_message_to_queue("DESIRED_THRUST",'thrust_queue', self.on_msg)

    def on_msg(self, msg):

        if (msg.key() == "DESIRED_RUDDER") and (msg.is_double()):
            self.data['desired_rudder'] = msg.double()
        elif (msg.key() == "DESIRED_THRUST") and (msg.is_double()):
            self.data['desired_thrust'] = msg.double()

        self._new_messages = True
        return True

    def update_morse_data(self):
        logger.debug('ThrustReader.update_morse_data() called.')
