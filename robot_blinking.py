import time
import random
import datetime
import sys

from naoqi import ALProxy

def log(log_file_name, message):
    log_file = open("logs/" + log_file_name, "a+")
    log_file.write("[" + str(datetime.datetime.today()) + "]: " + message + "\n")
    log_file.close()

def custom_print(message):
    print message
    sys.stdout.flush()

ip = "192.168.1.102"
port = 9559

proxy = ALProxy("ALLeds", ip, port)
file_name = "log_blinking.txt"

log(file_name, "=======================================================================\n")

while True:
    name = 'FaceLeds'
    
    intensity = 0.0
    duration = 0.2
    proxy.fade(name, intensity, duration)
    
    intensity = 1.0
    duration = 0.2
    proxy.fade(name, intensity, duration)
    
    log(file_name, "blink")
    custom_print("blink")
    
    interval = round(random.uniform(2, 10), 2)
    
    custom_print(str(interval))
    log(file_name, "interval(s): " + str(interval))
    time.sleep(interval)
