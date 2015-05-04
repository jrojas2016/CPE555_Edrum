'''
#CPE555 Raspberry Pi Project
#Title: Any-Surface Electronic Drum Kit
#by: Jorge Rojas

Description:
        Electronic drum kit triggered by vibration sensors going through ADS1115 ADC.
The LED's color and a sound are mapped to each vibration sensor as follows:
        -Channel 0 -> Red LED, Snare 
        -Channel 1 -> Blue LED, HiHat 
        -Channel 2 -> Green LED, Kick ... optional
        -Channel 3 -> Purple LED, Tom  ... optional

References:
'''

import sys
import time as t
#import thread as th     #used to parallelize each channel on the ADS1115
import signal as s
import pygame as pyg
import RPi.GPIO as GPIO
from Adafruit_ADS1x15 import ADS1x15 as ads

########################## SETUP & DECLARATIONS ########################################

#LED Pin Mappings
RED_LED = 11
BLUE_LED = 13
GREEN_LED = 15

#Piezo trigger threshold
piezo_threshold = 50

#LED GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

#ADS1115 Input Setup
def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)

s.signal(s.SIGINT, signal_handler)
ADS1115 = 0x01  #16-bit ADC
adc_gain = 4096 #+/- 4.096V
adc_sps = 860       #860 samples per second
adc = ads(ic=ADS1115)

#Audio setup
pyg.mixer.init()

########################## FUNTION DEFINITIONS ########################################
def blink(pin, delay):
        '''
        Blink function to use when vibration sensor is triggered.
        Input LED pin number and delay in seconds
        '''
        GPIO.output(pin, True)
        t.sleep(delay)
        GPIO.output(pin, False)
        t.sleep(delay)

def playDrum(drum_type):
        '''
        Play appropriate drum style based on drum type
        Drum Types(index): snare, kick, hihat, tom
        '''
        if drum_type == 'snare':
                pyg.mixer.music.load('s12.wav')
        elif drum_type == 'kick':
                pyg.mixer.music.load('k4.wav')
        elif drum_type == 'hihat':
                pyg.mixer.music.load('hh2open.wav')
        elif drum_type == 'tom':
                pyg.mixer.music.load('ta1.wav')
        pyg.mixer.music.play()
        while pyg.mixer.music.get_busy() == True:
                continue

def getPiezoValue(channel):
        '''
        Fetch the value from the ADS1115 ADC at the given channel.
        Channels: 0, 1, 2, 3
        '''
        if channel == 0:
                ch_value = adc.readADCSingleEnded(channel, adc_gain, adc_sps)
        elif channel == 1:
                ch_value = adc.readADCSingleEnded(channel, adc_gain, adc_sps)
        #NOT ENOUGH PIEZO ELEMENTS TO IMPLEMENT. UNCOMMENT TU USE ALL 4 CHANNELS OF ADS1115
        # elif channel == 2:
        #         ch_value = adc.readADCSingleEnded(channel, adc_gain, adc_sps)
        # elif channel == 3:
        #         ch_value = adc.readADCSingleEnded(channel, adc_gain, adc_sps)
        else:
                ch_value = 0    #Default case
        return ch_value

def sensorTriggered(channel, drum_type, pin, delay):
        '''
        Implemented as whole funtion to ease multithreading process.
        Checks if the vibration sensor at appropriate channel was triggered 
        and performs necessary actions. 
        '''
        ch_value = getPiezoValue(channel)
        print ch_value

        if ch_value > piezo_threshold:
                playDrum(drum_type)
                blink(pin, delay)
                

########################## MAIN PROGRAM ################################################

if __name__ == '__main__':
        #channel_values = []     #channel values

        while(True):

                sensorTriggered(0, 'snare', RED_LED, 0.25)
                sensorTriggered(1, 'hihat', BLUE_LED, 0.25)

                #TODO: Implement Threading for delay issue
                #try:
                        #th.start_new_thread(sensorTriggered, (0, 'snare', RED_LED, 0.25))
                        #th.start_new_thread(sensorTriggered, (1, 'hihat', BLUE_LED, 0.25))
                #except:
                        #print "Error: unable to start thread"


                #CODE FOR SENSOR TRIGGER WITHOUT THREADING
                # channel_values[0] = getPiezoValue(0)
                # channel_values[1] = getPiezoValue(1)
                # if channel_values[0] > piezo_threshold:
                #         #Play Snare sound and turn on red LED
                #         blink(RED_LED, 0.25)
                #         playDrum('snare', '1')
                # if channel_values[1] > piezo_threshold:
                #         #Play hihat sound and turn on blue LED
                #         blink(RED_LED, 0.25)
                #         playDrum('hihat', '1')

                #CAN CAUSE TIMING COMPLICATIONS IN PROGRAM
                # for i, channel in enumerate(channels.keys()):
                #         channel_values[i] = getPiezoValue(channels[channel][0])
                #         if channel_values[i] > piezo_threshold:
                #                 blink(channels[channel][2], 0.25)
                #                 playDrum(channels[channel][1], '1')


