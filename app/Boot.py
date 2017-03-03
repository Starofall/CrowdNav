import os, sys

from app.streaming import RTXConnector

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))

from app.logging import info
from app.routing.CustomRouter import CustomRouter
from app.network.Network import Network
from app.simulation.Simulation import Simulation
from streaming import RTXForword
from colorama import Fore
from sumo import SUMOConnector, SUMODependency
import Config
import traci, sys, os
import thread
import time


# uuid4()
def start(processID, parallelMode,useGUI):
    """ main entry point into the application """
    Config.processID = processID
    Config.parallelMode = parallelMode
    Config.sumoUseGUI = useGUI

    info('#####################################', Fore.CYAN)
    info('#      Starting CrowdNav v0.2       #', Fore.CYAN)
    info('#####################################', Fore.CYAN)
    info('# Configuration:', Fore.YELLOW)
    info('# Kafka-Host   -> ' + Config.kafkaHost, Fore.YELLOW)
    info('# Kafka-Topic1 -> ' + Config.kafkaTopicTrips, Fore.YELLOW)
    info('# Kafka-Topic2 -> ' + Config.kafkaTopicPerformance, Fore.YELLOW)

    # init sending updates to kafka and getting commands from there
    if Config.kafkaUpdates or Config.mqttUpdates:
        RTXForword.connect()
        RTXConnector.connect()

    # Check if sumo is installed and available
    SUMODependency.checkDeps()
    info('# SUMO-Dependency check OK!', Fore.GREEN)

    # Load the sumo map we are using into Python
    Network.loadNetwork()
    info(Fore.GREEN + "# Map loading OK! " + Fore.RESET)
    info(Fore.CYAN + "# Nodes: " + str(Network.nodesCount()) + " / Edges: " + str(Network.edgesCount()) + Fore.RESET)

    # After the network is loaded, we init the router
    CustomRouter.init()
    # Start sumo in the background
    SUMOConnector.start()
    info("\n# SUMO-Application started OK!", Fore.GREEN)
    # Start the simulation
    Simulation.start()
    # Simulation ended, so we shutdown
    info(Fore.RED + '# Shutdown' + Fore.RESET)
    traci.close()
    sys.stdout.flush()
    return None
