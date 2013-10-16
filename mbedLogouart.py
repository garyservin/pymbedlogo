#!/usr/bin/python

import serial

eSector = 0x0e
e = 0xe000
g = 0x2007c000

def read(mbed, count):
    """Reads count number of bytes from the mbed
    
    Args:
        mbed: mbed serial device
        count: number of bytes to read

    """
    if count == 1:
	return ord(mbed.read())
    else:
        response = []
        for i in range(count):
            response.append(ord(mbed.read()))
        return response

def write(mbed, data):
    """Writes one byte to the mbed
    
    Args:
        mbed: mbed serial device
        data: byte to be sent

    """
    mbed.write(chr(data & 0xff))

def write16(mbed, data):
    """Writes two bytes to the mbed
    
    Args:
        mbed: mbed serial device
        data: bytes to be sent

    """
    for i in range(2):
        mbed.write(chr(data & 0xff))
        data = data / 256

def write32(mbed, data):
    """Writes three bytes to the mbed
    
    Args:
        mbed: mbed serial device
        data: bytes to be sent

    """
    for i in range(4):
        mbed.write(chr(data & 0xff))
        data = data / 256

def testCommunication(mbed):
    """Tests the communication with the mbed
    
    Args:
        mbed: mbed serial device
    Returns:
        interger number 23

    """
    write(mbed, 0xff)
    return read(mbed, 1)

def readMemory(mbed, address, count):
    """Reads count bytes from memory starting at address
    
    Args:
        mbed:     mbed serial device
	address:  start address to read
	count:    number of bytes
    Returns:
        a list with the readings

    """
    write(mbed, 0xfe)		# Send the read memory opcode
    write32(mbed, address)	# Send the 32 bits start address (4 bytes)
    write16(mbed, count)	# Send how many bytes we want to read (2 bytes)
    return read(mbed, count)	# Read the number of bytes from the device

def writeMemory(mbed, address, count, data):
    """Writes count bytes to the RAM memory starting at address 
    
    Args:
        mbed:     mbed serial device
	address:  start address to write
	count:    number of bytes
        data:     list of bytes
    Returns:
        a number 0

    """
    write(mbed, 0xfd)		# Send the write memory opcode
    write32(mbed, address)	# Send the 32 bits destination address (4 bytes)
    write16(mbed, count)	# Send how many bytes we want to write (2 bytes)
    for i in range(len(data)):	# Write data
        write(mbed, data[i])
    return 0
	
def writeFlash(mbed, sector, address, count, data):
    """Writes count bytes to the FLASH memory starting at address in sector 
    
    Args:
        mbed:     mbed serial device
	sector:   sector of the FLASH memory
	address:  start address to write
	count:    number of bytes
        data:     list of bytes
    Returns:
        zero if the write was sucesfull

    """
    write(mbed, 0xfb)		# Send the write flash opcode
    write(mbed, sector)		# Send the sector to write
    write32(mbed, address)	# Send the 32 bits destination address (4 bytes)
    write(mbed, count)		# Send how many bytes we want to write (1 byte)
    for i in range(len(data)):	# Write data
        write(mbed, data[i])
    return read(mbed, 1)

def eraseFlash(mbed, sector):
    """Erases flash address at sector
    
    Args:
        mbed:     mbed serial device
	sector:   sector of the FLASH memory
    Returns:
        zero if the erase was sucesfull

    """
    write(mbed, 0xfa)		# Send the erase flash opcode
    write(mbed, sector)		# Send the sector to write
    return read(mbed, 1)

def runCommand(mbed, command):
    """Writes compiled Logo command to the FLASH memory and runs it
    
    Args:
        mbed:     mbed serial device
	command:  list with compiled Logo command 

    """
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
