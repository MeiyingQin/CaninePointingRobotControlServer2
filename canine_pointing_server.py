import socket
#import os
#import signal
#import subprocess
#import sys
import datetime
import time
import json
import random

from naoqi import ALProxy
import almath

class naoRobot(object):
    #length:meter
    def __init__(self, ip, port):
        self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", ip, port)
        self.postureProxy = ALProxy("ALRobotPosture", ip, port)
        self.behaviourProxy = ALProxy("ALBehaviorManager", ip, 9559)
        
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
        self.animatedSpeechProxy.say(text)
    
    def stand(self, speed):
        self.postureProxy.goToPosture("Stand", speed)

    def initialize(self):
        #self.ttsProxy.setParameter("volume", 82)
        self._disable_notifications()
    
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
        
        self.stand()

def custom_print(message):
    print message
    sys.stdout.flush()

def dispenser_rotate(dispenser_lists):
    pass

def parse_command(command, library):
    command_list = command.split(DELIMINATOR)
    if len(command_list) != 3:
        return
    
    section = command_list[0]
    command_name = command_list[1]
    condition = command_list[2]
    
    command_content = library[section][command_name][condition]["robot"]
    flag = library[section][command_name][condition]["flag"]
    
    return command_content, flag

def run_command(nao, command, flags, dispensers):
    flag_list = flag.strip().split(DELIMINATOR)
    
    for flag in flag_list:
        if flag == "speech":
            nao.speech(command)
        elif flag == "action":
            if command == "start_idle":
                nao.start_idle()
            elif command == "stop_idle":
                nao.stop_idle()
            elif command == "stand":
                nao.stand(0.2)
            elif command == "dispenser_rotate":
                pass
            else:
                custom_print("command is not defined")
        else:
            custom_print("this is not a valid flag")

def log(log_file_name, message):
    log_file = open("logs/" + log_file_name, "a+")
    log_file.write("[" + str(datetime.datetime.today()) + "]: " + message + "\n")
    log_file.close()

if __name__ == "__main__":
    CONNECTION_RESPOND = "success"
    LINE_TERMINATOR = "\n"
    DELIMINATOR = "|"
    
    json_file='data.json'
    json_data = open(json_file)
    command_library = json.load(json_data)
    json_data.close()    
    
    robot_ip = "192.168.1.102"
    robot_port = 9559
    
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.1.101"
    server_port = 10000
    server_address = (server_ip, server_port)
    socket.bind(server_address)
    socket.listen(1)
    
    file_name = "log_robot_actions.txt"
    log(file_name, "=======================================================================\n")  
    log(file_name, "robot speed = " + str(robot_speed) + "robot wait = " + str(robot_wait))
    
    idle_pid = []
    blinking_pid = []
    touch_pid = []   
    
    nao = naoRobot(robot_ip, robot_port)
    
    custom_print("server ip: " + server_ip)
    custom_print("server port: " + str(server_port))
    
    #pid = None   
    
    while True:
        
        if len(idle_pid) != 0:
            for pid in idle_pid:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            idle_pid = []
        
        if len(blinking_pid) != 0:
            for pid in blinking_pid:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            blinking_pid = []
        
        if len(touch_pid) != 0:
            for pid in blinking_pid:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            touch_pid = []
        
        blinking_process = subprocess.Popen("python ./robot_blinking.py", stdout=None, shell=True, preexec_fn=os.setsid)
        touch_process = subprocess.Popen("python ./touchsensor.py", stdout=None, shell=True, preexec_fn=os.setsid)
        
        blinking_pid.append(blinking_process.pid)
        touch_pid.append(touch_process.pid)
        
        connection, client_address = socket.accept()
        custom_print("get connection from " + str(client_address))
        log(file_name, "get connection from " + str(client_address))
        is_connected = True
        
        while is_connected:
            data = connection.recv(1024)
            if data:
                custom_print("received: " + data.strip())
                log(file_name, "received data: " + data.strip())
                command = data.strip()
                command_content, flag = parse_command(command, command_library)
                run_command(nao, command_content, flag)
                connection.sendall(CONNECTION_RESPOND + LINE_TERMINATOR)
            else:
                custom_print("received empty data, close socket")
                log(file_name, "close socket")
                is_connected = False               
        