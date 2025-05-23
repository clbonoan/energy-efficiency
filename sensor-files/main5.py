# main code for day 5 testing (PIR, mmWave, light lux sensor)

import time
from bulb_control import turn_on, turn_off, set_bulb_brightness
from pir_sensor import motion_detected
from mmwave_sensor import get_mmwave_distance
from light_sensor import read_lux, calculate_brightness

# track states
light_on = False
startup_checked = False
last_motion_time = 0
last_distance = None
last_distance_time = 0
exit_time = 0

# thresholds
WINDOW_EXIT = 3  # seconds allowed between distance and motion check
WINDOW_ENTRY = 5  # seconds allowed between motion and distance check
DISTANCE_THRESHOLD = 80  # in cm
EXIT_COOLDOWN = 5   # seconds to suppress mmWave readings after exit

while True:
    now = time.time()
    motion = motion_detected()  # true if motion detected
    distance_cm = get_mmwave_distance()
    lux = read_lux()
    
    if distance_cm is None:
        continue

    # debug
    print(f"Motion: {motion} | Distance: {distance_cm} cm | Lux: {lux:.2f} | Bulb: {light_on}")
    print("")

    # --- suppress distance after exit ---
    if not light_on and (now - exit_time < EXIT_COOLDOWN):
        print("Suppressing mmWave after exit")
        last_distance = 0
        last_distance_time = 0
    elif distance_cm is not None:
        last_distance = distance_cm
        last_distance_time = now
    
    # track last distance timestamp
    if distance_cm is not None:
        last_distance = distance_cm
        last_distance_time = now

    # track last motion timestamp
    if motion:
        last_motion_time = now

    # --- STARTUP: already in room (far) ---
    if not startup_checked and not light_on and distance_cm > DISTANCE_THRESHOLD:
        print("Startup: already in room  -> TURN ON")
        lux = read_lux()
        brightness = calculate_brightness(lux)
        if brightness > 0:
            print(f"Lux = {lux:.2f} -> Setting brightness to {brightness}")
            set_bulb_brightness(brightness)
            light_on = True
        else:
            print(f"Lux = {lux:.2f} -> Room too bright -> LIGHT STAYS OFF")
            #turn_on()
        #light_on = True
        startup_checked = True
        continue

    # --- EXIT: distance < 100 cm then motion within 3 seconds ---
    if (
        light_on and 
        (0 < last_distance_time - last_motion_time < WINDOW_EXIT) and 
        last_distance < DISTANCE_THRESHOLD
    ):    
        print("Exiting detected -> TURN OFF")
        turn_off()
        light_on = False
        exit_time = now  # start suppression window
        continue

    # --- ENTRY: motion then distance > 100 cm within 5 seconds ---
    if (
        not light_on and
        (now - exit_time > EXIT_COOLDOWN) and
        (0 < last_distance_time - last_motion_time < WINDOW_ENTRY) and 
        last_distance > DISTANCE_THRESHOLD
    ):
        print("Entering detected -> TURN ON")
        lux = read_lux()
        brightness = calculate_brightness(lux)
        if brightness > 0:
            print(f"Lux = {lux:.2f} -> Setting brightness to {brightness}")
            set_bulb_brightness(brightness)
            light_on = True
        else:
            print(f"Lux = {lux:.2f} -> Room is bright -> NO LIGHT NEEDED")
            #light_on = False
        #else:
        #    print("Too early -> KEEP LIGHT OFF")
        #    light_on = False
        continue
    
    # --- DIMMING: while user is still present ---
    if light_on and distance_cm > DISTANCE_THRESHOLD:
        lux = read_lux()
        brightness = calculate_brightness(lux)
        if brightness > 0:
            print(f"Adjusting brightness to {brightness} (lux = {lux:.2f})")
            set_bulb_brightness(brightness)
        else:
            print(f"Lux = {lux:.2f}) -> Room now bright -> TURNING OFF")
            turn_off()
            light_on = False
    
    # --- BLOCK entry logic during cooldown ---
    if not light_on and (now - exit_time <= EXIT_COOLDOWN):
        print("Entry logic blocked during exit cooldown")
 
    # --- STAYING IN ROOM: mmWave consistently sees > 100 cm ---
    # only if bulb is already on; do NOT use this to turn ON light
    if light_on and distance_cm > DISTANCE_THRESHOLD:
        # presence confirmed
        pass

    time.sleep(0.15)
