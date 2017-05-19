import random
import traci
import traci.constants as tc
from app import Config

from app.Util import addToAverage
from app.logging import CSVLogger
from app.network.Network import Network
from app.routing.CustomRouter import CustomRouter
from app.routing.RouterResult import RouterResult
from app.streaming import RTXForword


class Car:
    """ a abstract class of something that is driving around in the streets """

    def __init__(self, id):
        # the string id
        self.id = id  # type: str
        # the rounds this car already drove
        self.rounds = 0  # type: int
        # the current route as a RouterResult
        self.currentRouterResult = None  # type: RouterResult
        # when we started the route
        self.currentRouteBeginTick = None
        # the id of the current route (somu)
        self.currentRouteID = None  # type: str
        # the id of the current edge/street the car is driving (sumo)
        self.currentEdgeID = None
        # the tick this car got on this edge/street
        self.currentEdgeBeginTick = None
        # the target node this car drives to
        self.targetID = None
        # the source node this car is coming from
        self.sourceID = None
        # if it is disabled, it will stop driving
        self.disabled = False
        # the cars acceleration in the simulation
        self.acceleration = max(1, random.gauss(4, 2))
        # the cars deceleration in the simulation
        self.deceleration = max(1, random.gauss(6, 2))
        # the driver imperfection in handling the car
        self.imperfection = min(0.9, max(0.1, random.gauss(0.5, 0.5)))
        # is this car a smart car
        self.smartCar = Config.smartCarPercentage > random.random()
        # number of ticks since last reroute / arrival
        self.lastRerouteCounter = 0

    def setArrived(self, tick):
        """ car arrived at its target, so we add some statistic data """

        # import here because python can not handle circular-dependencies
        from app.entitiy.CarRegistry import CarRegistry
        # add a round to the car
        self.rounds += 1
        self.lastRerouteCounter = 0
        if tick > Config.initialWaitTicks and self.smartCar:  # as we ignore the first 1000 ticks for this
            # add a route to the global registry
            CarRegistry.totalTrips += 1
            # add the duration for this route to the global tripAverage
            durationForTrip = (tick - self.currentRouteBeginTick)
            CarRegistry.totalTripAverage = addToAverage(CarRegistry.totalTrips,  # 100 for faster updates
                                                        CarRegistry.totalTripAverage,
                                                        durationForTrip)
            # CSVLogger.logEvent("arrived", [tick, self.sourceID, self.targetID,
            #                                durationForTip, self.id,self.currentRouterResult.isVictim])
            # log the overrhead values
            minimalCosts = CustomRouter.minimalRoute(self.sourceID, self.targetID, None, None).totalCost
            tripOverhead = durationForTrip / minimalCosts / 1.1  # 1.6 is to correct acceleration and deceleration
            # when the distance is very short, we have no overhead
            if durationForTrip < 10:
                tripOverhead = 1
            # in rare cases a trip does take very long - as most outliers are <30, we cap the overhead to 30 here
            if tripOverhead > 30:
                print("-> capped overhead to 30 - " + str(minimalCosts) + " - " + str(durationForTrip) + " - " + str(
                    tripOverhead))
                tripOverhead = 30

            CarRegistry.totalTripOverheadAverage = addToAverage(CarRegistry.totalTrips,
                                                                CarRegistry.totalTripOverheadAverage,
                                                                tripOverhead)
            CSVLogger.logEvent("overhead", [tick, self.sourceID, self.targetID, durationForTrip,
                                            minimalCosts, tripOverhead, self.id, self.currentRouterResult.isVictim])
            # log to kafka
            msg = dict()
            msg["tick"] = tick
            msg["overhead"] = tripOverhead
            RTXForword.publish(msg, Config.kafkaTopicTrips)
        # if car is still enabled, restart it in the simulation
        if self.disabled is False:
            self.addToSimulation(tick)

    def __createNewRoute(self, tick):
        """ creates a new route to a random target and uploads this route to SUMO """
        # import here because python can not handle circular-dependencies
        if self.targetID is None:
            self.sourceID = random.choice(Network.nodes).getID()
        else:
            self.sourceID = self.targetID  # We start where we stopped
        # random target
        self.targetID = random.choice(Network.nodes).getID()
        self.currentRouteID = self.id + "-" + str(self.rounds)
        self.currentRouterResult = CustomRouter.route(self.sourceID, self.targetID, tick, self)
        if len(self.currentRouterResult.route) > 0:
            traci.route.add(self.currentRouteID, self.currentRouterResult.route)
            # set color to red
            return self.currentRouteID
        else:
            # recursion aka. try again as this should work!
            return self.__createNewRoute(tick)

    def processTick(self, tick):
        """ process changes that happened in the tick to this car """

        self.lastRerouteCounter += 1
        # reroute every x ticks based on config value
        if self.lastRerouteCounter >= CustomRouter.reRouteEveryTicks and CustomRouter.reRouteEveryTicks > 0:
            self.lastRerouteCounter = 0
            if self.smartCar:
                try:
                    oldRoute = self.currentRouterResult.route
                    currentEdgeID = traci.vehicle.getRoadID(self.id)
                    nextNodeID = Network.getEdgeIDsToNode(currentEdgeID).getID()
                    self.currentRouterResult = CustomRouter.route(nextNodeID, self.targetID, tick, self)
                    traci.vehicle.setRoute(self.id, [currentEdgeID] + self.currentRouterResult.route)
                    # print("OLD: " + str(oldRoute) + " - NEW: " + str(self.currentRouterResult.route))
                except IndexError as e:
                    # print(e)
                    pass
                except traci.exceptions.TraCIException as e:
                    # print(e)
                    pass

        roadID = traci.vehicle.getSubscriptionResults(self.id)[80]
        if roadID != self.currentEdgeID and self.smartCar:
            if self.currentEdgeBeginTick is not None:
                CustomRouter.applyEdgeDurationToAverage(self.currentEdgeID, tick - self.currentEdgeBeginTick, tick)
                # CSVLogger.logEvent("edge", [tick, self.currentEdgeID,
                #                             tick - self.currentEdgeBeginTick, self.id])
                # log to kafak
                # msg = dict()
                # msg["tick"] = tick
                # msg["edgeID"] = self.currentEdgeID,
                # msg["duration"] = tick - self.currentEdgeBeginTick
            # print("changed route to: " + roadID)
            self.currentEdgeBeginTick = tick
            self.currentEdgeID = roadID
            pass

    def addToSimulation(self, tick):
        """ adds this car to the simulation through the traci API """
        self.currentRouteBeginTick = tick
        try:
            traci.vehicle.add(self.id, self.__createNewRoute(tick), tick, -4, -3)
            traci.vehicle.subscribe(self.id, (tc.VAR_ROAD_ID,))
            # ! currently disabled for performance reasons
            # traci.vehicle.setAccel(self.id, self.acceleration)
            # traci.vehicle.setDecel(self.id, self.deceleration)
            # traci.vehicle.setImperfection(self.id, self.imperfection)
            if self.smartCar:
                # set color to red
                if self.currentRouterResult.isVictim:
                    traci.vehicle.setColor(self.id, (0, 255, 0, 0))
                else:
                    traci.vehicle.setColor(self.id, (255, 0, 0, 0))
            else:
                # dump car is using SUMO default routing, so we reroute using the same target
                # putting the next line left == ALL SUMO ROUTING
                traci.vehicle.changeTarget(self.id, self.currentRouterResult.route[-1])
        except Exception as e:
            print("error adding" + str(e))
            # try recursion, as this should normally work
            # self.addToSimulation(tick)

    def remove(self):
        """" removes this car from the sumo simulation through traci """
        traci.vehicle.remove(self.id)
