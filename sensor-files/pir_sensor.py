import RPi.GPIO as GPIO
import time

# PIR sensor GPIO pinn
PIR_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def motion_detected():
    return GPIO.input(PIR_PIN) == 1
#    if GPIO.input(PIR_PIN) == 1:
#        start = time.time()
#        while time.time() - start < 1.0:
#            if GPIO.input(PIR_PIN) == 0:
#                return False
#            return True
#        return False

