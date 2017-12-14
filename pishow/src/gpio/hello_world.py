import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT) #define pin 3 as output

while True:
    GPIO.output(3,1) #set ledpin HIGH
    time.sleep(2)    #delay 2 sec
    GPIO.output(3,0) #set ledpin LOW
    time.sleep(2)    #delay 2 sec
    
