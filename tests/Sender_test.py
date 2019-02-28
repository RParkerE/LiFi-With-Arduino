import serial
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\lib')))
from Sender import Sender_Driver


serial_port = serial.Serial()

sd = Sender_Driver("..\\files\\sender_test.txt", serial_port)

meta = sd.meta_creator()
print(meta)

data_send = sd.packet_loop()
print(data_send)
