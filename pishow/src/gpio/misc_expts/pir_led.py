import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #defining as BOARD different naming convention for IOs
GPIO.setup(3,GPIO.OUT) #define pin 3 as output
GPIO.setup(11,GPIO.IN) #define pin 11 as input from PIR

while True:
    i=GPIO.input(11)
    if i==0:         #when PIR senses nothing
        print ("Noone detected"),i
        GPIO.output(3,0) #set ledpin LOW/Led off
        time.sleep(0.1)    #delay

    if i==1:        #when PIR detects someone
        print ("Trigger!"), i
        GPIO.output(3,1) #set ledpin HIGH/Led on
        time.sleep(0.1)    #delay 
    
