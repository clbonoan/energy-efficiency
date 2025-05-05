# main code for day 3 testing (PIR sensor only)

import time
from bulb_control import turn_on, turn_off
from pir_sensor import motion_detected

# track states
light_on = False
last_motion_time = 0

# thresholds
MOTION_TIMEOUT = 10

while True:
    now = time.time()
    motion = motion_detected()  # true if motion detected
    
    if motion:
        print("Motion detected")
        last_motion_time = now
        if not light_on:
            print("Turning bulb ON")
            turn_on()
            light_on = True

    elif light_on and (now - last_motion_time > MOTION_TIMEOUT):
        print("Turning bulb OFF")
        turn_off()
        light_off = False

    time.sleep(1)


