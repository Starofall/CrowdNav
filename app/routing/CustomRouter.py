from random import gauss, random

import sys
from dijkstar import Graph, find_path

from app.network.Network import Network
from app.routing.RouterResult import RouterResult


class CustomRouter(object):
    """ our own custom defined router """

    # Empty starting references
    edgeMap = None
    graph = None

    # the percentage of smart cars that should be used for exploration
    explorationPercentage = 0.0 # INITIAL JSON DEFINED!!!
    # randomizes the routes
    routeRandomSigma = 0.2 # INITIAL JSON DEFINED!!!
    # how much speed influences the routing
    maxSpeedAndLengthFactor = 1 # INITIAL JSON DEFINED!!!
    # multiplies the average edge value
    averageEdgeDurationFactor = 1 # INITIAL JSON DEFINED!!!
    # how important it is to get new data
    freshnessUpdateFactor = 10 # INITIAL JSON DEFINED!!!
    # defines what is the oldest value that is still a valid information
    freshnessCutOffValue = 500.0 # INITIAL JSON DEFINED!!!
    # how often we reroute cars
    reRouteEveryTicks = 20 # INITIAL JSON DEFINED!!!

    @classmethod
    def init(self):
        """ set up the router using the already loaded network """
        self.graph = Graph()
        self.edgeMap = {}
        for edge in Network.routingEdges:
            self.edgeMap[edge.id] = edge
            self.graph.add_edge(edge.fromNodeID, edge.toNodeID,
                                {'length': edge.length, 'maxSpeed': edge.maxSpeed,
                                 'lanes': len(edge.lanes), 'edgeID': edge.id})

    @classmethod
    def minimalRoute(cls, fr, to, tick, car):
        """creates a minimal route based on length / speed  """
        cost_func = lambda u, v, e, prev_e: e['length'] / e['maxSpeed']
        route = find_path(cls.graph, fr, to, cost_func=cost_func)
        return RouterResult(route, False)

    @classmethod
    def route(cls, fr, to, tick, car):
        """ creates a route from the f(node) to the t(node) """
        # 1) SIMPLE COST FUNCTION
        # cost_func = lambda u, v, e, prev_e: max(0,gauss(1, CustomRouter.routeRandomSigma) \
        #                                         * (e['length']) / (e['maxSpeed']))

        # if car.victim:
        #     # here we reduce the cost of an edge based on how old our information is
        #     print("victim routing!")
        #     cost_func = lambda u, v, e, prev_e: (
        #         cls.getAverageEdgeDuration(e["edgeID"]) -
        #         (tick - (cls.edgeMap[e["edgeID"]].lastDurationUpdateTick))
        #     )
        # else:
        # 2) Advanced cost function that combines duration with averaging
        # isVictim = ??? random x percent (how many % routes have been victomized before)
        isVictim = cls.explorationPercentage > random()
        if isVictim:
            victimizationChoice = 1
        else:
            victimizationChoice = 0

        cost_func = lambda u, v, e, prev_e: \
            cls.getFreshness(e["edgeID"], tick) * \
            cls.averageEdgeDurationFactor * \
            cls.getAverageEdgeDuration(e["edgeID"]) \
            + \
            (1 - cls.getFreshness(e["edgeID"], tick)) * \
            cls.maxSpeedAndLengthFactor * \
            max(1, gauss(1, cls.routeRandomSigma) *
            (e['length']) / e['maxSpeed']) \
            - \
            (1 - cls.getFreshness(e["edgeID"], tick)) * \
            cls.freshnessUpdateFactor * \
            victimizationChoice

        # generate route
        route = find_path(cls.graph, fr, to, cost_func=cost_func)
        # wrap the route in a result object
        return RouterResult(route, isVictim)

    @classmethod
    def getFreshness(cls, edgeID, tick):
        try:
            lastUpdate = float(tick) - cls.edgeMap[edgeID].lastDurationUpdateTick
            return 1 - min(1, max(0, lastUpdate / cls.freshnessCutOffValue))
        except TypeError as e:
            # print("error in getFreshnessFactor" + str(e))
            return 1

    @classmethod
    def getAverageEdgeDuration(cls, edgeID):
        """ returns the average duration for this edge in the simulation """
        try:
            return cls.edgeMap[edgeID].averageDuration
        except:
            print("error in getAverageEdgeDuration")
            return 1

    @classmethod
    def applyEdgeDurationToAverage(cls, edge, duration, tick):
        """ tries to calculate how long it will take for a single edge """
        try:
            cls.edgeMap[edge].applyEdgeDurationToAverage(duration, tick)
        except:
            return 1
