import LCD
import time
import RPi.GPIO as GPIO

print("Hello")

temp = LCD.HD44780()
temp.message("Hello\nWorld!")
time.sleep(5)
temp.clear()
GPIO.cleanup()
