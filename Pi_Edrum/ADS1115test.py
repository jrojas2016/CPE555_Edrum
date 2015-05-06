'''
Script to test ADS1115 Piezo element readings.
Polls readings to define threshold for cpe555_edrum.py file
'''

from Adafruit_ADS1x15 import ADS1x15 as ads

#Setup ADS1115 through I2C
pga = 6144
sps = 8
adc = ads(ic=0x01)

while True:
	val = adc.readADCSingleEnded(0, pga, sps)
	print val