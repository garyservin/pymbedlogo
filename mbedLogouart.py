#!/usr/bin/python

import serial
import binascii

def testCommunication(mbed):
	mbed.write("\xff")
	
	response = []
	for i in range(1):
		response.append(mbed.read())
	return response


def readMemory(mbed, startAddress, bytesCount):
	
	# Copy received variables to modify them
	address = startAddress
	count = bytesCount

	# Send the read memory opcode
	mbed.write("\xfe")

	# Send the 32 bits start address (4 bytes)
	for i in range(4):
		tmp = address & 0xff
		address = address / 256
		mbed.write(chr(tmp))

	# Send how many bytes we want to read (2 bytes)
	for i in range(2):
		tmp = count & 0xff
		count = count / 256
		mbed.write(chr(tmp))

	# Read the number of bytes from the device
	response = []
	for i in range(bytesCount):
		response.append(mbed.read())
	return response

def writeMemory(mbed, destinationAddress, bytesCount, data):
	
	# Copy received variables to modify them
	address = destinationAddress
	count = bytesCount
	
	# Send the write memory opcode
	mbed.write("\xfd")

	# Send the 32 bits destination address (4 bytes)
	for i in range(4):
		tmp = address & 0xff
		address = address / 256
		mbed.write(chr(tmp))

	# Send how many bytes we want to write (2 bytes)
	for i in range(2):
		tmp = count & 0xff
		count = count / 256
		mbed.write(chr(tmp))

	# Write the data
	for i in range(len(data)):
		mbed.write(data[i])
	
	return 0
	
def writeFlash(mbed, destinationSector, destinationAddress, bytesCount, data):
	# Copy received variables to modify them
	sector = destinationSector
	address = destinationAddress
	count = bytesCount
	
	# Send the write flash opcode
	mbed.write("\xfb")

	# Send the sector to write
	mbed.write(chr(sector))
	
	# Send the 32 bits destination address (4 bytes)
	for i in range(4):
		tmp = address & 0xff
		address = address / 256
		mbed.write(chr(tmp))

	# Send how many bytes we want to write (1 byte)
	mbed.write(chr(count & 0xff))

	# Write the data
	for i in range(len(data)):
		mbed.write(data[i])
	
	return mbed.read()

def eraseFlash(mbed, sector):
	# Send the erase flash opcode
	mbed.write("\xfa")

	# Send the sector to write
	mbed.write(chr(sector))
	
	return mbed.read()


sectorFlash = 0x0E
addressFlash = 0x0000E000
addressMemory = 0x2007C000
data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

mbed = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

print "Testing communication"
print testCommunication(mbed)

## Working with Memory
print "Reading %d bytes from 0x%0X (Memory)" % (len(data),addressMemory)
print readMemory(mbed, addressMemory, len(data))

print "Writing %d bytes in 0x%0X (Memory)" % (len(data),addressMemory)
print writeMemory(mbed, addressMemory, len(data), data )

print "Reading %d bytes from 0x%0X (Memory)" % (len(data),addressMemory)
print readMemory(mbed, addressMemory, len(data))


## Working with Flash
print "Reading %d bytes from 0x%0X (FLASH)" % (len(data),addressFlash)
print readMemory(mbed, addressFlash, len(data))

print "Erasing flash"
print binascii.b2a_hex(eraseFlash(mbed, sectorFlash))

print "Writing %d bytes in 0x%0X (FLASH)" % (len(data),addressFlash)
print binascii.b2a_hex(writeFlash(mbed, sectorFlash, addressFlash, len(data), data))

print "Reading %d bytes from 0x%0X (FLASH)" % (len(data),addressFlash)
print readMemory(mbed, addressFlash, len(data))
