import RPi.GPIO as GPIO
import time

# PIR sensor GPIO pinn
PIR_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def motion_detected():
    return GPIO.input(PIR_PIN) == 1

