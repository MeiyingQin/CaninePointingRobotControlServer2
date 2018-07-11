import socket
#import os
#import signal
#import subprocess
import sys
import datetime
import time
import json
import random
import threading

from naoqi import ALProxy
import almath

from bait import Dispenser

class naoRobot(object):
    #length:meter
    def __init__(self, ip, port):
        
        self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", ip, port)
        self.postureProxy = ALProxy("ALRobotPosture", ip, port)
        self.behaviourProxy = ALProxy("ALBehaviorManager", ip, 9559)
        self.ledProxy = ALProxy("ALLeds", ip, port)
        
        self.motionProxy = ALProxy("ALMotion", ip, port)
        self.notificationProxy = ALProxy("ALDiagnosis", ip, port)
        self.bodyTemperatureProxy = ALProxy("ALBodyTemperature", ip, port)
        self.batteryProxy = ALProxy("ALBattery", ip, port)
        
        self.right_arm = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw", "RWristYaw"]
        self.left_arm = ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw", "LWristYaw"]
        self.head = ["HeadYaw", "HeadPitch"]

        self.stand_joints = {
            "RShoulderPitch": [83.4, 30.0/3],
            "RShoulderRoll": [-9.8, 10.0/3],
            "RElbowRoll": [23.0, 18.0/3],
            "RElbowYaw": [69.5, 39.0/3],
            "RWristYaw": [3.8, 90.0/3],
            "LShoulderPitch": [83.5, 30.0/3],
            "LShoulderRoll": [8.6, 10.0/3],
            "LElbowRoll": [-22.5, 18.0/3],
            "LElbowYaw": [-66.9, 40.0/3],
            "LWristYaw": [6.8, 90.0/3],
            "HeadYaw": [0, 30.0/3],
            "HeadPitch": [-7.5, 20.0/3]
        }
        
        self.scratch = [
            "customanimations-ff193e/scratch_back_left",
            "customanimations-ff193e/scratch_back_right",
            "customanimations-ff193e/scratch_eye",
            "customanimations-ff193e/scratch_leg",
        ]
        random.shuffle(self.scratch)
        
        self.stretch = [
            "customanimations-ff193e/relax_leg"
        ]
        
        self.idling = False
        self.is_running_idling = False
        
        self.blinking = False
        self.is_running_blinking = False        
        
        self.initialize()
    
    def _disable_notifications(self):
        self.notificationProxy.setEnableNotification(False)
        self.bodyTemperatureProxy.setEnableNotifications(False)
        self.motionProxy.setEnableNotifications(False)
        self.batteryProxy.enablePowerMonitoring(False)

    def _deg_to_rad(self, deg_lsts):
        return [x * almath.TO_RAD for x in deg_lsts]
    
    def _run_behaviour(self, behaviour):
        self.behaviourProxy.startBehavior(behaviour)
        
        while self.behaviourProxy.isBehaviorRunning(package_name + behaviour):
            time.sleep(0.5)
    
    def _joint_move_blocking(self, joint_lsts, angle_lsts, speed):
        self.motionProxy.angleInterpolationWithSpeed(joint_lsts, angle_lsts, speed)    
        
    #def _interaction_speech(self, text, speed = 82, volume = 85):
        #self.ttsProxy.setParameter("speed", speed)
        #self.ttsProxy.setParameter("volume", volume)
        #configuration = {"bodyLanguageMode":"contextual"}       
        #self.animatedSpeechProxy.say(text, configuration)
        #self.ttsProxy.resetSpeed()
    
    def speech(self, text):
        print "in speech text", text
        self.animatedSpeechProxy.say(text)
    
    def stand(self, speed):
        self.postureProxy.goToPosture("Stand", speed)

    def initialize(self):
        #self.ttsProxy.setParameter("volume", 82)
        self._disable_notifications()
        self.animatedSpeechProxy.setBodyLanguageModeFromStr("disabled")
    
    #def torso_stand(self, speed=None):
        #left_arm = [83.4, 10.4, -24, -67.5, 6.7, 0.3]
        #right_arm = [83.4, -10.4, 24, 67.5, 6.7, 0.3]
        
        #left_leg = [-10.1, 7.5, 5.6, -5.2, -7.4, 5.1]
        #right_leg = [-10.1, 7.5, -5.6, -5.2, 7.4, 5.1]
        
        #arm_movements = self._arm_movement(left_arm=left_arm, right_arm=right_arm)
        #leg_movements = self._leg_movement(left_leg=left_leg, right_leg=right_leg)
        
        #if speed == None:
            #speed = self.speed
            
        #self._run_movement_blocking([arm_movements], self.speed)
    
    #def torso_stand_unblocking(self):
        #left_arm = [83.4, 10.4, -24, -67.5, 6.7, 0.3]
        #right_arm = [83.4, -10.4, 24, 67.5, 6.7, 0.3]
    
        #left_leg = [-10.1, 7.5, 5.6, -5.2, -7.4, 5.1]
        #right_leg = [-10.1, 7.5, -5.6, -5.2, 7.4, 5.1]
    
        #arm_movements = self._arm_movement(left_arm=left_arm, right_arm=right_arm)
        #leg_movements = self._leg_movement(left_leg=left_leg, right_leg=right_leg)
    
        #self._run_movement_unblocking([arm_movements], self.speed)
    
    def start_idle(self):
        self.idling = True
        while self.idling:
            self.is_running_idling = True
            
            mode = random.random()
            if mode < 0.015: # stretch leg
                self._run_behaviour(self.stretch[1])
                self.stand()
            elif mode < 0.030: # scratch back, eye or leg
                if len(self.scratch) > 0:
                    self._run_behavoiur(self.scratch.pop())
                    self.stand()
            else:              
                joint_lists = []
                angle_lists = []
                
                for joint, [mean, sd] in self.stand_joints.items():
                    is_move = random.randint(1, 10) != 7
                    if is_move:
                        angle = random.gauss(mean, sd)
                        joint_lists.append(joint)
                        angle_lists.append(angle)
                
                self._joint_move_blocking(joint_lists, angle_lists, 0.2)

            self.is_running_idling = False
            
            wait = random.randint(1, 10)
            interval = 0.1
            for loop in range(int(wait / interval)):
                if not self.idling:
                    break
                time.sleep(interval)
    
    def stop_idle(self):
        self.idling = False
        
        while self.is_running_idling:
            time.sleep(0.1)
        
        self.stand(0.2)
    
    def start_blinking(self):
        self.blinking = True
        while self.blinking:
            self.is_running_blinking = True
            
            name = 'FaceLeds'
            intensity = 0.0
            duration = 0.2
            self.ledProxy.fade(name, intensity, duration)
            
            intensity = 1.0
            duration = 0.2
            self.ledProxy.fade(name, intensity, duration)
            
            custom_print("blink")

            self.is_running_blinking = False
            
            wait = round(random.uniform(2, 10), 2)
            interval = 0.1
            for loop in range(int(wait / interval)):
                if not self.blinking:
                    break
                time.sleep(interval)
    
    def stop_blinking(self):
        self.blinking = False
        
        while self.is_running_blinking:
            time.sleep(0.1)
    
    def stop(self):
        self.stop_idle()
        self.stop_blinking()

