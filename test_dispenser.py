from bait import Dispenser
import threading
import json

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
    threads = []
    for dispenser in dispenser_lists:
        dispenser_thread = threading.Thread(target=Dispenser.feed, args=(dispenser, ))
        threads.append(dispenser_thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

dispenser_rotate(dispensers)