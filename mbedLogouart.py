#!/usr/bin/python

import serial

eSector = 0x0e
e = 0xe000
g = 0x2007c000

def read(mbed, count):
    if count == 1:
	return ord(mbed.read())
    else:
        response = []
        for i in range(count):
            response.append(ord(mbed.read()))
        return response

def write(mbed, data):
    mbed.write(chr(data & 0xff))

def write16(mbed, data):
    for i in range(2):
        mbed.write(chr(data & 0xff))
        data = data / 256

def write32(mbed, data):
    for i in range(4):
        mbed.write(chr(data & 0xff))
        data = data / 256

def testCommunication(mbed):
    write(mbed, 0xff)
    return read(mbed, 1)

def readMemory(mbed, address, count):
    write(mbed, 0xfe)		# Send the read memory opcode
    write32(mbed, address)	# Send the 32 bits start address (4 bytes)
    write16(mbed, count)	# Send how many bytes we want to read (2 bytes)
    return read(mbed, count)	# Read the number of bytes from the device

def writeMemory(mbed, address, count, data):
    write(mbed, 0xfd)		# Send the write memory opcode
    write32(mbed, address)	# Send the 32 bits destination address (4 bytes)
    write16(mbed, count)	# Send how many bytes we want to write (2 bytes)
    for i in range(len(data)):	# Write data
        write(mbed, data[i])
    return 0
	
def writeFlash(mbed, sector, address, count, data):
    write(mbed, 0xfb)		# Send the write flash opcode
    write(mbed, sector)		# Send the sector to write
    write32(mbed, address)	# Send the 32 bits destination address (4 bytes)
    write(mbed, count)		# Send how many bytes we want to write (1 byte)
    for i in range(len(data)):	# Write data
        write(mbed, data[i])
    return read(mbed, 1)

def eraseFlash(mbed, sector):
    write(mbed, 0xfa)		# Send the erase flash opcode
    write(mbed, sector)		# Send the sector to write
    return read(mbed, 1)

def runCommand(mbed, command):
    eraseFlash(mbed, eSector)	# Erase flash sector
    writeFlash(mbed, eSector, e, len(command), command)	# Write command to flash
    write(mbed, 0xfc)		# Send the run opcode

data = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]

mbed = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

print "Testing communication...",
print testCommunication(mbed)

### Working with Memory
#print "Reading %d bytes from 0x%0X (Memory)" % (len(data), g)
#print readMemory(mbed, g, len(data))
#print ' '
#
#print "Writing %d bytes in 0x%0X (Memory)" % (len(data), g)
#print writeMemory(mbed, g, len(data), data )
#print ' '
#
#print "Reading %d bytes from 0x%0X (Memory)" % (len(data), g)
#print readMemory(mbed, g, len(data))
#print ' '
#
#print ' '
### Working with Flash
#print "Reading %d bytes from 0x%0X (FLASH)" % (len(data), e)
#print readMemory(mbed, e, len(data))
#print ' '
#
#print "Erasing flash"
#print eraseFlash(mbed, eSector)
#print ' '
#
#print "Writing %d bytes in 0x%0X (FLASH)" % (len(data), e)
#print writeFlash(mbed, eSector, e, len(data), data)
#print ' '
#
#print "Reading %d bytes from 0x%0X (FLASH)" % (len(data), e)
#print readMemory(mbed, e, len(data))

command1 = [1, 45, 10, 9, 0]
runCommand(mbed, command1)
print read(mbed, 4)

command2 = [1, 4, 3, 5, 0, 1, 12, 10, 9, 4, 17, 0]
runCommand(mbed, command2)
print read(mbed, 13)
