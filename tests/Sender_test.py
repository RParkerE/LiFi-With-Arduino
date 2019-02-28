import sys
import serial
sys.path.append('../lib/')
from Sender import Sender_Driver


serial_port = serial.Serial()

sd = Sender_Driver("..\\files\\sender_test.txt", serial_port)

meta = sd.meta_creator()
print(meta)

data_send = sd.packet_loop()
print(data_send)
