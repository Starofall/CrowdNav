import json
import traci
import traci.constants as tc
from app.network.Network import Network

from app.streaming import RTXForword
from colorama import Fore

from app import Config
from app.entitiy.CarRegistry import CarRegistry
from app.logging import info
from app.routing.CustomRouter import CustomRouter
from app.streaming import RTXConnector
import time

# get the current system time
from app.routing.RoutingEdge import RoutingEdge

current_milli_time = lambda: int(round(time.time() * 1000))


class Simulation(object):
    """ here we run the simulation in """

    # the current tick of the simulation
    tick = 0

    # last tick time
    lastTick = current_milli_time()

    @classmethod
    def applyFileConfig(cls):
        """ reads configs from a json and applies it at realtime to the simulation """
        try:
            config = json.load(open('./knobs.json'))
            CustomRouter.explorationPercentage = config['explorationPercentage']
            CustomRouter.averageEdgeDurationFactor = config['averageEdgeDurationFactor']
            CustomRouter.maxSpeedAndLengthFactor = config['maxSpeedAndLengthFactor']
            CustomRouter.freshnessUpdateFactor = config['freshnessUpdateFactor']
            CustomRouter.freshnessCutOffValue = config['freshnessCutOffValue']
            CustomRouter.reRouteEveryTicks = config['reRouteEveryTicks']
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

            # Log tick duration to kafka
            duration = current_milli_time() - cls.lastTick
            cls.lastTick = current_milli_time()
            msg = dict()
            msg["duration"] = duration
            RTXForword.publish(msg, Config.kafkaTopicPerformance)

            # Check for removed cars and re-add them into the system
            for removedCarId in traci.simulation.getSubscriptionResults()[122]:
                CarRegistry.findById(removedCarId).setArrived(cls.tick)

            timeBeforeCarProcess = current_milli_time()
            # let the cars process this step
            CarRegistry.processTick(cls.tick)
            # log time it takes for routing
            msg = dict()
            msg["duration"] = current_milli_time() - timeBeforeCarProcess
            RTXForword.publish(msg, Config.kafkaTopicRouting)

            # if we enable this we get debug information in the sumo-gui using global traveltime
            # should not be used for normal running, just for debugging
            # if (cls.tick % 10) == 0:
            # for e in Network.routingEdges:
            # 1)     traci.edge.adaptTraveltime(e.id, 100*e.averageDuration/e.predictedDuration)
            #     traci.edge.adaptTraveltime(e.id, e.averageDuration)
            # 3)     traci.edge.adaptTraveltime(e.id, (cls.tick-e.lastDurationUpdateTick)) # how old the data is

            # real time update of config if we are not in kafka mode
            if (cls.tick % 10) == 0:
                if Config.kafkaUpdates is False and Config.mqttUpdates is False:
                    # json mode
                    cls.applyFileConfig()
                else:
                    # kafka mode
                    newConf = RTXConnector.checkForNewConfiguration()
                    if newConf is not None:
                        if "exploration_percentage" in newConf:
                            CustomRouter.explorationPercentage = newConf["exploration_percentage"]
                            print("setting victimsPercentage: " + str(newConf["exploration_percentage"]))
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
                        if "re_route_every_ticks" in newConf:
                            CustomRouter.reRouteEveryTicks = newConf["re_route_every_ticks"]
                            print("setting reRouteEveryTicks: " + str(newConf["re_route_every_ticks"]))
                        if "total_car_counter" in newConf:
                            CarRegistry.totalCarCounter = newConf["total_car_counter"]
                            CarRegistry.applyCarCounter()
                            print("setting totalCarCounter: " + str(newConf["total_car_counter"]))
                        if "edge_average_influence" in newConf:
                            RoutingEdge.edgeAverageInfluence = newConf["edge_average_influence"]
                            print("setting edgeAverageInfluence: " + str(newConf["edge_average_influence"]))

            # print status update if we are not running in parallel mode
            if (cls.tick % 100) == 0 and Config.parallelMode is False:
                print(str(Config.processID) + " -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                    traci.vehicle.getIDCount()) + "/" + str(
                    CarRegistry.totalCarCounter) + " # avgTripDuration: " + str(
                    CarRegistry.totalTripAverage) + "(" + str(
                    CarRegistry.totalTrips) + ")" + " # avgTripOverhead: " + str(
                    CarRegistry.totalTripOverheadAverage))

                # @depricated -> will be removed
                # # if we are in paralllel mode we end the simulation after 10000 ticks with a result output
                # if (cls.tick % 10000) == 0 and Config.parallelMode:
                #     # end the simulation here
                #     print(str(Config.processID) + " -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                #         traci.vehicle.getIDCount()) + "/" + str(
                #         CarRegistry.totalCarCounter) + " # avgTripDuration: " + str(
                #         CarRegistry.totalTripAverage) + "(" + str(
                #         CarRegistry.totalTrips) + ")" + " # avgTripOverhead: " + str(
                #         CarRegistry.totalTripOverheadAverage))
                #     return
