import math
import zlib
import time
import os
from pathlib import Path, PureWindowsPath


class Sender_Driver:
#def sender_driver(file_name, serialPort):

    def __init__(self, state_mach, file_name=Path(PureWindowsPath("..\\files\\out.txt")), serialPort=None):
        self.__packet_list = []
        
        self.__my_fsm = state_mach
        self.__serialPort = serialPort

        self.__file_name = file_name
        self.__file = open(self.__file_name, 'rb')
        self.__file_obj = self.__file.read()
        self.__file_size = len(self.__file_obj)
        self.__packet_num = math.ceil(self.__file_size/56)
        self.__padding_size = 56 - (self.__file_size % 56)
        self.__padding = '0' * self.__padding_size
        self.__file_obj = self.__file_obj + self.__padding.encode('utf-8')
        self.__file_data = list(zip(*[iter(self.__file_obj)]*56))

    @property
    def packet_list(self):
        return self.__packet_list

    @packet_list.setter
    def packet_list(self, data):
        self.__packet_list.append(data)

    @property
    def my_fsm(self):
        return self.__my_fsm

    @property
    def serialPort(self):
        return self.__serialPort

    @serialPort.setter
    def serialPort(self, port):
        self.__serialPort = port

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, fn):
        self.__file_name = fn

    @property
    def file(self):
        return self.__file

    @property
    def packet_num(self):
        return self.__packet_num

    @property
    def padding_size(self):
        return self.__padding_size

    @property
    def file_data(self):
        return self.__file_data

    def meta_creator(self):
        index = 0
        file_name = self.file_name
        index = index.to_bytes(4, 'big')
        param_1 = self.packet_num.to_bytes(4, 'big')
        param_2 = self.padding_size.to_bytes(1, 'big')
        # TODO: Better implementation of this
        junk, file_extension = os.path.splitext(file_name)
        param_3 = bytes(file_extension.encode('utf-8'))
        padding = b'0' * 51
        meta = index + param_1 + param_2 + param_3 + padding
        meta_crc = zlib.crc32(meta) & 0xffffffff
        meta_crc = meta_crc.to_bytes(4, 'big')
        meta = index + param_1 + param_2 + param_3 + padding + meta_crc
        self.serialPort.write(meta)
        # TODO: FSM on_event to move to Send_Data State
        self.my_fsm.on_event("")
        self.packet_loop()
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
        self.packet_list = packet
        return packet

    def packet_loop(self):
        i = 0
        while i < self.packet_num:
            out_packet = self.packet_creator(i)
            self.serialPort.write(out_packet)
            time.sleep(0.1)
            i += 1
            return out_packet
        self.my_fsm.on_event("")

        self.file.close()
        # TODO: FSM on_event to move to Wait State

    def check_finish(self):
        packet_checker = self.serialPort.read(64)
        packet_num = packet_obj[:4]
        packet_num = packet_num.decode("utf-8") 
        checksum = int.from_bytes(packet_checker[60:], 'big')
        data = packet_checker[4:60]
        crc = zlib.crc32(data) & 0xffffffff
        if crc == checksum and packet_num == "DONE":
            self.my_fsm.on_event('finish')

    def check_resend(self):
        packet_checker = self.serialPort.read(64)
        packet_num = packet_obj[:4]
        packet_num = packet_num.decode("utf-8")
        checksum = int.from_bytes(packet_checker[60:], 'big')
        data = packet_checker[4:60]
        crc = zlib.crc32(data) & 0xffffffff
        if crc == checksum and packet_num == "RESE":
            self.my_fsm.on_event('resend')
            while data:
                idx = int.from_bytes(data[:4], 'big')
                del data[:4]
                if idx == 0:
                    pass
                else:
                    packet_creator(idx-1)
                    
                
                
            
