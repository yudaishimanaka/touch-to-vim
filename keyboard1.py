import atexit
import logging
import subprocess
import sys
import time
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
import uinput


KEY_MAPPING = {
    0: uinput.KEY_ENTER,
    1: uinput.KEY_RIGHT,
    2: uinput.KEY_U,
    3: uinput.KEY_M,
    4: uinput.KEY_UP,
    5: uinput.KEY_DOWN,
    6: uinput.KEY_I,
    7: uinput.KEY_O,
    8: uinput.KEY_ESC,
    9: uinput.KEY_LEFT,
    10: uinput.KEY_A,
    11: uinput.KEY_E,
}

IRQ_PIN = 26

MAX_EVENT_WAIT = 0.15
EVENT_WAIT_SLEEP = 0.1

subprocess.check_call(['modprobe', 'uinput'])

device = uinput.Device(KEY_MAPPING.values())

mpr121 = MPR121.MPR121()
if not mpr121.begin(0x5A):
    print('Faild to initializing MPR121!!')
    sys.exit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(IRQ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IRQ_PIN, GPIO.FALLING)
atexit.register(GPIO.cleanup)

mpr121.touched()

print('Press Ctrl-C to quit.')
while True:
    start = time.time()
    while (time.time() - start) < MAX_EVENT_WAIT and not GPIO.event_detected(IRQ_PIN):
        time.sleep(EVENT_WAIT_SLEEP)

    touched = mpr121.touched()
    for pin, key in KEY_MAPPING.iteritems():
        pin_bit = 1 << pin
        if touched & pin_bit:
            logging.debug('Input {0} touched. Keymap is {1}'.format(pin, key))
            device.emit_click(key)
