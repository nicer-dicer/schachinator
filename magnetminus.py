from setup import *

GPIO.output(magnetminus, GPIO.HIGH)
try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.output(magnetminus, GPIO.LOW)
    print("Main: KeyboardInterrupt received. Stopping threads...")
