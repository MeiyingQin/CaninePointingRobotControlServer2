from bait import Dispenser
import threading
import json

DISPENSER_USER_NAME = "user_name"
DISPENSER_PASSWORD = "password"

dispenser_file = 'dispenser_settings.json'
dispenser_data = open(dispenser_file)
dispenser_json = json.load(dispenser_data)
dispenser_data.close()

dispensers = []
for dispenser in dispenser_json.keys():
    user_name = dispenser_json[dispenser][DISPENSER_USER_NAME]
    password = dispenser_json[dispenser][DISPENSER_PASSWORD]
    dispensers.append(Dispenser(user_name, password))

def dispenser_rotate(dispenser_lists):
    setup_threads = []

    for dispenser in dispenser_lists:
        dispenser.setup_page()
        setup_dispenser_thread = threading.Thread(target=Dispenser.setup_page, args=(dispenser, False))
        setup_threads.append(setup_dispenser_thread)
    
    for thread in setup_threads:
        thread.start()
    
    for thread in setup_threads:
        thread.join()

    threads = []
    for dispenser in dispenser_lists:
        dispenser_thread = threading.Thread(target=Dispenser.feed, args=(dispenser, ))
        threads.append(dispenser_thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

def close_session(dispenser_lists):
    for dispenser in dispenser_lists:
        dispenser.close()

# dispenser_rotate(dispensers)
is_continue = True
while is_continue:
    user_input = raw_input("press any key to start rotating dispensers, press q to quit: ")
    if user_input == "q":
        is_continue = False
        close_session(dispensers)
    else:
        dispenser_rotate(dispensers)