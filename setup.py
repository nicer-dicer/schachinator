from time import sleep
import RPi.GPIO as GPIO # type: ignore


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
STEPX = 18 # step pin
DIRX = 14 # direction pin
ENX = 4 # enable pin
ENDX = 24 # endschalter
GPIO.setup(STEPX, GPIO.OUT)
GPIO.setup(DIRX, GPIO.OUT)
GPIO.setup(ENX, GPIO.OUT)
GPIO.setup(ENDX, GPIO.IN)
STOPX = GPIO.input(ENDX) # get stopx value

STEPY = 27 # step pin
DIRY = 17 # direction pin
ENY = 22 # enable pin
ENDY = 23 # endschalter
GPIO.setup(STEPY, GPIO.OUT)
GPIO.setup(DIRY, GPIO.OUT)
GPIO.setup(ENY, GPIO.OUT)
GPIO.setup(ENDY, GPIO.IN)
STOPY = GPIO.input(ENDY) # get stopy value

usDelay = 950 # number of microseconds
uS = 0.000001 # one microsecond

feldgrösse = 180
rand = 30

print("[press ctrl+c to end the script]")


def home():
    
    HOME = [30,30] #Hier wird die home position in steps von den endschalten definiert
    
    #Home X Achse
    try: # Main program loop
        GPIO.output(ENX, GPIO.LOW)
        GPIO.output(DIRX, GPIO.LOW) # richtung zu endschalter
        STOPX = GPIO.input(ENDX)
        print(STOPX)
        while STOPX == 1:
            GPIO.output(STEPX, GPIO.HIGH)
            sleep(uS * usDelay)
            GPIO.output(STEPX, GPIO.LOW)
            sleep(uS * usDelay)
            STOPX = GPIO.input(ENDX)
        
        
        #nach erreichen des endschalters zu 0|0 fahren
        GPIO.output(DIRX, GPIO.HIGH) #richtung zu (0|0)
        for i in range(HOME[0]):
            GPIO.output(STEPX, GPIO.HIGH)
            sleep(uS * usDelay)
            GPIO.output(STEPX, GPIO.LOW)
            sleep(uS * usDelay)
            
        GPIO.output(ENX, GPIO.HIGH) # treiber deaktivieren
            
    # Home Y Achse        
            
        GPIO.output(ENY, GPIO.LOW)
        GPIO.output(DIRY, GPIO.LOW) # richtung zum  endschalter
        STOPY = GPIO.input(ENDY)
        print(STOPY)
        while STOPY == 1:
            GPIO.output(STEPY, GPIO.HIGH)
            sleep(uS * usDelay)
            GPIO.output(STEPY, GPIO.LOW)
            sleep(uS * usDelay)
            STOPY = GPIO.input(ENDY)
            
        #nach erreichen des endschalters zu 0|0 fahren
        GPIO.output(DIRY, GPIO.HIGH) #richtung zu (0|0)
        for i in range(HOME[1]):
            GPIO.output(STEPY, GPIO.HIGH)
            sleep(uS * usDelay)
            GPIO.output(STEPY, GPIO.LOW)
            sleep(uS * usDelay)
            
        GPIO.output(ENY, GPIO.HIGH) # treiber deaktivieren
        
    except KeyboardInterrupt:
        # treiber deaktivieren
        GPIO.output(ENX, GPIO.HIGH)
        GPIO.output(ENY, GPIO.HIGH)


if __name__ == "__main__":
    home()
