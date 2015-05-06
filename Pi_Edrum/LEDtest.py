'''
Quick script to test correct functionality of LEDs. 
Light up each LED in a loop.
'''
import RPi.GPIO as GPIO
import time

#LED Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

while True:
	GPIO.output(11, True)
	time.sleep(0.5)
	GPIO.output(11, False)
	GPIO.output(13, True)
	time.sleep(0.5)	
	GPIO.output(13, False)
	GPIO.output(15, True)
	time.sleep(0.5)
	GPIO.output(15, False)