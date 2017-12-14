import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #chose what mode to define IOs
GPIO.setup(2,GPIO.OUT) #define pin 3 as output
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) #define pin 11 as input from button

try:
    while True:
        button_state=GPIO.input(18)
        if button_state==0:         #when button pressed
            print ("Button pressed")
            GPIO.output(2,1) #set ledpin HIGH/Led on
            time.sleep(0.2)    #delay

        else:
            GPIO.output(2,0) #set ledpin LOW/Led off

except:
    GPIO.cleanup()
