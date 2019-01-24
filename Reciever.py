from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Other Imports
import serial
import sys
import numpy
import struct
from array import array
Tk().withdraw()

key = "1001"


file_name = askopenfilename()
file = open(file_name, 'rb')
file_obj = file.read()
packet_num = int.from_bytes(file_obj[:3], 'big')
file_obj = file_obj[3:]



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
   
# Function used at the receiver side to decode  
# data received by sender 
def decodeData(data, key): 
   
    l_key = len(key) 
   
    # Appends n-1 zeroes at end of data 
    appended_data = data + '0'*(l_key-1) 
    remainder = mod2div(appended_data, key) 
   
    return remainder 

out = decodeData(file_obj.decode('utf-8'), key)

if out == '000':
    print('No Errors Detected')
else:
    print('Error Detected at ' + str(packet_num))



