import socket
#import os
#import signal
#import subprocess
#import sys
import datetime
import time
import json

from naoqi import ALProxy
import almath

class naoRobot(object):
    #length:meter
    def __init__(self, ip, port):
        self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", ip, port)
        
        self.motionProxy = ALProxy("ALMotion", ip, port)
        self.notificationProxy = ALProxy("ALDiagnosis", ip, port)
        self.bodyTemperatureProxy = ALProxy("ALBodyTemperature", ip, port)
        self.batteryProxy = ALProxy("ALBattery", ip, port)
        
        self.initialize()
        
    
    def _disable_notifications(self):
        self.notificationProxy.setEnableNotification(False)
        self.bodyTemperatureProxy.setEnableNotifications(False)
        self.motionProxy.setEnableNotifications(False)
        self.batteryProxy.enablePowerMonitoring(False)      
    
    #def _interaction_speech(self, text, speed = 82, volume = 85):
        #self.ttsProxy.setParameter("speed", speed)
        #self.ttsProxy.setParameter("volume", volume)
        #configuration = {"bodyLanguageMode":"contextual"}       
        #self.animatedSpeechProxy.say(text, configuration)
        #self.ttsProxy.resetSpeed()
    
    def speech(self, text):
        self.animatedSpeechProxy.say(text)
    
    def stand(self):
        self.animatedSpeechProxy.say("customanimations-ff193e/stand")

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
        for chain in ["Body", "Legs", "Arms", "LArm", "RArm"]:
            self.motionProxy.setBreathEnabled(chain, True)
    
    def stop_idle(self):
        for chain in ["Body", "Legs", "Arms", "LArm", "RArm"]:
            self.motionProxy.setBreathEnabled(chain, False)

def custom_print(message):
    print message
    sys.stdout.flush()

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
        
def run_command(nao, command, flag):
    if flag == "speech":
        nao.speech(command)
        nao.stand()
    elif flag == "speech not stand back":
        nao.speech(command)
    elif flag == "action":
        pass
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
        