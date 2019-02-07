# Other Imports
import serial
import sys
import numpy
import struct
from array import array
import zlib

def receiver_driver(file_name):

    file = open(file_name, 'rb')
    file_obj = file.read()
    packet_num = int.from_bytes(file_obj[:4], 'big')
    checksum = int.from_bytes(file_obj[60:], 'big')
    file_obj = file_obj[4:60]
    
    def data_checker(data):
        calc_crc = zlib.crc32(data)
        if(checksum == calc_crc):
            print("No Errors On Packet " + str(packet_num))
        else:
            print("Error Detectected On Packet " + str(packet_num))

    data_checker(file_obj)

def main(file_name):
    receiver_driver(file_name)



