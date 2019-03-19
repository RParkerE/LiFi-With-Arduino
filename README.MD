# LiFi Communication System

## Table Of Contents
1. [Introduction](#introduction)
2. [Code Architecture](#code-architecture)
3. [GUI](#gui)
4. [State Machine](#state-machine)
    1. [Sender States](#sender-states)
    2. [Receiver States](#receiver-states)
5. [Threads](#threads)
6. [Firmware](#firmware)
7. [Hardware](#hardware)

### Introduction
The aim of this project is to design and build a demonstration product of a low cost LiFi communication system for the 
home. The system will consist of a module that encodes and modulates a digital signal into an LED transmitter/receiver 
pair through the medium of air over a reasonable distance.

### Code Architecture


### GUI
The GUI for the driver is built using TkInter. All of the functions used in constructing thr GUI are in LiFiGUI.py. For
more information on GUI development with TkInter you can look at the following:

[TkInter Documentation](https://docs.python.org/3/library/tk.html)

[TkInter Wiki](https://wiki.python.org/moin/TkInter)

[TkInter Tutorial](https://likegeeks.com/python-gui-examples-tkinter-tutorial/)


### State Machine

This state machine tracks and models the life cycle of the driver.

```
.-> Receiver ---- "SEND BUTTON PUSHED" ---> Sender
|     |   ^_________________________           |
| "DATA RECEIVED"                   |          |
|     |                             |          |
| Parse Meta                        |     Create Meta
|     |                             |          |
| Receive Data<--------------.      |      Send Data<---.
|   __|____________          |      |          |        |    
|  |               |         |      |        Wait       |
.-"NO ERROR"     "ERROR(S)"--.      |     ____|______   |
                                    |    |           |  |
                                  "DONE PACKET"   "RESEND"
```

#### Sender States
There are 4 states that are associated with the Sender driver:

##### Sender
This state initializes the driver as the sender side and pushes the state machine to the next state

##### Create_Meta
This state takes the file data and creates a 64 byte meta packet include a 4 byte index [0x00000000], 15 bytes of data
[4 bytes - number of packets, 1 byte - 0 padding at end of file, 10 bytes - file extension] + 41 bytes of 0s for 
padding, and a final 4 bytes for a crc checksukm. Once this packet is created, it is written to the serial port using 
pySerial and pushes the state machine to the next state.

##### Send_Data
This state takes the data in the file, splits it into 56 byte chunks (or less for the last packet which is padded with 
0s to make it 56 bytes) and add a 4 byte header which increases sequentially, and a 4 byte crc checksum for each 56 
byte chunk. This is looped over and each individual packet is written to the serial port using pySerial. It then pushes 
the state machine to the next state.

##### Wait
This state waits for a reply from the receiver side. If a Finish Packet is received, then it moves the state machine 
back to the Receive state. If a Resend Packet is received, then it moves the state machine back to Send_Data, and 
resends the packets with errors.


#### Receiver States

There are 3 states that are associated with the Receiver driver:

##### Receiver
This state initializes the driver as the receiver side and is the default state

##### Parse_Meta
This state reads in 64 byte, the first full packet, from the serial port using pySerial. It makes sure the index is 0 
and the crc checksum calculated with the received data and the crc checksum that was received are equal to one another.
If these checks are both true, the data is then parsed and stored. The state machine is then pushed to Receive_Data.

##### Receive Data
This state reads in 64 bytes at a time from the serial port using pySerial. This is then split into index, data, and 
checksum. If the calculated and received checksum are equal, the data is then pushed to an array at the index that 
packet corresponds to, otherwise "ERROR" is written to the array at the corresponding index. After all data is read and
has been checked, if there are no errors, the data is written to a file and the Finish Packet is sent and the state
machine is pushed to the Receiver state. Otherwise the Resend packet will be sent with up to 14 indices that had errors
and the state machine is pushed back to the Receive_Data state.

### Threads

### Firmware


### Hardware
