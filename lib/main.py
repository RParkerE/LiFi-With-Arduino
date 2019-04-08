"""
main.py

This file is the main file for the LiFi driver. It imports all the files associated with
our driver and gives appropriate access to each object.
"""

from fsm import FSM
from LiFiGUI import SerialGUI
from Sender import Sender_Driver
from Receiver import Receiver_Driver

class Main:
    def __init__(self):
        # Create a State Machine object
        self.__my_fsm = FSM()

        # Create a Sender and Receiver Driver object
        self.__sd = Sender_Driver(self.__my_fsm)
        self.__rd = Receiver_Driver(self.__my_fsm)

        # Create a GUI object
        self.__my_gui = SerialGUI(self.__my_fsm, self.__sd, self.__rd)
        self.__my_gui.window.mainloop()


main = Main()
