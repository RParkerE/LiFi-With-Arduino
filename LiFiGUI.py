# GUI Imports
from tkinter import Tk, ttk
from tkinter import Label, Button, Entry, Menu, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Other Imports
import serial
import sys
import Sender

class SerialGUI:
        def __init__(self):
            # Define GUI Window, Call createWidgets()
            self.window = Tk()
            self.window.title("LiFi Communication")
            self.createWidgets()

            # Global Variables (Mainly For Serial Use)
            self.serialPort = serial.Serial()
            self.baudRate = ""
            self.comPort = ""
            self.commState = ""
            self.fileName = ""

        def createWidgets(self):
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

            self.sendButton = Button(fileFrame, text="Transmit: Send File", command=self.sendSide)
            self.sendButton.grid(row=1, column=1)

            self.receiveButton = Button(fileFrame, text="Receive: Write File", command=self.receiveSide)
            self.receiveButton.grid(row=1, column=2)

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

            self.connectButton = Button(connectFrame, text="Connect", command=self.connectToSerial)
            self.connectButton.grid(row=5, column=2)

            self.disconnectButton = Button(connectFrame, text="Disconnect", command=self.disconnectFromSerial)
            self.disconnectButton.grid(row=5, column=3)
            self.disconnectButton.config(state="disabled")

            # - - - - - - - - - - - - - - - - - - - - -
            # The Commands frame
            helpLf = ttk.LabelFrame(self.window, text=" Quick Help ")
            helpLf.grid(row=0, column=9, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

            self.helpLbl = Label(helpLf, text="Help will come - ask for it.")
            self.helpLbl.grid(row=0)

            # - - - - - - - - - - - - - - - - - - - - -
            # Start button in the upper right corner
            self.startButton = Button(self.window, text="Start", command=self.pushToStart)
            self.startButton.grid(row=0, column=15)

        # Setup Serial Port To Connect To Specified COM Port At Apecified Baud Rate
        def connectToSerial(self):
            try:
                self.comPort = "/dev/" + self.inComPort.get()
                self.baudRate = self.inBaudRate.get()
                self.serialPort.port = self.comPort
                self.serialPort.baudrate = self.baudRate
                self.serialPort.open()
                if(self.serialPort.is_open):
                    self.connectButton["text"] = "Connected: Port " + self.comPort + " at " + self.baudRate
                    self.connectButton.config(state="disabled")
                    self.disconnectButton.config(state="normal")
                    return self.serialPort
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)

        # Disconnect Serial Port If One Is Open
        def disconnectFromSerial(self):
            try:
                self.serialPort.close()
                if(not self.serialPort.is_open):
                    self.disconnectButton["text"] = "Disconnected"
                    self.disconnectButton.config(state="normal")
                    self.connectButton.config(state="disabled")
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)

        # Opens File Dialog And Saves Selected File to self.fileName
        def loadFile(self):
            self.fileName = askopenfilename()
            self.inFileTxt.insert(0, self.fileName)

        # Set self.commState To send And Show Chosen State
        def sendSide(self):
            try:
                self.commState = "send"
                self.sendButton["text"] = "Sender Chosen"
                self.sendButton.config(state="disabled")
                self.receiveButton["text"] = "Receive: Write File"
                self.receiveButton.config(state="normal")
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)

        # Set self.commState To receive And Show Chosen State
        def receiveSide(self):
            try:
                self.commState = "receive"
                self.receiveButton["text"] = "Receiver Chosen"
                self.receiveButton.config(state="disabled")
                self.sendButton["text"] = "Transmit: Send File"
                self.sendButton.config(state="normal")
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)

        # Wirte/Read Serial Port Based On self.commState
        def pushToStart(self):
            Sender.main(self.fileName)
            """self.startButton["text"] = "Started..."
            if(self.commState == "send"):
                try:
                    f = open(self.fileName, "rb")
                    for line in f:
                        data = line
                        self.serialPort.write(data)
                    self.startButton["text"] = "Start"
                except:
                    e = sys.exc_info()[0]
                    print("Error: %s" % e)
            if(self.commState == "receive"):
                try:
                    f = open(self.fileName, "wb")
                    data = self.serialPort.read()
                    while(data):
                        f.write(data)
                        data = self.serialPort.read()
                    self.startButton["text"] = "Start"
                except:
                    e = sys.exc_info()[0]
                    print("Error: %s" % e)"""
    
program = SerialGUI()
program.window.mainloop()