def custom_print(message):
    print message
    sys.stdout.flush()

def dispenser_rotate(dispenser_lists):
    pass
    """
    threads = []
    for dispenser in dispenser_lists:
        dispenser_thread = threading.Thread(target=Dispenser.feed, args=(dispenser, ))
        threads.append(dispenser_thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    """

def is_initial_information(command):
    command_list = command.strip().split(DELIMINATOR)
    return command_list[0] == INITIAL_INFORMATION

def set_initial_information(commmand):
    command_list = command.strip().split(DELIMINATOR)
    return [NAME_TAG + x.lower() for x in command_list[1:]]

def parse_command(command, library, dog, dog_gender, owner, pointer, assistant):
    command_list = command.strip().split(DELIMINATOR)
    if len(command_list) != 3:
        return
    
    section = command_list[0]
    command_name = command_list[1]
    condition = command_list[2]
    
    command_content = library[section][command_name][condition][DICT_COMMAND_KEY]
    flag = library[section][command_name][condition][DICT_FLAG_KEY]
    
    return command_content, flag

def run_command(nao, commands, flags, dispensers):
    print commands
    for flag_index in range(len(flags)):
        command = commands[flag_index]
        command = str(command)
        if flags[flag_index] == DICT_FLAG_SPEECH:
            command = command.replace(DICT_OWNER_TAG, owner)
            command = command.replace(DICT_DOG_TAG, dog)
            command = command.replace(DICT_DOG_GENDER_TAG, dog_gender)
            command = command.replace(DICT_POINTER_TAG, pointer)
            command = command.replace(DICT_ASSISTANT_TAG, assistant)
            print "run speech command: ", command
            nao.speech(command)
        elif flags[flag_index] == DICT_FLAG_ACTION:
            print "run action command: ", command
            if command == "start_idle":
                idle_thread = threading.Thread(target=naoRobot.start_idle, args=(nao, ))
                idle_thread.start()
                idle_thread.join()
            elif command == "stop_idle":
                nao.stop_idle()
            elif command == "stand":
                nao.stand(0.3)
            elif command == "dispenser_rotate":
                dispenser_rotate(dispensers)
            else:
                custom_print("command is not defined")
        else:
            custom_print(flag)
            custom_print("this is not a valid flag")
            

