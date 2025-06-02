from time import sleep, time
import RPi.GPIO as GPIO  # type: ignore
from setup import *

# globale variablen
current_coordinates = [0, 0]

def set_magnet(magnet_on, move_color, last_direction, last_change_time):
    now = time()
    # If magnet should be off, ensure both are LOW and update timer
    if not magnet_on:
        GPIO.output(magnetplus, GPIO.LOW)
        GPIO.output(magnetminus, GPIO.LOW)
        if last_direction is not None:
            # Only update last_change_time if we just turned something off
            return None, now
        else:
            return None, last_change_time

    # If magnet should be on
    if move_color == "W":
        if last_direction != "W":
            # If switching, ensure both are LOW for 1 second
            GPIO.output(magnetplus, GPIO.LOW)
            GPIO.output(magnetminus, GPIO.LOW)
            elapsed = now - last_change_time
            if elapsed < 1:
                sleep(1 - elapsed)
            GPIO.output(magnetplus, GPIO.HIGH)
            return "W", time()
        else:
            # Already in correct state, ensure only magnetplus is HIGH
            GPIO.output(magnetplus, GPIO.HIGH)
            GPIO.output(magnetminus, GPIO.LOW)
            return "W", last_change_time
    elif move_color == "B":
        if last_direction != "B":
            # If switching, ensure both are LOW for 1 second
            GPIO.output(magnetplus, GPIO.LOW)
            GPIO.output(magnetminus, GPIO.LOW)
            elapsed = now - last_change_time
            if elapsed < 1:
                sleep(1 - elapsed)
            GPIO.output(magnetminus, GPIO.HIGH)
            return "B", time()
        else:
            # Already in correct state, ensure only magnetminus is HIGH
            GPIO.output(magnetplus, GPIO.LOW)
            GPIO.output(magnetminus, GPIO.HIGH)
            return "B", last_change_time
    else:
        # Unknown color, turn both off
        GPIO.output(magnetplus, GPIO.LOW)
        GPIO.output(magnetminus, GPIO.LOW)
        return None, now

def move(coordinates):
    global current_coordinates
    # Enable drivers
    GPIO.output(ENX, GPIO.LOW)
    GPIO.output(ENY, GPIO.LOW)
    global STOPX, STOPY  # access variables as global

    # Züge ausrechnen
    deltaX = (coordinates[0] - current_coordinates[0]) * feldgrösse
    deltaY = (coordinates[1] - current_coordinates[1]) * feldgrösse

    # Move X axis up
    print(f"deltaX: {deltaX}")
    if deltaX > 0:
        GPIO.output(DIRX, GPIO.HIGH)  # Richtung zu hoch
        for x in range(abs(deltaX)):
            if STOPX == 1:  # failsafe in case it goes in the endstop
                GPIO.output(STEPX, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPX, GPIO.LOW)
                sleep(uS * usDelay)
            STOPX = GPIO.input(ENDX)
    # Move X axis down
    elif deltaX < 0:
        GPIO.output(DIRX, GPIO.LOW)  # Richtung runter
        for x in range(abs(deltaX)):
            if STOPX == 1:
                GPIO.output(STEPX, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPX, GPIO.LOW)
                sleep(uS * usDelay)
            STOPX = GPIO.input(ENDX)

    print(f"deltaY: {deltaY}")
    # Move Y axis up
    if deltaY > 0:
        GPIO.output(DIRY, GPIO.HIGH)  # Richtung hoch
        if STOPY == 1:
            for y in range(abs(deltaY)):
                GPIO.output(STEPY, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPY, GPIO.LOW)
                sleep(uS * usDelay)
            STOPY = GPIO.input(ENDY)
    # Move Y axis down
    elif deltaY < 0:
        GPIO.output(DIRY, GPIO.LOW)  # Richtung runter
        if STOPY == 1:
            for y in range(abs(deltaY)):
                GPIO.output(STEPY, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPY, GPIO.LOW)
                sleep(uS * usDelay)
            STOPY = GPIO.input(ENDY)

    # Disable drivers after moving
    GPIO.output(ENX, GPIO.HIGH)
    GPIO.output(ENY, GPIO.HIGH)
    current_coordinates = coordinates

def worker_task(task_queue):
    global current_coordinates
    home()
    current_coordinates = [0, 0]
    worker_loop(task_queue)

def worker_loop(task_queue):
    last_direction = None  # "W" or "B"
    last_change_time = time()
    while True:
        task = task_queue.get()
        if task is None:
            print("Worker: Stopping worker thread.")
            break

        # Unpack the queue item
        # Expected: [x, y, magnet_on, move_color]
        x, y, magnet_on, move_color = task

        # Magnet logic
        new_direction, new_change_time = set_magnet(magnet_on, move_color, last_direction, last_change_time)
        last_direction = new_direction
        last_change_time = new_change_time

        # Move logic
        move([x, y])