from setup import *

GPIO.output(magnetplus, GPIO.HIGH)
try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.output(magnetplus, GPIO.LOW)
    print("Main: KeyboardInterrupt received. Stopping threads...")
