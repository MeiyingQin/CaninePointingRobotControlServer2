import socket
import sys
import os
import signal
import subprocess
import sys
import datetime
import time

from naoqi import ALProxy
import almath

class naoRobot(object):
    #length:meter
    def __init__(self, ip, port, speed, wait):
        self.ttsProxy = ALProxy("ALTextToSpeech", ip, port)
        self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", ip, port)
        self.postureProxy = ALProxy("ALRobotPosture", ip, port)
        self.motionProxy = ALProxy("ALMotion", ip, port)
        self.notificationProxy = ALProxy("ALDiagnosis", ip, port)
        self.bodyTemperatureProxy = ALProxy("ALBodyTemperature", ip, port)
        self.batteryProxy = ALProxy("ALBattery", ip, port)
        self.right_arm = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw", "RWristYaw", "RHand"]
        self.left_arm = ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw", "LWristYaw", "LHand"]
        self.right_leg = ["RHipYawPitch", "RHipPitch", "RHipRoll", "RKneePitch", "RAnkleRoll", "RAnklePitch"]
        self.left_leg = ["LHipYawPitch", "LHipPitch", "LHipRoll", "LKneePitch", "LAnkleRoll", "LAnklePitch"]
        self.head = ["HeadYaw", "HeadPitch"]
        self.left_leg = []
        self.right_leg = []
        self.speed = speed
        self.wait = wait
        
        self.initialize()
        
    
    def _disable_notifications(self):
        self.notificationProxy.setEnableNotification(False)
        self.bodyTemperatureProxy.setEnableNotifications(False)
        self.motionProxy.setEnableNotifications(False)
        self.batteryProxy.enablePowerMonitoring(False)      
    
    def _joint_move_blocking(self, joint_lsts, angle_lsts, speed):
        self.motionProxy.angleInterpolationWithSpeed(joint_lsts, angle_lsts, speed)
        
    def _joint_move_unblocking(self, joint_lsts, angle_lsts, speed):
        self.motionProxy.setAngles(joint_lsts, angle_lsts, speed)
        
    def _arm_movement(self, left_arm = [], right_arm = []):
        joint_lsts = []
        angle_lsts = []
        
        if not left_arm and not right_arm:
            return
        
        if right_arm:
            joint_lsts += self.right_arm
            angle_lsts += self._deg_to_rad(right_arm[:-1]) + [right_arm[-1]]
        
        if left_arm:
            joint_lsts += self.left_arm
            angle_lsts += self._deg_to_rad(left_arm[:-1]) + [left_arm[-1]]
            
        return joint_lsts, angle_lsts
    
    def _leg_movement(self, left_leg, right_leg):
        joint_lsts = []
        angle_lsts = []
        
        joint_lsts += self.left_leg
        joint_lsts += self.right_leg
        angle_lsts += left_leg
        angle_lsts += right_leg
        
        return joint_lsts, self._deg_to_rad(self.angle_lsts)
    
    def _head_movement(self, head_angles):
        return self.head, self._deg_to_rad(head_angles)
    
    def _leg_movement(self, left_leg, right_leg):
        joint_lsts = []
        angle_lsts = []
        
        joint_lsts += self.left_leg
        joint_lsts += self.right_leg
        angle_lsts += left_leg
        angle_lsts += right_leg
        
        return joint_lsts, self._deg_to_rad(angle_lsts)
    
    def _run_movement_blocking(self, lst_move_tuples, speed):
        joint_lsts = []
        angle_lsts = []
        
        joint_lsts = [y for x in lst_move_tuples for y in x[0]]
        angle_lsts = [y for x in lst_move_tuples for y in x[1]]
        
        self._joint_move_blocking(joint_lsts, angle_lsts, speed)
    
    def _run_movement_unblocking(self, lst_move_tuples, speed):
        joint_lsts = []
        angle_lsts = []
    
        joint_lsts = [y for x in lst_move_tuples for y in x[0]]
        angle_lsts = [y for x in lst_move_tuples for y in x[1]]
    
        self._joint_move_unblocking(joint_lsts, angle_lsts, speed)
    
    def _open_hand(self):
        self._joint_move_blocking(["LHand", "RHand"], [1.0, 1.0], 0.3)
    
    def _close_hand(self):
        self._joint_move_blocking(["LHand", "RHand"], [0.0, 0.0], 0.3)
    
    def _bait(self, speed, left_arm=[], right_arm=[]):
        movements = self._arm_movement(left_arm=left_arm, right_arm=right_arm)
        self._run_movement_blocking([movements], speed)
        time.sleep(self.wait)
        
        self._open_hand()
        time.sleep(self.wait)
        
        self._close_hand()
        time.sleep(self.wait)

    def _deg_to_rad(self, deg_lsts):
        return [x * almath.TO_RAD for x in deg_lsts]
    
    def _interaction_speech(self, text, speed = 82, volume = 85):
        self.ttsProxy.setParameter("speed", speed)
        self.ttsProxy.setParameter("volume", volume)
        configuration = {"bodyLanguageMode":"contextual"}       
        self.animatedSpeechProxy.say(text, configuration)
        self.ttsProxy.resetSpeed()
    
    def _speech(self, text, speed = 82, volume = 85):
        self.ttsProxy.setParameter("speed", speed)
        self.ttsProxy.setParameter("volume", volume)
        self.ttsProxy.say(text)
        self.ttsProxy.resetSpeed()
    
    def _gaze_point(self, dog_name, head_angle_lsts, left_arm_angles=[], right_arm_angles=[]):
        self.stand(self.speed)
        self._speech(dog_name)
        time.sleep(self.wait)
        
        arm_movements = self._arm_movement(left_arm = left_arm_angles, right_arm = right_arm_angles)
        head_movements = self._head_movement(head_angle_lsts)
        
        self._run_movement_unblocking([arm_movements, head_movements], 0.2)
        self._speech("look")
        
        time.sleep(4)
        nao._speech("\\emph=1\\ Oh \\emph=0\\ kay")

    def initialize(self):
        self.ttsProxy.setParameter("volume", 82)
        self._disable_notifications()
    
    def stand(self, speed):
        self.postureProxy.goToPosture("Stand", speed)
    
    def kneels(self, speed):
        self.postureProxy.goToPosture("Crouch", speed)
    
    def get_bait(self):
        self.head_down()
        time.sleep(self.wait)
        movements = self._arm_movement(left_arm=[71.8, 0.8, -69.6, -53.3, -92.5, 1], right_arm=[71.8, -0.8, 69.6, 53.3, 92.5, 1])
        self._run_movement_blocking([movements], self.speed)
    
    def bait_middle(self):
        #movements = self._arm_movement(left_arm=[68.6, -0.4, -81.4, -79.9, 65.8, 0], right_arm=[68.6, -0.4, 81.4, 79.9, -65.8, 0])
        movements = self._arm_movement(left_arm=[31, -7.8, -7.8, -82.9, -90.2, 0], right_arm=[31, 7.8, 7.8, 82.9, 90.2,  0])
        self._run_movement_blocking([movements], self.speed)
        
        time.sleep(0.5)
        
        movements = self._arm_movement(left_arm=[31, -7.8, -7.8, -82.9, 90.2, 0], right_arm=[31, 7.8, 7.8, 82.9, -90.2,  0])
        self._run_movement_blocking([movements], self.speed)
        
        time.sleep(self.wait)
    
        movements = self._arm_movement(left_arm=[71.8, 0.8, -69.6, -53.3, -92.5, 0], right_arm=[71.8, -0.8, 69.6, 53.3, 92.5, 0])
        self._run_movement_blocking([movements], self.speed)        

    def bait_left(self):
        movements = self._arm_movement(left_arm=[58.4, 46.2, -29.9, -119.3, -92.3, 0])
        self._run_movement_blocking([movements], self.speed)
    
        time.sleep(1)
    
        movements = self._arm_movement(left_arm=[58.4, 46.2, -29.9, -119.3, 70.3, 0])
        self._run_movement_blocking([movements], self.speed)
    
        time.sleep(self.wait)        
        #movements = self._arm_movement(left_arm=[38.3, 50.9, -25.3, -118.8, -81.6, 0])
        #movements = self._arm_movement(left_arm=[39.5, 54.4, -21.9, -119.4, -80.6, 0])
        #self._run_movement_blocking([movements], self.speed)
    
        #time.sleep(1)
    
        #movements = self._arm_movement(left_arm=[39.5, 54.4, -21.9, -119.4, 70.6, 0])
        #self._run_movement_blocking([movements], self.speed)
    
        #time.sleep(self.wait)
    
        movements = self._arm_movement(left_arm=[71.8, 0.8, -69.6, -53.3, -92.5, 0])
        self._run_movement_blocking([movements], self.speed)
    
    def bait_right(self):
        movements = self._arm_movement(right_arm=[57.0, -38.4, 30.8, 119.5, 88.4, 0])
        self._run_movement_blocking([movements], self.speed)
    
        time.sleep(1)
    
        movements = self._arm_movement(right_arm=[57.0, -38.4, 30.8, 119.5, -88.4, 0])
        self._run_movement_blocking([movements], self.speed)
    
        time.sleep(self.wait)
    
        movements = self._arm_movement(right_arm=[71.8, -0.8, 69.6, 53.3, 92.5, 0])
        self._run_movement_blocking([movements], self.speed)        
        """
        movements = self._arm_movement(right_arm=[10.9, -49, 4.6, 85.4, 96.4, 0])
        self._run_movement_blocking([movements], self.speed)
    
        time.sleep(1)
    
        movements = self._arm_movement(right_arm=[10.9, -49, 4.6, 85.4, -70.6, 0])
        self._run_movement_blocking([movements], self.speed)
    
        time.sleep(self.wait)
    
        movements = self._arm_movement(right_arm=[71.8, -0.8, 69.6, 53.3, 92.5, 0])
        self._run_movement_blocking([movements], self.speed)
        """
    
    def left_gaze_point(self, dog_name):
        arm_angle_lsts = [40.1, 44.6, -5.3, -39.9, 5.8, 1]
        head_angle_lsts = [38, 11.5]
        self._gaze_point(dog_name, head_angle_lsts=head_angle_lsts, left_arm_angles=arm_angle_lsts)
    
    def right_gaze_point(self, dog_name):
        arm_angle_lsts = [40.1, -44.6, 5.3, 39.9, -5.8, 1]
        head_angle_lsts = [-38, 11.5]
        self._gaze_point(dog_name, head_angle_lsts=head_angle_lsts, right_arm_angles=arm_angle_lsts)
    
    def head_left_turn(self):
        movements = self._head_movement([38, -23.7])
        self._run_movement_blocking([movements], 0.3)
    
    def head_right_turn(self):
        movements = self._head_movement([-38, -23.7])
        self._run_movement_blocking([movements], 0.3)    
    
    def praise(self, dog_gender):
        self._speech("Good! " + dog_gender + "!")
        self.stand(0.4)
    
    def torso_stand(self, speed=None):
        left_arm = [83.4, 10.4, -24, -67.5, 6.7, 0.3]
        right_arm = [83.4, -10.4, 24, 67.5, 6.7, 0.3]
        
        left_leg = [-10.1, 7.5, 5.6, -5.2, -7.4, 5.1]
        right_leg = [-10.1, 7.5, -5.6, -5.2, 7.4, 5.1]
        
        arm_movements = self._arm_movement(left_arm=left_arm, right_arm=right_arm)
        leg_movements = self._leg_movement(left_leg=left_leg, right_leg=right_leg)
        
        if speed == None:
            speed = self.speed
            
        self._run_movement_blocking([arm_movements], self.speed)
    
    def torso_stand_unblocking(self):
        left_arm = [83.4, 10.4, -24, -67.5, 6.7, 0.3]
        right_arm = [83.4, -10.4, 24, 67.5, 6.7, 0.3]
    
        left_leg = [-10.1, 7.5, 5.6, -5.2, -7.4, 5.1]
        right_leg = [-10.1, 7.5, -5.6, -5.2, 7.4, 5.1]
    
        arm_movements = self._arm_movement(left_arm=left_arm, right_arm=right_arm)
        leg_movements = self._leg_movement(left_leg=left_leg, right_leg=right_leg)
    
        self._run_movement_unblocking([arm_movements], self.speed)        
    
    def start_idle(self):
        for chain in ["Body", "Legs", "Arms", "LArm", "RArm"]:
            self.motionProxy.setBreathEnabled(chain, True)
    
    def stop_idle(self):
        for chain in ["Body", "Legs", "Arms", "LArm", "RArm"]:
            self.motionProxy.setBreathEnabled(chain, False)
            
    def head_down(self):
        self.motionProxy.setAngles("HeadPitch", [28.5 * almath.TO_RAD], self.speed)
    
    def head_up(self):
        self.motionProxy.setAngles("HeadPitch", [-9.1 * almath.TO_RAD], self.speed)

