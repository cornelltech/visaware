import RPi.GPIO as GPIO
import sys
import os
from subprocess import Popen
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) #define pin 11 as input from button

movie1 = ("/opt/vc/src/hello_pi/hello_video/test.h264")
stream = ("http://192.168.0.18:8080/?action=stream")
stream1 = ("http://128.84.84.129:8080/?action=stream")

last_state1 = False
input_state1 = False
player = False


while True:

    #time.sleep(0.2)
    #Read state of input/button
    input_state1 = GPIO.input(18)

    if input_state1 != last_state1:
       
        if input_state1:
            #omxc.stdin.write('q')
            os.system('killall omxplayer.bin')
            player = True
            print("button released")

        elif (player and not input_state1):
            #os.system('killall omxplayer.bin')
            #omxc = Popen(['omxplayer', '-b', movie1])
            omxc = Popen(['omxplayer', '-b', '--live', stream1])
            player = False
            print("button pressed")

    #set last input states
    last_state1 = input_state1

    
    

