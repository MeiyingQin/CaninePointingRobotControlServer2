import socket
##import os
##import signal
##import subprocess
import sys
#import datetime
#import time
#import json
#import random
#import threading

def custom_print(message):
    print message
    sys.stdout.flush()

if __name__ == "__main__":
    CONNECTION_RESPOND = "success"
    LINE_TERMINATOR = "\n"
    
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_ip = "192.168.1.101"
    server_ip = "192.168.1.116"
    server_port = 10000
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
                if data:
                    custom_print("received: " + data.strip())
                    connection.sendall(CONNECTION_RESPOND + LINE_TERMINATOR)
                else:
                    custom_print("received empty data, close socket")
                    is_connected = False
            
            connection.close()
    except KeyboardInterrupt:
        socket.close()
        custom_print("main server receive keyboard interruption, close socket and shut server down")
  