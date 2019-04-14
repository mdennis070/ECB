# i2cdetect -y 1
# ls /dev/*i2c*


import smbus
import time

# slave device address 0x64
address = 0x64

# Initialize I2C (SMBus)
bus = smbus.SMBus(1)

def writeNumber(reg, value):
    bus.write_byte_data(address, int(reg), int(value))
    return -1

def readNumber(data):
    number = bus.read_byte_data(address, int(data))
    print(bin(number))
    return number

while True:
    #data = input("Enter the data to be sent: ")
    #data_list = list(data)
    #for i in data_list:
    #    writeNumber(int(ord(i)))
    #    time.sleep(.1)
    data = input("Enter register to read: ")
    readNumber(data)
    send_reg = input("Enter the reg to send to: ")
    send_data = input("Enter the data to send: ")
    writeNumber(send_reg, send_data)
    #writeNumber(int(0x0A))
