from __future__ import print_function

from subprocess import Popen

from app import Boot
import sys

# this script is used to run CrowdNav on multiple processes
# call it with >parallel.py #threads
if __name__ == "__main__":
    try:
        processorCount = int(sys.argv[1])
    except:
        processorCount = 4
    for i in range(0, processorCount):
        simulation = Popen(["python", "./run.py", str(i)])
        print("Simulations started...")
