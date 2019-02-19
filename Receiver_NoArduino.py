# Other Imports
import serial
import sys
import numpy
import struct
from array import array
import zlib

def receiver_driver(file_name):

    reconstruct = []
    
    file = open(file_name, 'rb')
    file_obj = file.read()
    all_packets = []
    for x in range(0 , int(round(len(file_obj)/64))):
        all_packets.append(file_obj[:64])
        file_obj = file_obj[64:]

    def data_checker(data):
        calc_crc = zlib.crc32(data)
        if(checksum == calc_crc):
            print("No Errors On Packet " + str(packet_num))
            
        else:
            print("Error Detectected On Packet " + str(packet_num))

    i = 0
    while(i < len(all_packets)):
        print(all_packets[i])
        packet_num = int.from_bytes(all_packets[i][:4], 'big')
        checksum = int.from_bytes(all_packets[i][60:], 'big')
        data = all_packets[i][4:60]
        reconstruct.append(data)
        data_checker(data)
        i += 1
    """packet_num = int.from_bytes(file_obj[:4], 'big')
    checksum = int.from_bytes(file_obj[60:], 'big')
    file_obj = file_obj[4:60]"""
    
    """def data_checker(data):
        calc_crc = zlib.crc32(data)
        if(checksum == calc_crc):
            print("No Errors On Packet " + str(packet_num))
            
        else:
            print("Error Detectected On Packet " + str(packet_num))"""

    #data_checker(data)
    open(file_name, 'w').close()
    file_w = open(file_name, 'ab')
    j = 0
    while(j < len(reconstruct)):
        file_w.write(reconstruct[j])
        j += 1

def main(file_name):
    receiver_driver(file_name)



