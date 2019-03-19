# GUI Imports
from tkinter import Tk, ttk
from tkinter import Label, Button, Entry, messagebox
from tkinter.filedialog import askopenfilename

# Threading Imports
import queue

# Other Imports
import time
import serial
from serial_connect import connectToSerial, disconnectFromSerial


class SerialGUI:
    def __init__(self, fsm, sender, receiver, in_queue):
        self.__my_queue = in_queue

        # Define GUI Window, Call createWidgets()
        self.window = Tk()
        self.window.title("LiFi Communication")

        # Global Variables
        self.__state_machine = fsm
        self.__sd = sender
        self.__rd = receiver
        
        self.__serialPort = serial.Serial(timeout=.25)
        self.__baudRate = ""
        self.__comPort = ""
        self.__fileName = ""

        self.window['padx'] = 5
        self.window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The Send/Receive frame
        fileFrame = ttk.LabelFrame(self.window, text="File Setup")
        fileFrame.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        inFileLbl = Label(fileFrame, text="Select File:")
        inFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.inFileTxt = Entry(fileFrame)
        self.inFileTxt.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)

        self.inFileBtn = Button(fileFrame, text="Browse...", command=self.loadFile)
        self.inFileBtn.grid(row=0, column=8, sticky='W', padx=5, pady=2)

        # - - - - - - - - - - - - - - - - - - - - -
        # The Baud Rate/COM Port frame
        connectFrame = ttk.LabelFrame(self.window, text="Serial Setup")
        connectFrame.grid(row=2, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.inBaudRate = Entry(connectFrame)
        self.inBaudRate.grid(row=3, column=2, columnspan=7, sticky="WE", pady=3)

        self.inBaudLbl = Label(connectFrame, text="Baud Rate:")
        self.inBaudLbl.grid(row=3, column=1, sticky='W', padx=5, pady=2)

        self.inComPort = Entry(connectFrame)
        self.inComPort.grid(row=4, column=2, columnspan=7, sticky="WE", pady=3)

        self.inComLbl = Label(connectFrame, text="COM Port:")
        self.inComLbl.grid(row=4, column=1, sticky='W', padx=5, pady=2)

        self.connectButton = Button(connectFrame, text="Connect", command=lambda: connectToSerial(self))
        self.connectButton.grid(row=5, column=2)

        self.disconnectButton = Button(connectFrame, text="Disconnect", command=lambda: disconnectFromSerial(self))
        self.disconnectButton.grid(row=5, column=3)
        self.disconnectButton.config(state="disabled")

        # - - - - - - - - - - - - - - - - - - - - -
        # Start button in the upper right corner
        self.startButton = Button(self.window, text="SEND", command=self.pushToSend)
        self.startButton.grid(row=0, column=15)

    @property
    def my_queue(self):
        return self.__my_queue

    @property
    def state_machine(self):
        return self.__state_machine

    @property
    def sd(self):
        return self.__sd

    @sd.setter
    def sd(self, send):
        self.__sd = send

    @property
    def rd(self):
        return self.__rd

    @rd.setter
    def rd(self, receive):
        self.__rd = receive

    @property
    def serialPort(self):
        return self.__serialPort

    @serialPort.setter
    def serialPort(self, serial):
        self.__serialPort = serial

    @property
    def baudRate(self):
        return self.__baudRate

    @baudRate.setter
    def baudRate(self, baud):
        self.__baudRate = baud

    @property
    def comPort(self):
        return self.__comPort

    @comPort.setter
    def comPort(self, port):
        self.__comPort = port

    @property
    def fileName(self):
        return self.__fileName

    @fileName.setter
    def fileName(self, name):
        self.__fileName = name

    # Opens File Dialog And Saves Selected File to self.fileName
    def loadFile(self):
        self.fileName = askopenfilename()
        self.rd.file_name = self.fileName
        self.sd.file_name = self.fileName
        self.inFileTxt.insert(0, self.fileName)

    def pushToSend(self):
        if self.fileName != "":
            self.state_machine.on_event("send")
            self.state_machine.on_event("")
            self.sd.meta_creator()
            self.startButton["text"] = "SENDING..."
        else:
            messagebox.showerror("Error", "File Must Be Selected To Send")

        self.startButton["text"] = "SEND"

    def threadProcessor(self):
        while self.my_queue.qsize():
            try:
                msg = self.my_queue.get(0)
                if msg == "meta":
                    self.state_machine.on_event("")
                    self.rd.parse_meta()
                else:
                    pass

            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

# program = SerialGUI()
# program.window.mainloop()
