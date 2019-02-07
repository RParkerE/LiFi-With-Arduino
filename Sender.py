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

def sender_driver(file_name):

    count = 0

    file = open(file_name, 'rb')
    file_obj = file.read()
    file_size = len(file_obj)
    packet_num = math.ceil(file_size/56)
    padding_size = 60 - (file_size % 56)
    padding = '0' * padding_size
    file_obj = file_obj + padding.encode('utf-8')
    file_data = list(zip(*[iter(file_obj)]*56))

    #packet Creater adding 3 bytes index to 48 bytes of data
    def packet_creater(counter):
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
    allData = b''
    while(i<packet_num):
        allData += packet_creater(count)
        count += 1
        i += 1

    out_file_name = askopenfilename()
    out_file = open(out_file_name, 'wb')
    out_file.write(allData)
    file.close()
    out_file.close()


def main(file_name):
    sender_driver(file_name)

"""if __name__ == "__main__":
    main()"""
    
    
