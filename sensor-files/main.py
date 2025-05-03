import time
from bulb_control import turn_on, turn_off
from pir_sensor import motion_detected
from mmwave_sensor import is_far

# track light state to avoid repeated MQTT calls
light_on = False
#motion_timer = 0
#MOTION_TIMEOUT = 3

while True:
    motion = motion_detected()
    far = is_far()
    
    #current_time = time.time()

    if motion:
        #motion_timer = current_time

        if far:
            if not light_on:
                # entering the room
                turn_on()
                light_on = True
        elif not far:
            if light_on:
                # exiting the room
                turn_off()
                light_on = False
    
    #else:
        # no motion
        # only turn off if user has exited and is no longer detected
    #    if (current_time - motion_timer > MOTION_TIMEOUT) and not far:
    #        if light_on:
    #            turn_off()
    #            light_on = False



