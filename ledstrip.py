'''
CS326 the teLEDgraph
Authors: Justin Voss and Tyler Voss
LED strip morse code communicator over MQTT.
'''
import sys
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import sys
import cv2
#RASPBERRI PI IMPORTS
#include all neccessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel
from rpi_ws281x import *
import argparse
from threading import Thread
from morse import *
#from buzzer import buzz
from gpiozero import Buzzer
from time import sleep

LED_COUNT      = 60     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Constants
PORT = 8883
QOS = 0
LED = 16
DELAY = 2.0
CERTS = '/etc/ssl/certs/ca-certificates.crt'

# Set hostname for MQTT broker
BROKER = 'iot.cs.calvin.edu'

# Note: these constants must be set for broker authentication
USERNAME = 'XXXXX'   # broker authentication username
PASSWORD = 'XXXXX'   # broker authentication password

#Initialise a strips variable, provide the GPIO Data Pin
#utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
pixels1 = neopixel.NeoPixel(board.D18, 60, brightness=1) #this is strip

#GPIO Port, How many nodes on LED strip, brightness
#Also create an arbitary count variable
x=0

#SET UP BUZZER
buzzerPIN = 17
# Set PIN to output
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPIN,GPIO.OUT)
# define PWM signal and start it on trigger PIN
buzzer = GPIO.PWM(buzzerPIN, 490)

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

#buzzer = Buzzer(17)
color = (0,255,0)
color2 = (255,255,0)


def buzz(type):
    ''' Return a long or short buzz based on dot or dash
    '''
    buzzer.ChangeFrequency(495)
    if type == 'dot':
        buzzer.start(10) 
        time.sleep(.1)
        buzzer.stop()
        time.sleep(.005)
    elif type == 'dash':
        buzzer.ChangeFrequency(400)
        buzzer.start(10)
        time.sleep(.3)
        buzzer.stop()
        time.sleep(.0005)
        
def on_publish(client, userdata, mid):
    ''' Callback when an MQTT message is published
    '''
    print("MQTT data published")

def on_connect(client, userdata, flags, rc):
    ''' Callback when connecting to the MQTT broker
    '''
    if rc==0:
        print(f'Connected to {BROKER}')
    else:
        print(f'Connection to {BROKER} failed. Return code={rc}')
        sys.exit(1)        

def on_message(client, data, msg):
    ''' Callback when client receives a PUBLISH message from the broker
    '''    
    if msg.topic == 'thv4/LED':
        print(f'Received message: LED = {msg.payload}')
        if int(msg.payload) == 1:
            # Turn on LED strip
            pixels1.fill((127, 127, 127))
        elif int(msg.payload) == 0:
            #Returns all LED to off
            pixels1.fill((0, 0, 0))
        elif int(msg.payload) == 2:
           colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        elif int(msg.payload) == 3:
            rainbow(strip) # rainbow

        elif int(msg.payload) == 11: # red color
            pixels1.fill((255, 0, 0))
        elif int(msg.payload) == 12: # orange color
            pixels1.fill((255, 74, 0))
        elif int(msg.payload) == 13: # yellow color
            pixels1.fill((255, 255, 0))
        elif int(msg.payload) == 14: # green color
            pixels1.fill((0, 255, 0))
        elif int(msg.payload) == 15: # blue color
            pixels1.fill((0, 0, 255))
        elif int(msg.payload) == 16: # purple color
            pixels1.fill((148, 0, 255))
        elif int(msg.payload) == 17: # white color
            pixels1.fill((127, 127, 127))
        else:
            pixels1.fill((0,0,0))
    elif msg.topic =='thv4/LEDMessage':
        print(f'Received message: LED = {msg.payload}')
        newMessage = msg.payload.decode('utf-8')
        print(newMessage)
        print(encrypt(newMessage))     
        led_morse(encrypt((newMessage)))   # from Morse.py, uses the function to encrypt the message.
        print(color)
        


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    i = 0
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
def colorDot(strip):
     #Focusing on a particular strip, use the command Fill to make it all a single colour
    #based on decimal code R, G, B. Number can be anything from 255 - 0.     
    for i in range(30):
        pixels1[i] = (255,0,0)
        # strip.setPixelColor(i, color)
        time.sleep(.005)
        pixels1[i] = (0, 0, 0)
        

def colorDash(strip):
     #Focusing on a particular strip, use the command Fill to make it all a single colour
    #based on decimal code R, G, B. Number can be anything from 255 - 0.       
    for i in range(40):
        pixels1[i] = (0,255,0)
        if i < 50:
            pixels1[i+9] = (0,255,0)
        time.sleep(.0005)
        pixels1[i] = (0, 0, 0)
        
def led_morse(message):
    for character in message:
        if character == '-':   # if the letter is a dash, do the dash animation on the LED strip
            colorDash(strip)
            buzz('dash')
        elif character == '.':   # if the letter is a dot, do the dot animation on the LED strip
            colorDot(strip)
            buzz('dot')  
        else: 
            pixels1.fill((0, 0, 0))
            time.sleep(1)

#EXTRA FUN FUNCTIONS
# Help from Tony DiCola (tony@tonydicola.com) on GitHub
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
    
def rainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
    

# Setup MQTT client and callbacks
client = mqtt.Client()
client.username_pw_set(USERNAME,password=PASSWORD) # remove for anonymous access
client.tls_set(CERTS)
client.on_connect = on_connect
client.on_message = on_message
# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("thv4/LED", qos=QOS)
client.subscribe("thv4/LEDMessage", qos=QOS)
client.loop_start()


try:
    while True:
        client.publish('jcalvin/motion', '1')
        time.sleep(DELAY)

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    print('Done')


