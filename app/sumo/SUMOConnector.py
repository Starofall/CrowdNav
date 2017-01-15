from sumolib import checkBinary
from app import Config
import traci
from colorama import Fore


# Starts SUMO in the background using the defined network
def start():
    if Config.sumoUseGUI:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", Config.sumoConfig,"--no-step-log", "true","--no-warnings","true"])

