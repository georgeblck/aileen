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

videos = sorted(glob.glob("videos/*.mp4"))

syscmd("export DISPLAY=:0", waiting=True)

while True:
    # play first video and measure time
    t = time.time()
    GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=2000)
    syscmd("vlc --no-video-title-show --fullscreen --repeat " + videos[0])
    while GPIO.event_detected(pin) == False:
        time.sleep(1)

    sleepTime = (time.time() - t) % (4 * 60)
    if sleepTime <= 21:
        time.sleep(21 - sleepTime)

    syscmd("killall vlc")
    t = time.time()
    syscmd("vlc --no-video-title-show --fullscreen --repeat " + videos[1])
    while (GPIO.event_detected(pin) == False) | ((time.time() - t) < (20 * 3)):
        wasevent = GPIO.event_detected(pin)
        time.sleep(1)

    syscmd("killall vlc")
    if wasevent == True:
        syscmd("vlc --no-video-title-show --fullscreen " +
               videos[2], waiting=True)

GPIO.cleanup()
