import socket
import sys
import time

from naoqi import ALProxy
import almath

def progressToAngle(progress):
    return (float(progress) * ROBOT_HEAD_RANGE / PROGRESS_BAR_RANGE) * almath.TO_RAD

def angleToProgress(angle):
    return int(round((angle / almath.TO_RAD) * PROGRESS_BAR_RANGE / ROBOT_HEAD_RANGE, 1))

def custom_print(message):
    print message
    sys.stdout.flush()

if __name__ == "__main__":
    # Comment all these out so this is no longer a server
    # and do not need other signals to run
    CONNECTION_RESPOND = "success"
    LINE_TERMINATOR = "\n"
    DELIMINATOR = "|"
    GET_HEAD_ANGLE = "get head angle"
    SET_HEAD_ANGLE = "set head angle"
    PROGRESS_BAR_RANGE = 100.0
    ROBOT_HEAD_RANGE = 75.0
    
    robot_ip = "192.168.1.102"
    robot_port = 9559
    robot_speed = 0.1
    motionProxy = ALProxy("ALMotion", robot_ip, robot_port)   
    
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.1.116"
    server_port = 10001
    server_address = (server_ip, server_port)
    socket.bind(server_address)
    socket.listen(1)
    
    custom_print("server ip: " + server_ip)
    custom_print("server port: " + str(server_port))
    
    try:
        while True:
            connection, client_address = socket.accept()
            custom_print("get connection from " + str(client_address))
            is_connected = True
            
            while is_connected:
                data = connection.recv(1024)
                message = CONNECTION_RESPOND + LINE_TERMINATOR
                if data:
                    custom_print("received: " + data.strip())
                    data = data.strip().split(DELIMINATOR)
                    if data[0] == GET_HEAD_ANGLE:
                        angle = motionProxy.getAngles("HeadYaw", False)[0]
                        progress = angleToProgress(angle)
                        message = str(progress) + LINE_TERMINATOR
                    elif data[0] == SET_HEAD_ANGLE:
                        angle = progressToAngle(data[1])
                        motionProxy.setAngles("HeadYaw", [angle], robot_speed)
                    custom_print("sent: " + message)
                    connection.sendall(message)
                else:
                    custom_print("received empty data, close socket")
                    is_connected = False
            connection.close()
    except KeyboardInterrupt:
        socket.shutdown()
        socket.close()
        custom_print("real time server receive keyboard interruption, close socket and shut server down")    