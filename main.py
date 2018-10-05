# Zach Cotter, Clayton Howeth
# Capstone Project: Pie Decider

import numpy as np
import random as rand
import smbus 
import time
import spidev
import AccelerometerClass as Accl
import RPi.GPIO as GPIO
import LCD

GPIO.cleanup()

# define button pin
button1=18

# define buzzer pin
buzzerPin=26

myArray=[]
lcd = LCD.HD44780()
foodArray=[]
pitch=500
duration=.2
pitches=[]
durations=[]
song=[]

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)

    for i in range(cycles):
        GPIO.output(buzzerPin, True)
        time.sleep(delay)
        GPIO.output(buzzerPin, False)
        time.sleep(delay)

    time.sleep(duration * 0.2)

def getTune():
    data=np.loadtxt("tune.txt")
    pitches=np.int_(data[:,0])
    durations=np.float_(data[:,1])
    l=len(pitches)

    for i in range (0,(l-2)):
        buzz(pitches[i],durations[i])
        time.sleep(.2)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(buzzerPin,GPIO.OUT)

    # Get I2C bus - initial bus to channel 1 for accelerometer
    bus = smbus.SMBus(1)

    # read in food list
    with open('foodList.txt') as food:
        for line in food:
            food = foodArray.append(line)

def welcome():
    print("Hello")
    lcd.message("Hello\nWorld!")
    time.sleep(5)
    lcd.clear()
    
    

def do8ball(ev=None):
    try:
        lcd.clear()
        time.sleep(0.2)
        lcd.message("Shake to decide\nwhere to eat!")
        time.sleep(5)
        i=0
        bus = smbus.SMBus(1) 
        newData=Accl.Accelerometer()
        while (newData.change()):
            x = 0
            print(i)
            i+=1
            #Parameters for write_byte_data
            #1. Address of the device
            #2. Communication data - active mode control register
            #3. Our data - 0 (standby mode) or 1 (active)
            bus.write_byte_data(0x1D, 0x2A, 1) 
            time.sleep(0.5)

            #Read from the status register, real-time status register 0x00
            #Data returned will be an array
            #Contents of 7 bytes read and stored in data array represent:
            #status (ignore), MSBx, LSBx, MSBy, LSBy, MSBz, LSBz
            data = bus.read_i2c_block_data(0x1D, 0x00, 7)     

            MSB_x=data[1]
            LSB_x=data[2]
            numberOfBits=16

            xAccl=(MSB_x*256+LSB_x)/numberOfBits
            if xAccl>2047:
                xAccl-=4096

            #put register in standbye mode
            bus.write_byte_data(0x1D, 0x2A, 0) 
            time.sleep(0.2)

            #print(data)
            
            #read in data and convert to realistic values
            newData=Accl.Accelerometer(data[2], data[4], data[6])
            #newData.printCoord()
            myArray.append(newData)
        
        x=rand.randint(0,len(foodArray))
        print(foodArray[x])
        
        lcd.clear()
        time.sleep(0.2)
        lcd.message(foodArray[x])
        time.pause(5)

    #capture the control c and exit cleanly
    except(KeyboardInterrupt, SystemExit): 
        print("User requested exit... bye!")

    for accl in myArray:
        accl.printCoord()

def loop():
    GPIO.add_event_detect(button1, GPIO.FALLING, callback=do8ball, bouncetime=2000)
    try:
        while True:
            time.sleep(.01)

        #capture the control c and exit cleanly
    except(KeyboardInterrupt, SystemExit): 
        print("User requested exit... bye!")
        GPIO.cleanup()

setup()
getTune()
welcome()
loop()




        
        

