#! /usr/bin/python

import json
from collections import OrderedDict

json_file='data.json'
json_data = open(json_file)
data = json.load(json_data, object_pairs_hook=OrderedDict)
json_data.close()
count = 0

for section in data.keys():
    for keyword in data[section].keys():
        for command_type in data[section][keyword].keys():
            count += 1
            #command = data[section][keyword][command_type]["text"]
            #robot = []
            #flag = []
            
            #data[section][keyword][command_type]["robot"] = robot
            #data[section][keyword][command_type]["flag"] = flag

new_json_data = open("new_data.json", "w")
json.dump(data, new_json_data, indent = 4, separators=(',', ': '))
new_json_data.close()

#print data["Unexpected"]["pointer explain"]["full"]["text"]