#! /usr/bin/python

import json
import string
import os
from collections import OrderedDict

json_file='../data.json'
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
punctuation = punctuation.replace("_", "")
punctuation = punctuation.replace("=", "")

def get_json_file_data(file_name):
	json_file = '../actions.json'
    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()
    return data

def add_names(names, target_dict, category):
	for name in names:
		if name in target_dict.keys():
			print category, " name ", name, " already in recorded"
		else:
			target_dict[name] = 0

actions = get_json_file_data("../actions.json")
names = get_json_file_data("./names.json")

is_loop = False

action_dict = {}
for key in actions.keys():
    action_dict[key] = 0

sound_to_record = []
sound_dict = {}

target_directories = [
    "../../NaoBehaviours/NaoSoundLibraries"
]

add_names(names["owners"], sound_dict, "owner")
add_names(names["dogs"], sound_dict, "dog")
add_names(names["assistants"], sound_dict, "assistant")

for target_directory in target_directories:
    for root, dirs, files in os.walk(target_directory):
        for name in files:
        	if name.endswith("\.ogg")
	            name = name[:-4]
	            if name in sound_dict.keys():
	                print name, "already in recorded"
	            else:
	                #print name
	                sound_dict[name] = 0

for section in data.keys():
    for keyword in data[section].keys():
        for command_condition in data[section][keyword].keys():
            count += 1
            texts = data[section][keyword][command_condition]["text"]
            data[section][keyword][command_condition]["robot"] = []
            data[section][keyword][command_condition]["flag"] = []
            for text in texts:
                commands = text.strip().split("|")
                robot_command = ""
                to_be_added = ""
                is_speech = True
                for command in commands:
                    command = command.strip().lower()
                    command = "".join(i for i in command if i not in list(punctuation))
                    if command.startswith("["): # actions
                        command = command.replace("[", "")
                        command = command.replace("]", "")
                        detailed_command = command.split("/")
                        #print detailed_command
                        command_type = detailed_command[0]
                        command_content = detailed_command[1]
                        # check if action defined
                        action_dict[command_content] += 1
                        # start define command
                        if command_type == "b":
                            robot_command += "^run("
                            robot_command += actions[command_content]
                            robot_command += ") "
                            if command_content.startswith("loop"):
                                is_loop = True
                                to_be_added = "^stop(" + actions[command_content] + ") "
                        elif command_type == "nb":
                            robot_command += "^start("
                            robot_command += actions[command_content]
                            robot_command += ") "
                            if command_content.startswith("loop"):
                                is_loop = True
                                to_be_added = "^stop(" + actions[command_content] + ") "
                            else:
                                to_be_added = "^wait(" + actions[command_content] + ") "
                        elif command_type == "u":
                            is_speech = False
                            robot_command += command_content
                        else:
                            print section + "|" + keyword + "|" + command_condition + ": has invalid action type - " + command_type
                    elif command.startswith("{"): # direct naoqi command like pause
                        command = command.replace("{", "")
                        command = command.replace("}", "")
                        robot_command += command.strip() + " "
                        if is_loop:
                            robot_command += to_be_added
                            to_be_added = ""
                            is_loop = False
                    else: # speech
                        # remember to replace <owner>, <pointer>, <dog>, <dog_gender>, <assistant>, later
                        # speech
                        detailed_command = command.split("/")
                        #print detailed_command
                        command_type = detailed_command[0]
                        if "<" in detailed_command[1]:
                            command_content = detailed_command[1].strip().replace(" ", "_")
                        else:
                            command_content = section.replace(" ", "_") + "_" + command_condition + "_" + keyword.replace(" ", "_") + "_" + detailed_command[1].strip().replace(" ", "_")
                        command_content = command_content.lower()
                        # check if sound file exist
                        if command_content not in sound_dict.keys():
                            sound_to_record.append(command_content)
                        else:
                            sound_dict[command_content] += 1
                        # start define command
                        if command_type == "d":
                            robot_command += "^mode(disabled)" + " "
                            robot_command += "^runSound(CanineStudy/"
                            robot_command += command_content
                            robot_command += ") "
                            if not is_loop:
                                robot_command += to_be_added
                                to_be_added = ""
                        elif command_type == "c":
                            robot_command += "^mode(contextual)" + " "
                            robot_command += "^runSound(CanineStudy/"
                            robot_command += command_content
                            robot_command += ") "
                            if not is_loop:
                                robot_command += to_be_added
                                to_be_added = ""                        
                        else:
                            print section + "|" + keyword + "|" + command_condition + ": has invalid saying type - " + command_type
                data[section][keyword][command_condition]["robot"].append(robot_command)
                if is_speech:
                    data[section][keyword][command_condition]["flag"].append("speech")
                else:
                    data[section][keyword][command_condition]["flag"].append("action")
            #robot = []
            #flag = []
            
            #data[section][keyword][command_type]["robot"] = robot
            #data[section][keyword][command_type]["flag"] = flag

new_json_data = open("../new_new_data.json", "w")
json.dump(data, new_json_data, indent = 4, separators=(',', ': '))
new_json_data.close()

"""
keys = action_dict.keys()
keys.sort()
for key in keys:
    print key, action_dict[key]
"""

print "command needs to be recorded are:"
sound_to_record.sort()
for command in sound_to_record:
    if "<" not in command:
    #if "<" not in command and not command.startswith("warmup") and not command.startswith("testing"):
        print command

print

print "command not used are:"
sounds = sound_dict.keys()
sounds.sort()
for sound in sounds:
    if sound_dict[sound] == 0:
        print sound

print

print "command used more than once: "
sounds = sound_dict.keys()
sounds.sort()
for sound in sounds:
    if sound_dict[sound] > 1:
        print sound