from bait import Dispenser
import threading

dispenser_1 = Dispenser("robot.pointing.feeder.1@gmail.com", "")
dispenser_2 = Dispenser("robot.pointing.feeder.2@gmail.com", "")

dispensers = [dispenser_1, dispenser_2]

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