def log(log_file_name, message):
    log_file = open("logs/" + log_file_name, "a+")
    log_file.write("[" + str(datetime.datetime.today()) + "]: " + message + "\n")
    log_file.close()

if __name__ == "__main__":
    CONNECTION_RESPOND = "success"
    LINE_TERMINATOR = "\n"
    DELIMINATOR = "|"
    INITIAL_INFORMATION = "initial information"
    DICT_COMMAND_KEY = "robot"
    DICT_FLAG_KEY = "flag"
    DICT_FLAG_SPEECH = "speech"
    DICT_FLAG_ACTION = "action"
    DICT_OWNER_TAG = "<owner>"
    DICT_DOG_TAG = "<dog>"
    DICT_DOG_GENDER_TAG = "<dog_gender>"
    DICT_POINTER_TAG = "<pointer>"
    DICT_ASSISTANT_TAG = "<assistant>"
    NAME_TAG = "name_"
    
    json_file='data.json'
    json_data = open(json_file)
    command_library = json.load(json_data)
    json_data.close()    
    
    robot_ip = "192.168.1.102"
    robot_port = 9559
    
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_ip = "192.168.1.101"
    server_ip = "192.168.1.116"
    server_port = 10000
    server_address = (server_ip, server_port)
    socket.bind(server_address)
    socket.listen(1)
    
    file_name = "log_robot_actions.txt"
    log(file_name, "=======================================================================\n")
    
    nao = naoRobot(robot_ip, robot_port)
    
    custom_print("server ip: " + server_ip)
    custom_print("server port: " + str(server_port))
    
    dispenser_1 = Dispenser("robot.pointing.feeder.1@gmail.com", "")
    dispenser_2 = Dispenser("robot.pointing.feeder.2@gmail.com", "")
    
    dispensers = [dispenser_1, dispenser_2]
    
    try:
        while True:
            
            connection, client_address = socket.accept()
            custom_print("get connection from " + str(client_address))
            log(file_name, "get connection from " + str(client_address))
            
            blinking_thread = threading.Thread(target=naoRobot.start_blinking, args=(nao, ))
            blinking_thread.start()
            
            dog = ""
            dog_gender = ""
            owner = ""
            pointer = ""
            assistant = ""
            
            is_connected = True
            
            while is_connected:
                data = connection.recv(1024)
                if data:
                    custom_print("received: " + data.strip())
                    log(file_name, "received data: " + data.strip())
                    command = data.strip()
                    if is_initial_information(command):
                        [owner, dog, dog_gender, pointer, assistant] = set_initial_information(command)
                    else:
                        command_content, flag = parse_command(command, command_library, dog, dog_gender, owner, pointer, assistant)
                        if command:
                            run_command(nao, command_content, flag, dispensers)
                    connection.sendall(CONNECTION_RESPOND + LINE_TERMINATOR)
                else:
                    custom_print("received empty data, close socket")
                    log(file_name, "close socket")
                    is_connected = False
                    nao.stop()
                    blinking_thread.join()
            
            connection.close()
    except KeyboardInterrupt:
        socket.close()
        custom_print("main server receive keyboard interruption, close socket and shut server down")
        nao.stop()
        blinking_thread.join()        