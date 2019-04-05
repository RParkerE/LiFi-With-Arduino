"""
serial_connect.py

This file contains the functions for connecting to a serial device. It also has a function for
finding and automatically connecting to Arduino devices.
"""

import time
import warnings
import platform
from serial.tools import list_ports


# Get Serial Port Associated With Arduino and connects to it
def getArduinoPort():

	arduino_ports = [
		p.device
		for p in list_ports.comports()
		if 'Arduino' in p.description
	]

	if not arduino_ports:
		raise IOError("No Arduino Found")
	if len(arduino_ports) > 1:
		warnings.warn('Multiple Arduinos Found - Using First One')

	return arduino_ports[0]


# Setup Serial Port To Connect To Specified COM Port At Specified Baud Rate
def connectToSerial(self):
	sys_name = platform.system()
	if self.inComPort.get() == "":
		self.comPort = getArduinoPort()
		self.baudRate = 115200
	else:
		if sys_name == "Windows":
			self.comPort = "COM" + self.inComPort.get()
			self.baudRate = self.inBaudRate.get()
		else:
			self.comPort = "/dev/" + self.inComPort.get()
			self.baudRate = self.inBaudRate.get()

	self.serialPort.port = self.comPort
	self.serialPort.baudrate = self.baudRate
	self.serialPort.setRTS(False)
	self.serialPort.setDTR(False)
	self.serialPort.open()
	if self.serialPort.is_open:
		self.serialPort.reset_output_buffer()
		self.serialPort.flush()
		self.serialPort.reset_input_buffer()
		self.connectButton["text"] = "Connected: Port " + str(self.comPort) + " at " + str(self.baudRate)
		self.connectButton.config(state="disabled")
		self.disconnectButton["text"] = "Disconnect"
		self.disconnectButton.config(state="normal")
		self.sd.serialPort = self.serialPort
		self.rd.serialPort = self.serialPort

	return self.serialPort


# Disconnect Serial Port If One Is Open
def disconnectFromSerial(self):
	self.serialPort.close()
	if not self.serialPort.is_open:
		self.disconnectButton["text"] = "Disconnected"
		self.disconnectButton.config(state="disabled")
		self.connectButton["text"] = "Connect"
		self.connectButton.config(state="normal")
