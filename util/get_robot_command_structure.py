#! /usr/bin/python

import json
import string
from collections import OrderedDict

json_file='data.json'
json_data = open(json_file)
data = json.load(json_data, object_pairs_hook=OrderedDict)
json_data.close()
count = 0
punctuation = string.punctuation
punctuation = punctuation.replace("{", "")
punctuation = punctuation.replace("}", "")
punctuation = punctuation.replace("<", "")
punctuation = punctuation.replace(">", "")
punctuation = punctuation.replace("\\", "")
punctuation = punctuation.replace("[", "")
punctuation = punctuation.replace("]", "")
punctuation = punctuation.replace("/", "")
punctuation = punctuation.replace("|", "")

actions_json_file = 'actions.json'
actions_json_data = open(actions_json_file)
actions = json.load(actions_json_data)
actions_json_data.close()

for section in data.keys():
    for keyword in data[section].keys():
        for command_type in data[section][keyword].keys():
            count += 1
            commands = data[section][keyword][command_type]["text"].strip().split("|")
            robot_command = ""
            to_be_added = ""
            for command in commands:
                command = command.strip()
                command = "".join(i for i in command if i not in list(punctuation))
                if command.startswith("["):
                    command = command.replace("[", "")
                    command = command.replace("]", "")
                    detailed_command = command.split("/")
                    command_type = detailed_command[0]
                    command_content = detailed_command[1]
                    if command_type == "b":
                        robot_command += "^run("
                        robot_command += actions[command_content]
                        robot_command += ") "
                    elif command_type == "nb":
                            robot_command += "^start("
                            robot_command += actions[command_content]
                            robot_command += ") "
                            to_be_added = "^wait(" + actions[command_content] + ") "
                    else:
                        print section + "|" + keyword + "|" + command_type + ": has invalid action type"
                elif command.startswith("{"):
                    command = command.replace("{", "")
                    command = command.replace("}", "")
                    robot_command += command.strip() + " "
                else:
                    # remember to replace <owner>, <pointer>, <dog>, <dog_gender>, <assistant>, later
                    # speech
                    detailed_command = command.split("/")
                    command_type = detailed_command[0]
                    command_content = detailed_command[1]                    
                    if command_type == "d":
                        robot_command += "^mode(disabled)" + " "
                        robot_command += "^runSound(****/"
                        robot_command += command_content.replace(" ", "_")
                        robot_command += ") "
                        robot_command += to_be_added
                        to_be_added = ""
                    elif command_type == "c":
                        robot_command += "^mode(contextual)" + " "
                        robot_command += "^mode(disabled)" + " "
                        robot_command += "^runSound("
                        robot_command += command_content
                        robot_command += ") "
                        robot_command += to_be_added
                        to_be_added = ""                        
                    else:
                        print section + "|" + keyword + "|" + command_type + ": has invalid saying type"
            #robot = []
            #flag = []
            
            #data[section][keyword][command_type]["robot"] = robot
            #data[section][keyword][command_type]["flag"] = flag

new_json_data = open("new_new_data.json", "w")
json.dump(data, new_json_data, indent = 4, separators=(',', ': '))
new_json_data.close()

#print data["Unexpected"]["pointer explain"]["full"]["text"]