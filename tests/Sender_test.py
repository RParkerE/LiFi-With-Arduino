import sys
import serial
sys.path.append('../lib/')
from Sender import Sender_Driver


serial_port = serial.Serial(port="/dev/cu.usbmodem14201", baudrate=115200)

sd = Sender_Driver('/Users/raheefjalmiran/Documents/GitHub/LiFi-Python/files/sender_test.txt', serial_port)

meta = sd.meta_creator()
print(meta)

data_send = sd.packet_loop()
print(data_send)

print(sd.get_file_size())
