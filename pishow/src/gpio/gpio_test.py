import time
import RPi.GPIO as io
io.setmode(io.BCM)

pir_pin = 18
door_pin = 23

io.setup(pir_pin, io.IN)
#io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)

while True:
    if io.input(pir_pin):
        print("PIR ALARM!")
    #if io.input(door_pin):
        #print("SWITCH ALARM!")
    time.sleep(0.5)
