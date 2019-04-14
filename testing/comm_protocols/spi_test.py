import spidev
import RPi.GPIO as GPIO
import time

num_boards = 3

GPIO.setmode(GPIO.BCM)

sr_latch_pin = 13
GPIO.setup(sr_latch_pin, GPIO.OUT)

GPIO.output(sr_latch_pin, 1)

spi = spidev.SpiDev()
spi.open(1, 0)
spi.max_speed_hz = 500000 # 100 kHz
#spi.no_cs = False

xfer_list = [0, 0, 0, 0] # start frame
brightness = 0.2
brightness = int(brightness * 31)

for itr in range(0, 16*num_boards):
    xfer_list.append(224 | brightness) # 0b11100000 | brightness
    xfer_list.append(0) # b
    xfer_list.append(0) # g
    xfer_list.append(255) # r
xfer_list.append(255) # end frame byte 1
xfer_list.append(255) # end frame byte 2
xfer_list.append(255) # end frame byte 3
xfer_list.append(255) # end frame byte 4

print(xfer_list)

count = 0
#while count < 300:
while True:
    GPIO.output(sr_latch_pin, 0)
    time.sleep(0.01)
    GPIO.output(sr_latch_pin, 1)
    time.sleep(0.01)

    return_list = spi.xfer2(xfer_list)
      
#    print(return_list)
    
    print("\n list")
    for item in return_list[0:4*num_boards]:
        print("\t{:>8b}".format(int(item)))
    
    print("Count is: {}".format(count))
    
    count = count + 1
    time.sleep(0.25)

    

spi.close()

GPIO.cleanup()
