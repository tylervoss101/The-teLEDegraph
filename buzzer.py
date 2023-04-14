# Import required libraries
import sys
import RPi.GPIO as GPIO
import time

# Set trigger PIN according with your cabling
buzzerPIN = 17

# Set PIN to output
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPIN,GPIO.OUT)

# define PWM signal and start it on trigger PIN
#buzzer = GPIO.PWM(buzzerPIN, 490)
state = 'dash'
buzzer = GPIO.PWM(buzzerPIN, 490)
def buzz(type):
    buzzer.ChangeFrequency(490)
    if type == 'dot':
        buzzer.start(10) 
        time.sleep(.1)
        buzzer.stop()
        time.sleep(.3)
    elif type == 'dash':
        buzzer.start(10)
        time.sleep(.45)
        buzzer.stop()
        time.sleep(.3)

# cleanup will free PINS and exit will terminate code execution



GPIO.cleanup()
sys.exit()

# Please find below some addictional commands to change frequency and
# dutycycle without stopping buzzer, or to stop buzzer:
#
# buzzer.ChangeDutyCycle(10)
# buzzer.ChangeFrequency(1000)
# buzzer.stop()
