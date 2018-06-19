import random
import time
import datetime
import sys

from naoqi import ALProxy
import almath

def log(log_file_name, message):
    log_file = open("logs/" + log_file_name, "a+")
    log_file.write("[" + str(datetime.datetime.today()) + "]: " + message + "\n")
    log_file.close()
    
def custom_print(message):
    print message
    sys.stdout.flush()

def getAmplitude(bpm):
    return bpm / (-30.0) + 1.0

if __name__ == "__main__":

    ip = "192.168.1.102"
    port = 9559
    
    file_name = "log_idle.txt"
    log(file_name, "=======================================================================\n")
    
    motionProxy = ALProxy("ALMotion", ip, port)
    postureProxy = ALProxy("ALRobotPosture", ip, port)
    
    while True:
        min_bpm = 6
        max_bpm = 25
        bpm = random.randint(min_bpm, max_bpm)
        amplitude = round(random.uniform(getAmplitude(min_bpm), getAmplitude(bpm)), 1)
        motionProxy.setBreathConfig([['Bpm', bpm], ['Amplitude', amplitude]])
        log(file_name, "breath config: bpm = " + str(bpm) + ", amplitude = " + str(amplitude))
        custom_print("breath config: bpm = " + str(bpm) + ", amplitude = " + str(amplitude))
        
        """
        isHeadMove = random.randint(0, 100)
        if isHeadMove <= 60:
            headPitch = round(random.uniform(-21.6, 15.5), 1)
            headYaw = round(random.uniform(-30.9, 42.1), 1)
            motionProxy.angleInterpolationWithSpeed(["HeadYaw", "HeadPitch"], [headYaw * almath.TO_RAD, headPitch * almath.TO_RAD], 0.1)
            custom_print("move head: HeadPitch = " + str(headPitch) + ", HeadYaw = " + str(headYaw))
            log(file_name, "move head: HeadPitch = " + str(headPitch) + ", HeadYaw = " + str(headYaw))
            
        isLeftHandMove = random.randint(0, 100)
        custom_print("isLeftHandMove = " + str(isLeftHandMove))
        if isLeftHandMove <= 50:
            lHand = round(random.uniform(0.2, 0.8), 2)
            motionProxy.setAngles(["LHand"], [lHand], 0.1)
            log(file_name, "move left hand: LHand = " + str(lHand))
            custom_print("move left hand: LHand = " + str(lHand))
        
        isRightHandMove = random.randint(0, 100)
        custom_print("isRightHandMove = " + str(isRightHandMove))
        if isRightHandMove <= 50:
            rHand = round(random.uniform(0.2, 0.8), 2)
            motionProxy.setAngles(["RHand"], [rHand], 0.1)
            log(file_name, "move rihgt hand: RHand = " + str(rHand))
            custom_print("move right hand: LHand = " + str(rHand))
        """
            
        time.sleep(15)
