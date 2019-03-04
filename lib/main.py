from fsm import FSM
from LiFiGUI import SerialGUI


class Main:
    def __init__(self):
        self.__my_fsm = FSM()

        self.__my_gui = SerialGUI(self.__my_fsm)
        self.__my_gui.window.mainloop()


main = Main()
