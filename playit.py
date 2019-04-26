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

videos = glob.glob("videos/*.mp4")

while True:
    # play first video and measure time
    t = time.time()
    GPIO.add_event_detect(pin, GPIO.BOTH)
    syscmd("vlc --no-video-title-show --fullscreen --repeat" + videos[0])
    while GPIO.event_detected(pin) == False:
        time.sleep(1)

    sleepTime = (time.time - t) % (4 * 60)
    if sleepTime <= 21:
        time.sleep(sleepTime - 1)

    t = time.time()
    GPIO.add_event_detect(pin, GPIO.BOTH)
    syscmd("vlc --no-video-title-show --fullscreen --repeat" + videos[1])
    while (GPIO.event_detected(pin) == False) & (time.time() - t) < (20 * 3):
        time.sleep(1)

    syscmd("vlc --no-video-title-show --fullscreen --repeat" + videos[2])
    time.sleep(5)
