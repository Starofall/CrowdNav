from app import Boot
import sys

# this starts the simulation (int parameters are used for parallel mode)
if __name__ == "__main__":
    try:
        processID = int(sys.argv[1])
        parallelMode = True
        useGUI = False
    except:
        processID = 0
        parallelMode = False
        useGUI = True
    if processID is not None:
        # Starting the application
        Boot.start(processID, parallelMode,useGUI)
