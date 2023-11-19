# THIS IS JUST AN EXAMPLE TO HOW SUCH A SCRIPT COULD LOOK LIKE
# THE ACTUAL SCRIPT AND COSMIC RAY DETECTOR IS IN PROGRESS


import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
from datetime import datetime

GM_TUBE_PIN = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GM_TUBE_PIN, GPIO.IN)
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

scintillator_channel = AnalogIn(ads, ADS.P0)

# Energy Classification (Example)
BACKGROUND_THRESHOLD = 5000
COSMIC_RAY_THRESHOLD = 20000

def read_gm_tube():
    return GPIO.input(GM_TUBE_PIN)

def read_scintillator():
    return scintillator_channel.value

def classify_event(gm_tube_state, scintillator_value):
    if gm_tube_state and scintillator_value > COSMIC_RAY_THRESHOLD:
        return "Cosmic Ray"
    elif gm_tube_state or scintillator_value > BACKGROUND_THRESHOLD:
        return "Possible Cosmic Ray"
    else:
        return "Background"

def log_event(event_type, energy):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("cosmic_ray_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - Event Type: {event_type}, Energy: {energy}\n")

def main():
    try:
        while True:
            gm_tube_state = read_gm_tube()
            scintillator_value = read_scintillator()

            # Classify the event based on GM tube state and scintillator value
            event_type = classify_event(gm_tube_state, scintillator_value)

            # Log the event with type and energy
            log_event(event_type, scintillator_value)

            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
