# Other Imports
import serial
import sys
import numpy
import struct
from array import array
import zlib

def receiver_driver(file_name, serialPort):
    file = open(file_name, "ab")

    def data_checker(data):
        calc_crc = zlib.crc32(data)
        if(checksum == calc_crc):
            file.write(data)
            print("No Errors On Packet " + str(packet_num))
        else:
            print("Error Detectected On Packet " + str(packet_num))
            
    packet_obj = serialPort.read(64)
    print(packet_obj)
    packet_num = int.from_bytes(packet_obj[:4], 'big')
    checksum = int.from_bytes(packet_obj[60:], 'big')
    payload = packet_obj[4:60]
    
    data_checker(payload)
    file.close()



