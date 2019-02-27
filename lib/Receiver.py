import zlib


def receiver_driver(file_name, serialPort):

    packet_list = []

    file = open(file_name, "wb")
    file.write()
    file.close()
    file = open(file_name, "ab")
    
    def data_checker(data, packet_num):
        calc_crc = zlib.crc32(data)
        if (checksum == calc_crc) or (checksum + 1 == calc_crc) or (checksum - 1 == calc_crc):
            packet_list[packet_num - 1] = data
            file.write(data)
        else:
            packet_list[packet_num - 1] = "ERROR"
            
    packet_obj = serialPort.read(64)

    while packet_obj != b'':
        packet_num = int.from_bytes(packet_obj[:4], 'big')
        checksum = int.from_bytes(packet_obj[60:], 'big')
        payload = packet_obj[4:60]
        data_checker(payload, packet_num)
        packet_obj = serialPort.read(64)

    file.close()
