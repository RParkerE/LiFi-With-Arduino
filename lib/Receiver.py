import zlib


class Receiver_Driver:
#def receiver_driver(file_name, serialPort):

    def __init__(self, file_name, serialPort):
        self.__packet_list = []

        self.__serialPort = serialPort

        self.__file = open(file_name, "wb")
        self.__file.write()
        self.__file.close()
        self.__file = open(file_name, "ab")

    @property
    def packet_list(self):
        return self.__packet_list

    @packet_list.setter
    def packet_list(self, data):
        return self.__packet_list.append(data)

    @property
    def serialPort(self):
        return self.__serialPort

    @property
    def file(self):
        return self.__file

    def data_checker(self, data, packet_num, checksum):
        calc_crc = zlib.crc32(data)
        if (checksum == calc_crc) or (checksum + 1 == calc_crc) or (checksum - 1 == calc_crc):
            self.packet_list = data
            self.file.write(data)
        else:
            self.packet_list = "ERROR"
            
    def data_loop(self):
        packet_obj = self.serialPort.read(64)

        while packet_obj != b'':
            packet_num = int.from_bytes(packet_obj[:4], 'big')
            checksum = int.from_bytes(packet_obj[60:], 'big')
            payload = packet_obj[4:60]
            self.data_checker(payload, packet_num, checksum)
            packet_obj = self.serialPort.read(64)

        self.file.close()
