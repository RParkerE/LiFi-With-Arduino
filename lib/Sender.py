import math
import zlib
import time
import os


class Sender_Driver:
#def sender_driver(file_name, serialPort):

    def __init__(self, file_name, serialPort):
        self.packet_list = []

        self.serialPort = serialPort

        self.file = open(file_name, 'rb')
        self.file_obj = self.file.read()
        self.file_size = len(self.file_obj)
        self.packet_num = math.ceil(self.file_size/56)
        self.padding_size = 56 - (self.file_size % 56)
        self.padding = '0' * self.padding_size
        self.file_obj = self.file_obj + self.padding.encode('utf-8')
        self.file_data = list(zip(*[iter(self.file_obj)]*56))

    def meta_creator(self):
        index = 0
        index = index.to_bytes(4, 'big')
        param_1 = self.packet_num.to_bytes(4, 'big')
        param_2 = self.padding_size.to_bytes(1, 'big')
        # TODO: Better implementation of this
        junk, file_extension = os.path.splitext(self.file.name)
        param_3 = bytes(file_extension.encode('utf-8'))
        padding = b'0' * 51
        meta = index + param_1 + param_2 + param_3 + padding
        meta_crc = zlib.crc32(meta) & 0xffffffff
        meta_crc = meta_crc.to_bytes(4, 'big')
        meta = index + param_1 + param_2 + param_3 + padding + meta_crc
        return meta
        
        

    # Packet Creator adding 4 bytes index to 48 bytes of data
    def packet_creator(self, counter):
        data = self.file_data[0][counter]
        data_byte = bytes(data)
        counter += 1
        index = counter.to_bytes(4, 'big')
        data_crc = zlib.crc32(data_byte) & 0xffffffff
        data_crc = data_crc.to_bytes(4, 'big')
        packet = index + data_byte + data_crc
        self.packet_list.append(packet)
        return packet


    def packet_loop(self):
        i = 0
        while i < self.packet_num:
            out_packet = self.packet_creator(i)
            #self.serialPort.write(out_packet)
            time.sleep(0.1)
            i += 1
            return out_packet

        self.file.close()
    def get_file_size(self):
        return self.file_size
        
        
