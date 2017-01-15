import json
import traci
import traci.constants as tc
from colorama import Fore

from app import Config
from app.entitiy.CarRegistry import CarRegistry
from app.logging import info
from app.network.Network import Network

from app.routing.CustomRouter import CustomRouter
from app.streaming import KafkaConnector


class Simulation(object):
    """ here we run the simulation in """

    # the current tick of the simulation
    tick = 0

    @classmethod
    def applyFileConfig(cls):
        """ reads configs from a json and applies it at realtime to the simulation """
        try:
            config = json.load(open('./knobs.json'))
            CustomRouter.victimsPercentage = config['victimsPercentage']
            CustomRouter.averageEdgeDurationFactor = config['averageEdgeDurationFactor']
            CustomRouter.maxSpeedAndLengthFactor = config['maxSpeedAndLengthFactor']
            CustomRouter.freshnessUpdateFactor = config['freshnessUpdateFactor']
            CustomRouter.freshnessCutOffValue = config['freshnessCutOffValue']
        except:
            pass

    @classmethod
    def start(cls):
        """ start the simulation """
        info("# Start adding initial cars to the simulation", Fore.MAGENTA)
        # apply the configuration from the json file
        cls.applyFileConfig()
        CarRegistry.applyCarCounter()
        cls.loop()

    @classmethod
    # @profile
    def loop(cls):
        """ loops the simulation """

        # start listening to all cars that arrived at their target
        traci.simulation.subscribe((tc.VAR_ARRIVED_VEHICLES_IDS,))
        while 1:
            # Do one simulation step
            cls.tick += 1
            traci.simulationStep()

            # Check for removed cars and re-add them into the system
            for removedCarId in traci.simulation.getSubscriptionResults()[122]:
                CarRegistry.findById(removedCarId).setArrived(cls.tick)

            # let the cars process this step
            CarRegistry.processTick(cls.tick)

            # if we enable this we get debug information in the sumo-gui using global traveltime
            # should not be used for normal running, just for debugging
            # if (cls.tick % 10) == 0:
            #   for e in Network.routingEdges:
            # 1)     traci.edge.adaptTraveltime(e.id, 100*e.averageDuration/e.predictedDuration)
            # 2)     traci.edge.adaptTraveltime(e.id, e.averageDuration)
            # 3)     traci.edge.adaptTraveltime(e.id, (cls.tick-e.lastDurationUpdateTick)) # how old the data is

            # real time update of config if we are not in kafka mode
            if (cls.tick % 100) == 0:
                if Config.kafkaUpdates is False:
                    # json mode
                    cls.applyFileConfig()
                else:
                    # kafka mode
                    newConf = KafkaConnector.checkForNewConfiguration()
                    if newConf is not None:
                        if "victim_percentage" in newConf:
                            CustomRouter.victimsPercentage = newConf["victim_percentage"]
                            print("setting victimsPercentage: " + str(newConf["victim_percentage"]))
                        if "route_random_sigma" in newConf:
                            CustomRouter.routeRandomSigma = newConf["route_random_sigma"]
                            print("setting routeRandomSigma: " + str(newConf["route_random_sigma"]))
                        if "max_speed_and_length_factor" in newConf:
                            CustomRouter.maxSpeedAndLengthFactor = newConf["max_speed_and_length_factor"]
                            print("setting maxSpeedAndLengthFactor: " + str(newConf["max_speed_and_length_factor"]))
                        if "average_edge_duration_factor" in newConf:
                            CustomRouter.averageEdgeDurationFactor = newConf["average_edge_duration_factor"]
                            print("setting averageEdgeDurationFactor: " + str(newConf["average_edge_duration_factor"]))
                        if "freshness_update_factor" in newConf:
                            CustomRouter.freshnessUpdateFactor = newConf["freshness_update_factor"]
                            print("setting freshnessUpdateFactor: " + str(newConf["freshness_update_factor"]))
                        if "freshness_cut_off_value" in newConf:
                            CustomRouter.freshnessCutOffValue = newConf["freshness_cut_off_value"]
                            print("setting freshnessCutOffValue: " + str(newConf["freshness_cut_off_value"]))

            # print status update if we are not running in parallel mode
            if (cls.tick % 100) == 0 and Config.parallelMode is False:
                print(str(Config.processID) + " -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                    traci.vehicle.getIDCount()) + "/" + str(
                    CarRegistry.totalCarCounter) + " # avgTripDuration: " + str(
                    CarRegistry.totalTripAverage) + "(" + str(
                    CarRegistry.totalTrips) + ")" + " # avgTripEfficiency: " + str(
                    CarRegistry.totalTripOverheadAverage))

            # if we are in paralllel mode we end the simulation after 10000 ticks with a result output
            if (cls.tick % 10000) == 0 and Config.parallelMode:
                # end the simulation here
                print(str(Config.processID) + " -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                    traci.vehicle.getIDCount()) + "/" + str(
                    CarRegistry.totalCarCounter) + " # avgTripDuration: " + str(
                    CarRegistry.totalTripAverage) + "(" + str(
                    CarRegistry.totalTrips) + ")" + " # avgTripEfficiency: " + str(
                    CarRegistry.totalTripOverheadAverage))
                return