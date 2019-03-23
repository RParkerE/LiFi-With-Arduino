from fsm import FSM
from LiFiGUI import SerialGUI
from Sender import Sender_Driver
from Receiver import Receiver_Driver

# Threading Imports
import queue

class Main:
    def __init__(self):
        self.__my_queue = queue.Queue()

        self.__my_fsm = FSM()

        self.__sd = Sender_Driver(self.__my_fsm)
        self.__rd = Receiver_Driver(self.__my_fsm)

        self.__my_gui = SerialGUI(self.__my_fsm, self.__sd, self.__rd, self.__my_queue)
        self.__my_gui.window.mainloop()


main = Main()
