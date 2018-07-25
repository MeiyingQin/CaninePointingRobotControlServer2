import json

def get_data(path):
    json_file = path
    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()
    return data
    
server_data = get_data("../data.json")
gui_data = get_data("../../GUI/CaninePointingGuiProgressController2/app/src/main/assets/data.json")

server_data_extract = {}
gui_data_extract = {}

for session in server_data.keys():
    if session not in server_data_extract.keys():
        server_data_extract[session] = server_data[session].keys()

for session in gui_data.keys():
    if session.startswith("Warmup"):
        if "Warmup" not in gui_data_extract.keys():
            gui_data_extract["Warmup"] = gui_data[session].keys()
        else:
            gui_data_extract["Warmup"].extend(gui_data[session].keys())
    elif session.startswith("Testing"):
        if "Testing" not in gui_data_extract.keys():
            gui_data_extract["Testing"] = gui_data[session].keys()
        else:
            gui_data_extract["Testing"].extend(gui_data[session].keys())
    else:
        if session not in gui_data_extract.keys():
            gui_data_extract[session] = gui_data[session].keys()

for session in server_data.keys():
    print "========================================================"
    print "working on session: ", session
    current_server_data_extract = set(server_data_extract[session])
    current_gui_data_extract = set(gui_data_extract[session])
    print
    print "in server but not in gui: "
    for element in current_server_data_extract.difference(current_gui_data_extract):
        print element
    print
    print "in gui but not in server: "
    for element in current_gui_data_extract.difference(current_server_data_extract):
        print element    