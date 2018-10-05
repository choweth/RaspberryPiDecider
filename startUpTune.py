# Start up tune

#import libraries
import numpy as np
import time
import spidev
import RPi.GPIO as GPIO


buzzerPin=26
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin,GPIO.OUT)

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
        

try:
    getTune()

except(KeyboardInterrupt,SystemExit):
    print("User requested exit... shutting down now")
finally:
    GPIO.cleanup()
