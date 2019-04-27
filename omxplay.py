import RPi.GPIO as GPIO
import time
import subprocess
from utils import *
import glob


# set the input pin
pin = 23
# init GPIO shit
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Read the videos and sort them
videos = sorted(glob.glob("videos/*.mp4"))

#syscmd("export DISPLAY=:0", waiting=True)
GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=2000)

while True:
    # play first video in loop and measure time
    t = time.time()
    syscmd("omxplayer -b --loop --no-osd -o local --vol 0 " + videos[0])
    # Idle till event is detected
    while GPIO.event_detected(pin) == False:
        time.sleep(0.5)

    print("First Button pushed")
    # If the video is still playing-->idle some more
    sleepTime = (time.time() - t) % (4 * 60)
    if sleepTime <= 21:
        time.sleep(21 - sleepTime)
    # kill the first video
    syscmd("killall omxplayer.bin", waiting=True)

    # play second video in loop and measure time
    t = time.time()
    syscmd("omxplayer -b --loop --no-osd -o local --vol 0 " + videos[1])
    # Set event detector hard coded
    wasevent = False
    while (wasevent == False) and ((time.time() - t) < (20 * 3)):
        wasevent = GPIO.event_detected(pin)
        time.sleep(0.4)

    # If the video is still playing, idle some more
    sleepTime = (time.time() - t) % (20)
    if sleepTime <= 20:
        print("went into second sleeptime if")
        time.sleep(20 - sleepTime)

    # If the button was pushed play the last video and kill everything
    syscmd("killall omxplayer.bin")
    if wasevent == True:
        print("Second button pushed")
        syscmd("omxplayer -b --no-osd -o local --vol 0 " +
               videos[2], waiting=True)
        syscmd("killall omxplayer.bin")

GPIO.cleanup()
