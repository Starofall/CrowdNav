import threading
import time
# import os , sys
# package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# # Add the parent directory to the Python path
# sys.path.append(package_path)
from app.simulation.Simulation import Simulation
from app.streaming import RTXConnector



def read_data_thread(thread_id):
    for i in range(5):
        print('Thread', {thread_id})
        time.sleep(1)

if __name__ == "__main__":
    threads = []

    # Create and start multiple threads
    newConf = RTXConnector.checkForNewConfiguration()
    print(RTXConnector)
    for i in range(3):
        thread = threading.Thread(target=read_data_thread, args=(i,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads have finished reading data.")
