from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Other Imports
#import serial
import sys
import math
import numpy
import struct
from array import array
import zlib
import time

def sender_driver(file_name, serialPort):

    count = 0

    file = open(file_name, 'rb')
    file_obj = file.read()
    file_size = len(file_obj)
    packet_num = math.ceil(file_size/56)
    padding_size = 56 - (file_size % 56)
    padding = '0' * padding_size
    file_obj = file_obj + padding.encode('utf-8')
    file_data = list(zip(*[iter(file_obj)]*56))

    #packet Creator adding 4 bytes index to 48 bytes of data
    def packet_creator(counter):
        data = file_data[counter]
        data_byte = bytes(data)
        counter += 1
        index = counter.to_bytes(4, 'big')
        data_crc = zlib.crc32(data_byte) & 0xffffffff
        data_crc = data_crc.to_bytes(4, 'big')
        packet = index + data_byte + data_crc
        print(packet)
        return packet
    
    i = 0
    while(i<packet_num):
        packet = packet_creator(i)
        serialPort.write(packet)
        time.sleep(0.1)
        i += 1

    file.close()
    
    
