from time import sleep
import RPi.GPIO as GPIO # type: ignore
import setup


#globale variablen
current_coordinates = [0,0]


def move(coordinates):#moves from current position to chosen postition
    #züge ausrechnen
    deltaX = (coordinates[0] - current_coordinates[0]) * setup.feldgrösse
    deltaY = (coordinates[1] - current_coordinates[1]) * setup.feldgrösse
    print(deltaX)
    print(deltaY)
    
    
def worker_task(task_queue):
    #setup des workers
    global current_coordinates
    setup.home()
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