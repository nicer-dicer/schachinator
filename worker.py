from time import sleep
import RPi.GPIO as GPIO # type: ignore
from setup import *


#globale variablen
current_coordinates = [0,0]


def move(coordinates):#moves from current position to chosen postition
    global current_coordinates
    #enable drivers
    GPIO.output(ENX, GPIO.LOW)
    GPIO.output(ENY, GPIO.LOW)
    global STOPX, STOPY #access variables as global
    #züge ausrechnen
    deltaX = (coordinates[0] - current_coordinates[0]) * feldgrösse
    deltaY = (coordinates[1] - current_coordinates[1]) * feldgrösse
    #move X axis up
    print(deltaX)
    if deltaX > 0:
        GPIO.output(DIRX, GPIO.HIGH) # richtung zu hoch
        for x in range(deltaX):
            if STOPX == 1:#failsafe incase it goes in the endstop
                GPIO.output(STEPX, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPX, GPIO.LOW)
                sleep(uS * usDelay)
            STOPX = GPIO.input(ENDX)
                
                
        #move X axis down
    elif deltaX < 0:
        GPIO.output(DIRX, GPIO.LOW) # richtung runter
        for x in range(deltaX):
            if STOPX == 1:#failsafe incase it goes in the endstop
                GPIO.output(STEPX, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPX, GPIO.LOW)
                sleep(uS * usDelay)
            STOPX = GPIO.input(ENDX)

    print(deltaY)
    # move Y axis up
    if deltaY > 0:
        GPIO.output(DIRY, GPIO.HIGH) # richtung hoch
        if STOPY == 1:#failsafe incase it goes in the endstop
            for y in range(deltaY):
                GPIO.output(STEPY, GPIO.HIGH)
                sleep(uS * usDelay)
                GPIO.output(STEPY, GPIO.LOW)
                sleep(uS * usDelay)
        STOPY = GPIO.input(ENDY)
                
    elif deltaY < 0:
        GPIO.output(DIRY, GPIO.LOW) # richtung runter
        if STOPY == 1:#failsafe incase it goes in the endstop
            for y in range(deltaY):
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
    #setup des workers
    global current_coordinates
    home()
    current_coordinates = [0,0]
    # anfang vom Loop
    worker_loop(task_queue)


def worker_loop(task_queue):
    while True:
        coordinates = task_queue.get()
        if coordinates == None:
            print("Worker: Stopping worker thread.")
            break
        
        move(coordinates)