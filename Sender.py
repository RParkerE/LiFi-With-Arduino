from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Other Imports
import serial
import sys
import math
import numpy
import struct
from array import array

Tk().withdraw()

count = 0
key = "1001" 

file_name = askopenfilename()
file = open(file_name, 'rb')
file_obj = file.read()
file_size = len(file_obj)
packet_num = math.ceil(file_size/60)
padding_size = 60 - (file_size % 60)
padding = '0' * padding_size
file_obj = file_obj + padding.encode('utf-8')
file_data = list(zip(*[iter(file_obj)]*60))

#parity check function for any byte

'''
def parity_brute_force(x):
    bit = 0
    num_bits = 0
    while x:
        bitmask = 1 << bit
        bit += 1
        if x & bytes(bitmask):
            num_bits += 1
        x &= ~bytes(bitmask)
    return num_bits % 2
'''

#packet Creater adding 3 bytes index to 48 bytes of data
def packet_creater(counter):
    data = file_data[counter]
    dataByte = bytes(data)
    counter += 1
    index = counter.to_bytes(3, 'big')
    strData = str(dataByte.decode('utf-8'))
    codedData = encodeData(strData,key).encode('utf-8')
    packet = index + codedData
    return packet
    
   
#CRC for error detection
def xor(a, b): 
   
    # initialize result 
    result = [] 
   
    # Traverse all bits, if bits are 
    # same, then XOR is 0, else 1 
    for i in range(1, len(b)): 
        if a[i] == b[i]: 
            result.append('0') 
        else: 
            result.append('1') 
   
    return ''.join(result) 
   
   
# Performs Modulo-2 division 
def mod2div(divident, divisor): 
   
    # Number of bits to be XORed at a time. 
    pick = len(divisor) 
   
    # Slicing the divident to appropriate 
    # length for particular step 
    tmp = divident[0 : pick] 
   
    while pick < len(divident): 
   
        if tmp[0] == '1': 
   
            # replace the divident by the result 
            # of XOR and pull 1 bit down 
            tmp = xor(divisor, tmp) + divident[pick] 
   
        else:   # If leftmost bit is '0' 
  
            # If the leftmost bit of the dividend (or the 
            # part used in each step) is 0, the step cannot 
            # use the regular divisor; we need to use an 
            # all-0s divisor. 
            tmp = xor('0'*pick, tmp) + divident[pick] 
   
        # increment pick to move further 
        pick += 1
   
    # For the last n bits, we have to carry it out 
    # normally as increased value of pick will cause 
    # Index Out of Bounds. 
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
   
    checkword = tmp 
    return checkword 
   
# Function used at the sender side to encode 
# data by appending remainder of modular divison 
# at the end of data. 
def encodeData(data, key): 
   
    l_key = len(key) 
   
    # Appends n-1 zeroes at end of data 
    appended_data = data + '0'*(l_key-1) 
    remainder = mod2div(appended_data, key) 
   
    # Append remainder in the original data 
    codeword = data + remainder 
    return codeword     


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



    