def custom_print(message):
    print message
    sys.stdout.flush()

def stand(nao, speed):
    custom_print("stand")
    nao.stand(speed)

def introduction_1(nao, dog_name, owner_name):
    custom_print("intro 1")
    nao.head_left_turn()
    time.sleep(0.7)
    nao._speech("Hi")

def introduction_2(nao, dog_name, owner_name):
    custom_print("intro 2")
    # head turn to owner
    stand(nao, 0.2)

def introduction_3(nao, dog_name, owner_name):
    custom_print("intro 3")
    nao._interaction_speech("Hello! \\pau=400\\ " + owner_name)
    #nao.torso_stand()
    stand(nao, 0.2)

def introduction_4(nao, dog_name, owner_name):
    custom_print("intro 4")
    nao._interaction_speech("Nice to meet you. \\pau=900\\ I am Nao. \\pau=900\\ How are you.")
    #nao.torso_stand()
    stand(nao, 0.2)
    
def introduction_5(nao, dog_name, owner_name):
    custom_print("intro 5")
    nao._interaction_speech("Hi! \\pau=100\\ " + dog_name)
    time.sleep(0.5)
    nao._interaction_speech("I am so happy to meet you today. \\pau=900\\ I heard that \\pau=50\\ we will play some fun games together. \\pau=900\\ Hope that \\pau=10\\ you can find all the treats")
    #nao.torso_stand()
    stand(nao, 0.2)
    
    ## give treat
    #introduction_bait_only(nao)

