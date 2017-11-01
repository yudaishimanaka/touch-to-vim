import time
import RPi.GPIO as GPIO
import uinput
import subprocess


KEY_MAPPING = {
    13: uinput.KEY_A,
    24: uinput.KEY_I,
    12: uinput.KEY_U,
    16: uinput.KEY_E,
    21: uinput.KEY_O,
}

SWITCH_PIN = [13, 24, 12, 16, 21]
MAX_EVENT_WAIT = 0.3
EVENT_WAIT_SLEEP = 0.1

subprocess.check_call(['modprobe', 'uinput'])

device = uinput.Device(KEY_MAPPING.values())

try:
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SWITCH_PIN, GPIO.IN)
        for i, key in KEY_MAPPING.iteritems():
            switch_state = GPIO.input(i)
            if switch_state == False:
                device.emit_click(key)

        GPIO.cleanup()

except KeyboardInterrupt:
    pass

