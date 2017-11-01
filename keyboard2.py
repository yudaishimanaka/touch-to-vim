import atexit
import logging
import subprocess
import sys
import time
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
import uinput


KEY_MAPPING = {
    0: uinput.KEY_BACKSPACE,
    1: uinput.KEY_E,
    2: uinput.KEY_H,
    3: uinput.KEY_H,
    4: uinput.KEY_U,
    5: uinput.KEY_A,
    6: uinput.KEY_O,
    7: uinput.KEY_H,
    8: uinput.KEY_Q,
    9: uinput.KEY_I,
    10: uinput.KEY_H,
    11: uinput.KEY_H,
}

MOTHER_KEYS = {
    0: uinput.KEY_A, 
    1: uinput.KEY_K, 
    2: uinput.KEY_S, 
    3: uinput.KEY_T, 
    4: uinput.KEY_N, 
    5: uinput.KEY_H, 
    6: uinput.KEY_M,
    7: uinput.KEY_Y, 
    8: uinput.KEY_R, 
    9: uinput.KEY_W, 
    10: uinput.KEY_G, 
    11: uinput.KEY_Z, 
    12: uinput.KEY_D, 
    13: uinput.KEY_B,
}

IRQ_PIN = 26

MAX_EVENT_WAIT = 0.15
EVENT_WAIT_SLEEP = 0.1

subprocess.check_call(['modprobe', 'uinput'])

device = uinput.Device(KEY_MAPPING.values())
device2 = uinput.Device(MOTHER_KEYS.values())
mpr121 = MPR121.MPR121()
if not mpr121.begin(0x5B):
    print('Faild to initializing MPR121!!')
    sys.exit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(IRQ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IRQ_PIN, GPIO.FALLING)
atexit.register(GPIO.cleanup)

mpr121.touched()

mother_state = 0

print('Press Ctrl-C to quit.')
while True:
    start = time.time()
    while (time.time() - start) < MAX_EVENT_WAIT and not GPIO.event_detected(IRQ_PIN):
        time.sleep(EVENT_WAIT_SLEEP)

    touched = mpr121.touched()
    for pin, key in KEY_MAPPING.iteritems():
        pin_bit = 1 << pin
        if touched & pin_bit:
            if pin_bit == 256:
                if mother_state == 13:
                    mother_state = 0
                else:
                    mother_state += 1
            
            if mother_state == 0:
                device.emit_click(key)
            else:
                device2.emit_click(MOTHER_KEYS[mother_state])
                device.emit_click(key)