def introduction_6(nao, dog_name, owner_name):
    custom_print("intro 6")
    nao._interaction_speech("Great! \\pau=900\\ Now lets start the game.")
    stand(nao, 0.2)

def get_bait(nao):
    custom_print("get bait")
    # give treat
    nao.get_bait()
    
def bait_warmup_left(nao):
    custom_print("warmup left bait")
    nao.bait_left()

def bait_warmup_right(nao):
    custom_print("warmup right bait")
    nao.bait_right()

def bait_test(nao):
    custom_print("test bait")
    nao.bait_middle()

def point_left(nao, dog_name):
    custom_print("point left")
    nao.left_gaze_point(dog_name)

def point_right(nao, dog_name):
    custom_print("point right")
    nao.right_gaze_point(dog_name)

def release_spoon(nao):
    custom_print("release spoon")
    nao._open_hand()
    nao.torso_stand()

def get_spoon(nao):
    custom_print("get spoon")
    nao._close_hand()

def release_dog(nao):
    custom_print("release dog")
    nao._speech("\\emph=1\\ Oh \\emph=0\\ kay")

def praise(nao, dog_gender):
    custom_print("praise")
    nao.torso_stand_unblocking()
    nao.head_up()
    nao.praise(dog_gender)
    #nao.stand(0.2)

