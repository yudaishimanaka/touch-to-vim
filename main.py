import sys
import time
import Adafruit_MPR121.MPR121 as MPR121


cap = MPR121.MPR121()

if not cap.begin():
    sys.exit(1)

print("Press Ctrl-C to quit.")
last_touchd = cap.touched()
while True:
    current_touched = cap.touched()
    for i in range(12):
        pin_bit = 1 << i
        if current_touched & pin_bit and not last_touchd & pin_bit:
            print("{0} touched!".format(i))

        if not current_touched & pin_bit and last_touchd & pin_bit:
            print("{0} released!".format(i))

    last_touchd = current_touched
    time.sleep(0.1)