def stand_back(nao, speed):
    custom_print("stand back")
    nao.torso_stand(speed)
    nao.stand(speed)

def rest(nao):
    custom_print("rest")
    nao.kneels(0.4)
    
def command_talk(nao, message):
    custom_print("command talk")
    nao._speech(message)

def start_idle(nao):
    custom_print("start idle")
    nao.start_idle()

def stop_idle(nao):
    custom_print("stop idle")
    nao.stop_idle()

def parse_command(nao, command_list, pid):
    new_pid = None
    command = command_list[0]
    if command.startswith("introduction"):
        command = command.split()[1]
        dog_name = command_list[1]
        owner_name = command_list[2]
        if command == "1":
            introduction_1(nao, dog_name, owner_name)
        elif command == "2":
            introduction_2(nao, dog_name, owner_name)
        elif command == "3":
            introduction_3(nao, dog_name, owner_name)
        elif command == "4":
            introduction_4(nao, dog_name, owner_name)
        elif command == "5":
            introduction_5(nao, dog_name, owner_name)
        elif command == "6":
            introduction_6(nao, dog_name, owner_name)        
    elif command == "command talk":
        command_talk(nao, command_list[1])
    elif command == "get treat":
        get_bait(nao)
    elif command == "warmup bait left":
        bait_warmup_left(nao)
    elif command == "warmup bait right":
        bait_warmup_right(nao)
    elif command == "test bait":
        bait_test(nao)
    elif command == "point left":
        point_left(nao, command_list[1])
    elif command == "point right":
        point_right(nao, command_list[1])
    elif command == "get spoon":
        get_spoon(nao)
    elif command == "release spoon":
        release_spoon(nao);
    elif command == "release dog":
        release_dog(nao)
    elif command == "praise":
        praise(nao, command_list[1])
    elif command == "stand":
        stand(nao, 0.1)
    elif command == "rest":
        rest(nao)
    elif command == "stand back":
        stand_back(nao, 0.1)
    elif command == "start idle":
        if len(pid) != 0:
            for current_pid in idle_pid:
                os.killpg(os.getpgid(current_pid), signal.SIGTERM)
        while len(pid) != 0:
            pid.pop()     
        idle_process = subprocess.Popen("python ./robot_idle.py", stdout=None, shell=True, preexec_fn=os.setsid) 
        new_pid = idle_process.pid
        start_idle(nao)
    elif command == "stop idle":
        stop_idle(nao)
        if len(pid) != 0:
            for current_pid in idle_pid:
                os.killpg(os.getpgid(current_pid), signal.SIGTERM)
        while len(pid) != 0:
            pid.pop()
    
    return new_pid

def log(log_file_name, message):
    log_file = open("logs/" + log_file_name, "a+")
    log_file.write("[" + str(datetime.datetime.today()) + "]: " + message + "\n")
    log_file.close()

if __name__ == "__main__":
    CONNECTION_RESPOND = "success"
    LINE_TERMINATOR = "\n"
    DELIMINATOR = "|"
    
    robot_ip = "192.168.1.102"
    robot_port = 9559
    robot_speed = 0.2 # default: 0.1
    robot_wait = 0.3 # default: 0.5 or 1
    
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
    
    nao = naoRobot(robot_ip, robot_port, robot_speed, robot_wait)
    
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
                command_list = data.strip().split(DELIMINATOR)
                pid = parse_command(nao, command_list, idle_pid)
                if pid != None:
                    idle_pid.append(pid)
                connection.sendall(CONNECTION_RESPOND + LINE_TERMINATOR)
            else:
                custom_print("received empty data, close socket")
                log(file_name, "close socket")
                is_connected = False               
        